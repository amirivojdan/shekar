from numbers import Integral
from pathlib import Path

import numpy as np
import onnxruntime as ort

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
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
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

    @staticmethod
    def validate_generation_parameters(
        num_beams: int,
        max_new_tokens: int,
    ) -> None:
        if (
            isinstance(num_beams, bool)
            or not isinstance(num_beams, Integral)
            or num_beams < 1
        ):
            raise ValueError("num_beams must be a positive integer.")
        if (
            isinstance(max_new_tokens, bool)
            or not isinstance(max_new_tokens, Integral)
            or max_new_tokens < 1
        ):
            raise ValueError("max_new_tokens must be a positive integer.")

    @staticmethod
    def _normalized_score(score: float, sequence: list[int]) -> float:
        generated_length = max(len(sequence) - 1, 1)
        return float(score) / generated_length

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
        self.validate_generation_parameters(num_beams, max_new_tokens)

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
        vocab_size = logp.shape[0]
        if num_beams >= vocab_size:
            raise ValueError(
                f"num_beams must be smaller than the vocabulary size ({vocab_size})."
            )

        eos_id = self._tokenizer._eos_id
        start_id = self._tokenizer._pad_id
        finished: list[tuple[float, list[int]]] = [
            (
                float(logp[eos_id]),
                [start_id, eos_id],
            )
        ]

        active_logp = logp.copy()
        active_logp[eos_id] = -np.inf
        top_ids = np.argsort(-active_logp, kind="stable")[:num_beams]

        seqs = [[start_id, int(token_id)] for token_id in top_ids]
        scores = active_logp[top_ids].astype(np.float32)

        self_k = [np.repeat(n2o[n], num_beams, axis=0) for n in self._present_self_k]
        self_v = [np.repeat(n2o[n], num_beams, axis=0) for n in self._present_self_v]
        cross_k = [np.repeat(n2o[n], num_beams, axis=0) for n in self._present_cross_k]
        cross_v = [np.repeat(n2o[n], num_beams, axis=0) for n in self._present_cross_v]

        enc_out_b = np.repeat(enc_out, num_beams, axis=0)
        enc_mask_b = np.repeat(attention_mask, num_beams, axis=0)

        for _ in range(max_new_tokens - 1):
            best_finished_score = max(score for score, _ in finished)
            best_active_upper_bound = float(scores.max()) / max_new_tokens
            if best_finished_score >= best_active_upper_bound:
                break

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

            for beam_index, sequence in enumerate(seqs):
                eos_sequence = sequence + [eos_id]
                finished.append(
                    (
                        self._normalized_score(
                            cand_scores[beam_index, eos_id],
                            eos_sequence,
                        ),
                        eos_sequence,
                    )
                )

            active_scores = cand_scores.copy()
            active_scores[:, eos_id] = -np.inf
            flat = active_scores.reshape(-1)
            top_idx = np.argsort(-flat, kind="stable")[:num_beams]
            beam_idx = top_idx // logp.shape[1]
            tok_idx = top_idx % logp.shape[1]
            new_scores = flat[top_idx]

            new_seqs = [
                seqs[beam_index] + [int(token_id)]
                for beam_index, token_id in zip(beam_idx, tok_idx)
            ]

            # Self-attn KV grows every step; take the full updated cache from model output.
            self_k = [n2o[n][beam_idx] for n in self._present_self_k]
            self_v = [n2o[n][beam_idx] for n in self._present_self_v]
            # Cross-attn KV is constant; re-index by selected parent beams.
            cross_k = [cross_k[i][beam_idx] for i in range(self._num_layers)]
            cross_v = [cross_v[i][beam_idx] for i in range(self._num_layers)]

            seqs = new_seqs
            scores = new_scores

        candidates = finished + [
            (self._normalized_score(score, sequence), sequence)
            for score, sequence in zip(scores, seqs)
        ]
        best_seq = max(candidates, key=lambda candidate: candidate[0])[1]

        if best_seq and best_seq[0] == start_id:
            best_seq = best_seq[1:]
        if best_seq and best_seq[-1] == eos_id:
            best_seq = best_seq[:-1]

        return best_seq
