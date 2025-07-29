import pickle

import numpy as np
from shekar.hub import Hub
from pathlib import Path
from .base import BaseEmbedder

WORD_EMBEDDING_REGISTRY = {
    "fasttext-d100": "fasttext_d100_w5_v100k_cbow_wiki.bin",
    "fasttext-d300": "fasttext_d300_w10_v250k_cbow_naab.bin",
}


class WordEmbedder(BaseEmbedder):
    """WordEmbedder class for embedding words using pre-trained models.
    Args:
        model (str): Name of the word embedding model to use.
        model_path (str, optional): Path to the pre-trained model file. If None, it will be downloaded from the hub.
    Raises:
        ValueError: If the specified model is not found in the registry.
    """

    def __init__(
        self, model: str = "fasttext-d100", model_path=None, oov_strategy: str = "zero"
    ):
        """Initialize the WordEmbedder with a specified model and path.
        Args:

            model (str): Name of the word embedding model to use.
            model_path (str, optional): Path to the pre-trained model file. If None,
                it will be downloaded from the hub.
            oov_strategy (str): Strategy for handling out-of-vocabulary words. Default is "zero". Can be "zero", "none", or "error".
        Raises:
            ValueError: If the specified model is not found in the registry.
        """

        super().__init__()
        self.oov_strategy = oov_strategy
        model = model.lower()
        if model not in WORD_EMBEDDING_REGISTRY:
            raise ValueError(
                f"Unknown word embedding model '{model}'. Available: {list(WORD_EMBEDDING_REGISTRY.keys())}"
            )

        resource_name = WORD_EMBEDDING_REGISTRY[model]
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        model = pickle.load(open(model_path, "rb"))
        self.words = model["words"]
        self.embeddings = model["embeddings"]
        self.vector_size = model["vector_size"]
        self.window = model["window"]
        self.model_type = model["model"]
        self.epochs = model["epochs"]
        self.dataset = model["dataset"]

        self.token2idx = {word: idx for idx, word in enumerate(self.words)}

    def embed(self, token: str) -> np.ndarray:
        if token in self.token2idx:
            index = self.token2idx[token]
            return self.embeddings[index]
        else:
            if self.oov_strategy == "zero":
                return np.zeros(self.vector_size)
            elif self.oov_strategy == "none":
                return None
            elif self.oov_strategy == "error":
                raise KeyError(f"Token '{token}' not found in the vocabulary.")

    def transform(self, X: str) -> np.ndarray:
        return self.embed(X)

    def most_similar(self, token: str, top_n: int = 5) -> list:
        """Find the most similar tokens to a given token.
        Args:
            token (str): The token to find similar tokens for.
            top_n (int): Number of similar tokens to return.
        Returns:
            list: List of tuples containing similar tokens and their similarity scores.
        """

        vec = self.embed(token)
        if vec is None:
            return []

        similarities = []
        for other_token in self.words:
            if other_token != token:
                sim = self.similarity(token, other_token)
                similarities.append((other_token, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]
