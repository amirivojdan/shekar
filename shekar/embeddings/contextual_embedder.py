import numpy as np

from .albert_embedder import AlbertEmbedder
from .base import BaseEmbedder

CONTEXTUAL_EMBEDDING_REGISTRY = {
    "albert": AlbertEmbedder,
}


class ContextualEmbedder(BaseEmbedder):
    """ContextualEmbedder class for embedding sentences using pre-trained models.
    Args:
        model (str): Name of the word embedding model to use.
        model_path (str, optional): Path to the pre-trained model file. If None, it will be downloaded from the hub.
    Raises:
        ValueError: If the specified model is not found in the registry.
    """

    supports_batching = True

    def __init__(self, model: str = "albert", *, batch_size=32, model_path=None):
        self.batch_size = self._validate_batch_size(batch_size)
        model = model.lower()
        if model not in CONTEXTUAL_EMBEDDING_REGISTRY:
            raise ValueError(
                f"Unknown contextual embedding model '{model}'. Available: {list(CONTEXTUAL_EMBEDDING_REGISTRY.keys())}"
            )

        factory = CONTEXTUAL_EMBEDDING_REGISTRY[model]
        self.embedder = (
            factory() if model_path is None else factory(model_path=model_path)
        )
        if getattr(self.embedder, "supports_batching", False) is True:
            self.embedder.batch_size = self.batch_size

    def embed(self, phrase: str) -> np.ndarray:
        if not isinstance(phrase, str):
            return self.embed_batch(phrase)
        return self.embedder(phrase)

    def transform(self, X: str) -> np.ndarray:
        return self.embed(X)

    def embed_batch(self, texts, *, batch_size=None):
        size = self.batch_size if batch_size is None else batch_size
        if getattr(self.embedder, "supports_batching", False) is True:
            return self.embedder.embed_batch(texts, batch_size=size)
        vectors = [
            self.embedder(text)
            for batch in self._text_batches(texts, size)
            for text in batch
        ]
        return np.asarray(vectors)

    def transform_batch(self, texts, *, batch_size=None):
        return self.embed_batch(texts, batch_size=batch_size)
