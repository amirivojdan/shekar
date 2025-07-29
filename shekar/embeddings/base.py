from abc import abstractmethod
from shekar.base import BaseTransform
import numpy as np


class BaseEmbedder(BaseTransform):
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors.
        Args:
            vec1 (np.ndarray): First vector.
            vec2 (np.ndarray): Second vector.
            Returns:
            float: Cosine similarity between the two vectors.
        """

        if (
            vec1 is None
            or not isinstance(vec1, np.ndarray)
            or (vec2 is None or not isinstance(vec2, np.ndarray))
        ):
            return 0.0

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    @abstractmethod
    def embed(self, text: str) -> np.ndarray:
        """Embed a given text/token into a vector representation.
        Args:
            text (str): Input text to be embedded.
        Returns:
            np.ndarray: Vector representation of the input text.
        """
        pass

    def transform(self, X: str) -> np.ndarray:
        """Transform the input text into its embedded vector representation.
        Args:
            X (str): Input text to be transformed.
        Returns:
            np.ndarray: Embedded vector representation of the input text.
        """
        return self.embed(X)

    def similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts.
        Args:
            text1 (str): First text.
            text2 (str): Second text.
        Returns:
            float: Cosine similarity between the embeddings of the two texts.
        """

        vec1 = self.embed(text1)
        vec2 = self.embed(text2)
        return self._cosine_similarity(vec1, vec2)
