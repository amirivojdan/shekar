import numpy as np
import onnxruntime as ort
from pathlib import Path

from shekar.utils import get_onnx_providers
from shekar.transliteration.byt5_tokenizer import ByT5Tokenizer


class ByT5Decoder:
    def __init__(self, model_path: str | Path):
        self._session = self._make_session(Path(model_path))
        self._tokenizer = ByT5Tokenizer()

        dec_input_names = [i.name for i in self._session.get_inputs()]
        dec_output_names = [o.name for o in self._session.get_outputs()]

        self._past_self_k = self._by_idx(
            [
                n
                for n in dec_input_names
                if n.startswith("past_key_values.") and n.endswith(".decoder.key")
            ]
        )
        self._past_self_v = [n.replace(".key", ".value") for n in self._past_self_k]
        self._past_cross_k = self._by_idx(
            [
                n
                for n in dec_input_names
                if n.startswith("past_key_values.") and n.endswith(".encoder.key")
            ]
        )
        self._past_cross_v = [n.replace(".key", ".value") for n in self._past_cross_k]

        self._present_self_k = self._by_idx(
            [
                n
                for n in dec_output_names
                if n.startswith("present.") and n.endswith(".decoder.key")
            ]
        )
        self._present_self_v = [
            n.replace(".key", ".value") for n in self._present_self_k
        ]
        self._present_cross_k = self._by_idx(
            [
                n
                for n in dec_output_names
                if n.startswith("present.") and n.endswith(".encoder.key")
            ]
        )
        self._present_cross_v = [
            n.replace(".key", ".value") for n in self._present_cross_k
        ]

        self._output_names = dec_output_names
        self._has_use_cache_branch = "use_cache_branch" in dec_input_names
        self._num_layers = len(self._past_self_k)

        kv_meta = next(
            i for i in self._session.get_inputs() if i.name == self._past_self_k[0]
        )
        shape = kv_meta.shape
        self._num_heads = int(shape[1]) if isinstance(shape[1], int) else 6
        self._d_kv = int(shape[3]) if isinstance(shape[3], int) else 64

    @staticmethod
    def _make_session(path: Path) -> ort.InferenceSession:
        so = ort.SessionOptions()
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
        so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        return ort.InferenceSession(
            str(path), sess_options=so, providers=get_onnx_providers()
        )

    @staticmethod
    def _by_idx(names: list[str]) -> list[str]:
        return sorted(names, key=lambda n: int(n.split(".")[1]))

    @staticmethod
    def _log_softmax(x: np.ndarray) -> np.ndarray:
        x = x - x.max()
        return x - np.log(np.exp(x).sum())

    @staticmethod
    def _log_softmax_2d(x: np.ndarray) -> np.ndarray:
        x = x - x.max(axis=-1, keepdims=True)
        return x - np.log(np.exp(x).sum(axis=-1, keepdims=True))

    def _empty_self_past(self, batch_size: int) -> dict:
        zero = np.zeros((batch_size, self._num_heads, 0, self._d_kv), dtype=np.float32)
        feed = {}
        for k, v in zip(self._past_self_k, self._past_self_v):
            feed[k] = zero
            feed[v] = zero
        return feed

    def _empty_cross_past(self, batch_size: int, enc_seq_len: int) -> dict:
        zero = np.zeros(
            (batch_size, self._num_heads, enc_seq_len, self._d_kv), dtype=np.float32
        )
        feed = {}
        for k, v in zip(self._past_cross_k, self._past_cross_v):
            feed[k] = zero
            feed[v] = zero
        return feed

    def decode(
        self,
        enc_out: np.ndarray,
        attention_mask: np.ndarray,
        num_beams: int = 4,
        max_new_tokens: int = 256,
    ) -> list[int]:
        """Run beam-search decoding given encoder outputs.

        Returns token ids with the leading decoder-start and trailing EOS already stripped.
        """
        src_len = attention_mask.shape[1]

        first_feed = {
            "input_ids": np.array([[self._tokenizer._pad_id]], dtype=np.int64),
            "encoder_attention_mask": attention_mask,
            "encoder_hidden_states": enc_out,
        }
        first_feed.update(self._empty_self_past(1))
        first_feed.update(self._empty_cross_past(1, src_len))
        if self._has_use_cache_branch:
            first_feed["use_cache_branch"] = np.array([False], dtype=bool)

        out0 = self._session.run(None, first_feed)
        n2o = dict(zip(self._output_names, out0))
        logp = self._log_softmax(n2o["logits"][0, -1])
        top_ids = np.argpartition(-logp, num_beams)[:num_beams]
        top_ids = top_ids[np.argsort(-logp[top_ids])]

        seqs = [[self._tokenizer._pad_id, int(t)] for t in top_ids]
        scores = logp[top_ids].astype(np.float32)

        self_k = [np.repeat(n2o[n], num_beams, axis=0) for n in self._present_self_k]
        self_v = [np.repeat(n2o[n], num_beams, axis=0) for n in self._present_self_v]
        cross_k = [np.repeat(n2o[n], num_beams, axis=0) for n in self._present_cross_k]
        cross_v = [np.repeat(n2o[n], num_beams, axis=0) for n in self._present_cross_v]

        enc_out_b = np.repeat(enc_out, num_beams, axis=0)
        enc_mask_b = np.repeat(attention_mask, num_beams, axis=0)

        finished: list[tuple[float, list[int]]] = []

        for _ in range(max_new_tokens - 1):
            last_tokens = np.array([[s[-1]] for s in seqs], dtype=np.int64)
            feed = {
                "input_ids": last_tokens,
                "encoder_attention_mask": enc_mask_b,
                "encoder_hidden_states": enc_out_b,
            }
            for i in range(self._num_layers):
                feed[self._past_self_k[i]] = self_k[i]
                feed[self._past_self_v[i]] = self_v[i]
                feed[self._past_cross_k[i]] = cross_k[i]
                feed[self._past_cross_v[i]] = cross_v[i]
            if self._has_use_cache_branch:
                feed["use_cache_branch"] = np.array([True], dtype=bool)

            outs = self._session.run(None, feed)
            n2o = dict(zip(self._output_names, outs))
            logits = n2o["logits"][:, -1, :]
            logp = self._log_softmax_2d(logits)

            cand_scores = scores[:, None] + logp
            flat = cand_scores.reshape(-1)
            top_idx = np.argpartition(-flat, num_beams)[:num_beams]
            top_idx = top_idx[np.argsort(-flat[top_idx])]
            beam_idx = top_idx // logp.shape[1]
            tok_idx = top_idx % logp.shape[1]
            new_scores = flat[top_idx]

            new_seqs = []
            for b, t, s in zip(beam_idx, tok_idx, new_scores):
                seq = seqs[b] + [int(t)]
                new_seqs.append(seq)
                if int(t) == self._tokenizer._eos_id:
                    lp = len(seq) - 1
                    finished.append((float(s) / max(lp, 1), seq))

            # Self-attn KV grows every step; take the full updated cache from model output.
            self_k = [n2o[n][beam_idx] for n in self._present_self_k]
            self_v = [n2o[n][beam_idx] for n in self._present_self_v]
            # Cross-attn KV is constant; re-index by selected parent beams.
            cross_k = [cross_k[i][beam_idx] for i in range(self._num_layers)]
            cross_v = [cross_v[i][beam_idx] for i in range(self._num_layers)]

            seqs = new_seqs
            scores = new_scores

            if finished and max(s for s, _ in finished) >= float(scores.max()):
                break

        if not finished:
            best_seq = seqs[int(np.argmax(scores))]
        else:
            best_seq = max(finished, key=lambda x: x[0])[1]

        if best_seq and best_seq[0] == self._tokenizer._pad_id:
            best_seq = best_seq[1:]
        if best_seq and best_seq[-1] == self._tokenizer._eos_id:
            best_seq = best_seq[:-1]

        return best_seq
