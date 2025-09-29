import numpy as np
from shekar.embeddings.albert_embedder import AlbertEmbedder


class TestAlbertEmbedder:
    def test_init_with_default_path(self):
        embedder = AlbertEmbedder()
        assert embedder.session is not None
        assert embedder.tokenizer is not None
        assert embedder.vector_size == 768

    def test_init_with_custom_path(self):
        # This will fall back to Hub.get_resource since path doesn't exist
        embedder = AlbertEmbedder(model_path="nonexistent_path.onnx")
        assert embedder.session is not None
        assert embedder.tokenizer is not None
        assert embedder.vector_size == 768

    def test_embed_single_word(self):
        embedder = AlbertEmbedder()
        result = embedder.embed("سلام")
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float32
        assert result.shape == (768,)

    def test_embed_sentence(self):
        embedder = AlbertEmbedder()
        result = embedder.embed("سلام دنیا چطوری؟")
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float32
        assert result.shape == (768,)

    def test_embed_empty_string(self):
        embedder = AlbertEmbedder()
        result = embedder.embed("")
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float32
        assert result.shape == (768,)

    def test_embed_long_text(self):
        embedder = AlbertEmbedder()
        long_text = "این یک متن طولانی است. " * 50
        result = embedder.embed(long_text)
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float32
        assert result.shape == (768,)

    def test_embed_consistency(self):
        embedder = AlbertEmbedder()
        text = "تست پایداری"
        result1 = embedder.embed(text)
        result2 = embedder.embed(text)
        np.testing.assert_array_equal(result1, result2)

    def test_embed_different_inputs_different_outputs(self):
        embedder = AlbertEmbedder()
        result1 = embedder.embed("متن اول")
        result2 = embedder.embed("متن دوم")
        assert not np.array_equal(result1, result2)

    def test_vector_size_property(self):
        embedder = AlbertEmbedder()
        assert embedder.vector_size == 768
        assert isinstance(embedder.vector_size, int)
