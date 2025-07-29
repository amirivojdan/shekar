import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from shekar.embeddings.albert_embedder import AlbertEmbedder


@pytest.fixture
def mock_session():
    mock = MagicMock()
    mock.run.return_value = [
        np.random.random((1, 10, 768)),  # logits
        np.random.random((1, 10, 768)),  # last_hidden_state
    ]
    return mock


@pytest.fixture
def mock_tokenizer():
    mock = MagicMock()
    mock.return_value = {
        "input_ids": np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]),
        "attention_mask": np.array([[1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]),
        "token_type_ids": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    }
    return mock


class TestAlbertEmbedder:
    @patch("shekar.embeddings.albert_embedder.onnxruntime.InferenceSession")
    @patch("shekar.embeddings.albert_embedder.Hub.get_resource")
    @patch("shekar.embeddings.albert_embedder.AlbertTokenizer")
    def test_init_default_model_path(
        self, mock_tokenizer_class, mock_hub, mock_session_class
    ):
        # Setup
        mock_hub.return_value = "mock_model_path"
        mock_session_class.return_value = MagicMock()
        mock_tokenizer_class.return_value = MagicMock()

        # Execute
        embedder = AlbertEmbedder()

        # Assert
        mock_hub.assert_called_once_with(file_name="albert_persian_mlm_embeddings.onnx")
        mock_session_class.assert_called_once_with("mock_model_path")
        assert embedder.vector_size == 768

    @patch("shekar.embeddings.albert_embedder.onnxruntime.InferenceSession")
    @patch("shekar.embeddings.albert_embedder.Path.exists")
    @patch("shekar.embeddings.albert_embedder.AlbertTokenizer")
    def test_init_custom_model_path(
        self, mock_tokenizer_class, mock_exists, mock_session_class
    ):
        # Setup
        mock_exists.return_value = True
        mock_session_class.return_value = MagicMock()
        mock_tokenizer_class.return_value = MagicMock()

        # Execute
        embedder = AlbertEmbedder(model_path="custom_path")
        embedder.vector_size

        # Assert
        mock_exists.assert_called_once()
        mock_session_class.assert_called_once_with("custom_path")

    def test_embed(self, mock_session, mock_tokenizer):
        # Setup
        with (
            patch(
                "shekar.embeddings.albert_embedder.onnxruntime.InferenceSession",
                return_value=mock_session,
            ),
            patch(
                "shekar.embeddings.albert_embedder.AlbertTokenizer",
                return_value=mock_tokenizer,
            ),
            patch(
                "shekar.embeddings.albert_embedder.Hub.get_resource",
                return_value="mock_path",
            ),
        ):
            embedder = AlbertEmbedder()

            # Execute
            result = embedder.embed("test phrase")

            # Assert
            assert isinstance(result, np.ndarray)
            assert result.shape == (768,)
            assert result.dtype == np.float32
            mock_session.run.assert_called_once()
            mock_tokenizer.assert_called_once_with("test phrase")

    def test_embed_empty_input(self, mock_session, mock_tokenizer):
        # Setup
        with (
            patch(
                "shekar.embeddings.albert_embedder.onnxruntime.InferenceSession",
                return_value=mock_session,
            ),
            patch(
                "shekar.embeddings.albert_embedder.AlbertTokenizer",
                return_value=mock_tokenizer,
            ),
            patch(
                "shekar.embeddings.albert_embedder.Hub.get_resource",
                return_value="mock_path",
            ),
        ):
            embedder = AlbertEmbedder()

            # Execute
            result = embedder.embed("")

            # Assert
            assert isinstance(result, np.ndarray)
            assert result.shape == (768,)
