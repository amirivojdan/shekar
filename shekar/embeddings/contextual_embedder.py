import numpy as np
from .base import BaseEmbedder
from .albert_embedder import AlbertEmbedder

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

    def __init__(self, model: str = "albert"):
        model = model.lower()
        if model not in CONTEXTUAL_EMBEDDING_REGISTRY:
            raise ValueError(
                f"Unknown contextual embedding model '{model}'. Available: {list(CONTEXTUAL_EMBEDDING_REGISTRY.keys())}"
            )

        self.embedder = CONTEXTUAL_EMBEDDING_REGISTRY[model]()

    def embed(self, phrase: str) -> np.ndarray:
        return self.embedder(phrase)

    def transform(self, X: str) -> np.ndarray:
        return self.embed(X)
