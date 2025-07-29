import pytest
import numpy as np
from unittest.mock import Mock, patch
from shekar.embeddings.sentence_embedder import (
    SentenceEmbedder,
    SENTENCE_EMBEDDING_REGISTRY,
)


class TestSentenceEmbedder:
    def test_init_with_default_model(self):
        """Test initialization with default model."""
        embedder = SentenceEmbedder()
        assert isinstance(embedder.embedder, SENTENCE_EMBEDDING_REGISTRY["albert"])

    def test_init_with_uppercase_model_name(self):
        """Test initialization with uppercase model name."""
        embedder = SentenceEmbedder(model="ALBERT")
        assert isinstance(embedder.embedder, SENTENCE_EMBEDDING_REGISTRY["albert"])

    def test_init_with_invalid_model(self):
        """Test initialization with invalid model raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            SentenceEmbedder(model="nonexistent_model")

        assert "Unknown sentence embedding model" in str(excinfo.value)
        assert "Available: ['albert']" in str(excinfo.value)

    @patch("shekar.embeddings.sentence_embedder.SENTENCE_EMBEDDING_REGISTRY")
    def test_embed_calls_embedder(self, mock_registry):
        """Test that embed method calls the underlying embedder."""
        mock_embedder = Mock()
        mock_embedder.return_value = np.array([0.1, 0.2, 0.3])
        mock_registry.__getitem__.return_value = lambda: mock_embedder
        mock_registry.__contains__.return_value = True
        mock_registry.keys.return_value = ["albert"]

        embedder = SentenceEmbedder()
        result = embedder.embed("test phrase")

        mock_embedder.assert_called_once_with("test phrase")
        assert np.array_equal(result, np.array([0.1, 0.2, 0.3]))

    @patch("shekar.embeddings.sentence_embedder.SentenceEmbedder.embed")
    def test_transform_calls_embed(self, mock_embed):
        """Test that transform method calls the embed method."""
        mock_embed.return_value = np.array([0.4, 0.5, 0.6])

        embedder = SentenceEmbedder()
        result = embedder.transform("test sentence")

        mock_embed.assert_called_once_with("test sentence")
        assert np.array_equal(result, np.array([0.4, 0.5, 0.6]))
