import numpy as np


class ByT5Tokenizer:
    def __init__(self):
        self._pad_id = 0
        self._eos_id = 1
        self._byte_offset = 3

    def tokenize(self, text: str) -> np.ndarray:
        ids = [b + self._byte_offset for b in text.encode("utf-8")]
        ids.append(self._eos_id)
        return np.asarray(ids, dtype=np.int64)

    def detokenize(self, ids) -> str:
        out = bytearray()
        for i in ids:
            i = int(i)
            if i < self._byte_offset:
                continue
            out.append(i - self._byte_offset)
        return out.decode("utf-8", errors="replace")

    def batch_tokenize(self, texts: list[str]) -> tuple[np.ndarray, np.ndarray]:
        seqs = [self.tokenize(t) for t in texts]
        maxlen = max(len(s) for s in seqs)
        input_ids = np.full((len(seqs), maxlen), self._pad_id, dtype=np.int64)
        attn = np.zeros((len(seqs), maxlen), dtype=np.int64)
        for i, s in enumerate(seqs):
            input_ids[i, : len(s)] = s
            attn[i, : len(s)] = 1
        return input_ids, attn
