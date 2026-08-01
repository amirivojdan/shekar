import pickle
from numbers import Integral
from pathlib import Path

import numpy as np

from shekar.hub import Hub

from .base import BaseEmbedder

WORD_EMBEDDING_REGISTRY = {
    "fasttext-d100": "fasttext_d100_w5_v100k_cbow_wiki.bin",
    "fasttext-d300": "fasttext_d300_w10_v250k_cbow_naab.bin",
}

_OOV_STRATEGIES = frozenset({"zero", "none", "error"})


class _RestrictedEmbeddingUnpickler(pickle.Unpickler):
    """Load legacy NumPy embedding dictionaries without arbitrary globals."""

    _ALLOWED_GLOBALS = {
        ("numpy", "dtype"): np.dtype,
        ("numpy", "ndarray"): np.ndarray,
        ("numpy._core.multiarray", "_reconstruct"): np._core.multiarray._reconstruct,
        ("numpy._core.multiarray", "scalar"): np._core.multiarray.scalar,
        ("numpy._core.numeric", "_frombuffer"): np._core.numeric._frombuffer,
        ("numpy.core.multiarray", "_reconstruct"): np._core.multiarray._reconstruct,
        ("numpy.core.multiarray", "scalar"): np._core.multiarray.scalar,
        ("numpy.core.numeric", "_frombuffer"): np._core.numeric._frombuffer,
    }

    def find_class(self, module: str, name: str):
        allowed = self._ALLOWED_GLOBALS.get((module, name))
        if allowed is None:
            raise pickle.UnpicklingError(
                f"Unsupported global in embedding model: {module}.{name}"
            )
        return allowed


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
        if not isinstance(oov_strategy, str) or oov_strategy not in _OOV_STRATEGIES:
            available = ", ".join(sorted(_OOV_STRATEGIES))
            raise ValueError(
                f"Unknown OOV strategy '{oov_strategy}'. Available: {available}"
            )
        self.oov_strategy = oov_strategy
        model = model.lower()
        if model not in WORD_EMBEDDING_REGISTRY:
            raise ValueError(
                f"Unknown word embedding model '{model}'. Available: {list(WORD_EMBEDDING_REGISTRY.keys())}"
            )

        resource_name = WORD_EMBEDDING_REGISTRY[model]
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        model_data = self._load_model(Path(model_path))
        self.words = list(model_data["words"])
        self.embeddings = np.asarray(model_data["embeddings"])
        self.vector_size = int(model_data["vector_size"])
        self._validate_model()

        self.window = int(model_data["window"])
        self.model_type = str(model_data["model"])
        self.epochs = int(model_data["epochs"])
        self.dataset = str(model_data["dataset"])

        self.token2idx = {word: idx for idx, word in enumerate(self.words)}

        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        self._normalized_embeddings = np.zeros_like(
            self.embeddings,
            dtype=np.result_type(self.embeddings.dtype, np.float32),
        )
        np.divide(
            self.embeddings,
            norms,
            out=self._normalized_embeddings,
            where=norms != 0,
        )

    @staticmethod
    def _load_model(model_path: Path) -> dict:
        """Load NPZ models safely, with pickle support for legacy hosted models."""

        if model_path.suffix.lower() == ".npz":
            with np.load(model_path, allow_pickle=False) as model:
                return {key: model[key] for key in model.files}

        with open(model_path, "rb") as model_file:
            return _RestrictedEmbeddingUnpickler(model_file).load()

    def _validate_model(self) -> None:
        if self.embeddings.ndim != 2:
            raise ValueError("Embedding matrix must be two-dimensional.")
        if not np.issubdtype(self.embeddings.dtype, np.number):
            raise ValueError("Embedding matrix must contain numeric values.")
        if self.embeddings.shape[0] != len(self.words):
            raise ValueError(
                "Embedding matrix row count must match the vocabulary size."
            )
        if self.vector_size <= 0 or self.embeddings.shape[1] != self.vector_size:
            raise ValueError(
                "vector_size must be positive and match the embedding matrix width."
            )
        if not all(isinstance(word, str) for word in self.words):
            raise ValueError("Embedding vocabulary must contain only strings.")
        if len(set(self.words)) != len(self.words):
            raise ValueError("Embedding vocabulary contains duplicate tokens.")
        if not np.isfinite(self.embeddings).all():
            raise ValueError("Embedding matrix contains non-finite values.")

    def embed(self, token: str) -> np.ndarray:
        if token in self.token2idx:
            index = self.token2idx[token]
            return self.embeddings[index]

        if self.oov_strategy == "zero":
            return np.zeros(self.vector_size, dtype=self.embeddings.dtype)
        if self.oov_strategy == "none":
            return None
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

        if isinstance(top_n, bool) or not isinstance(top_n, Integral) or top_n < 0:
            raise ValueError("top_n must be a non-negative integer.")
        top_n = int(top_n)
        if top_n == 0:
            return []

        vec = self.embed(token)
        if vec is None:
            return []

        query_norm = np.linalg.norm(vec)
        if query_norm == 0:
            normalized_query = np.zeros_like(
                vec,
                dtype=self._normalized_embeddings.dtype,
            )
        else:
            normalized_query = vec / query_norm

        similarities = self._normalized_embeddings @ normalized_query
        order = np.argsort(-similarities, kind="stable")

        token_index = self.token2idx.get(token)
        if token_index is not None:
            order = order[order != token_index]

        return [
            (self.words[index], float(similarities[index])) for index in order[:top_n]
        ]
