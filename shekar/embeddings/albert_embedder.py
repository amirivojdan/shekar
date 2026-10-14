from pathlib import Path

import numpy as np

from shekar.hub import resolve_model_path
from shekar.tokenization import AlbertTokenizer
from shekar.utils import create_onnx_session

from .base import BaseEmbedder


class AlbertEmbedder(BaseEmbedder):
    supports_batching = True

    def __init__(self, model_path: str | Path | None = None, *, batch_size=32):
        super().__init__()
        self.batch_size = self._validate_batch_size(batch_size)
        resource_name = "albert_persian_mlm_embeddings.onnx"
        model_path = resolve_model_path(model_path, resource_name)
        self.session = create_onnx_session(model_path)
        self._session_batch_size(self.session, self.batch_size)
        self.tokenizer = AlbertTokenizer(
            enable_padding=True,
            enable_truncation=True,
            return_overflowing_tokens=True,
        )
        self.vector_size = 768

    def embed(self, phrase) -> np.ndarray:
        if not isinstance(phrase, str):
            return self.embed_batch(phrase)
        return self._transform_batch([phrase], self.batch_size)[0]

    def embed_batch(self, texts, *, batch_size=None) -> np.ndarray:
        vectors = super().transform_batch(texts, batch_size=batch_size)
        return np.asarray(vectors, dtype=np.float32).reshape(-1, self.vector_size)

    def transform_batch(self, texts, *, batch_size=None):
        return self.embed_batch(texts, batch_size=batch_size)

    def _transform_batch(self, texts, batch_size):
        sums = np.zeros((len(texts), self.vector_size), dtype=np.float64)
        counts = np.zeros(len(texts), dtype=np.float64)
        size = self._session_batch_size(self.session, batch_size)
        names = {item.name for item in self.session.get_inputs()}
        encoded = (self.tokenizer(text) for text in texts)
        for inputs, owners in AlbertTokenizer._encoded_batches(
            encoded, size, self.tokenizer.pad_token_id, trim_padding=True
        ):
            hidden = self.session.run(
                ["last_hidden_state"], {k: v for k, v in inputs.items() if k in names}
            )[0]
            mask = inputs["attention_mask"].astype(hidden.dtype)
            # Preserve the existing pooling policy, including special tokens.
            row_sums = (hidden * mask[:, :, None]).sum(axis=1)
            for row, (document, _, _) in enumerate(owners):
                sums[document] += row_sums[row]
                counts[document] += mask[row].sum()
        return (sums / np.maximum(counts[:, None], 1e-9)).astype(np.float32)
