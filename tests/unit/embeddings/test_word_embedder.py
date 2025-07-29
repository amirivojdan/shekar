import pytest
import numpy as np
import pickle

from shekar.embeddings.word_embedder import WordEmbedder


@pytest.fixture
def dummy_model_path(tmp_path):
    """Create a dummy embedding model pickle file for testing."""
    model_data = {
        "words": ["سیب", "موز", "هلو"],
        "embeddings": np.array(
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]], dtype=np.float32
        ),
        "vector_size": 3,
        "window": 5,
        "model": "fasttext",
        "epochs": 10,
        "dataset": "dummy",
    }
    file_path = tmp_path / "dummy_model.pkl"
    with open(file_path, "wb") as f:
        pickle.dump(model_data, f)
    return file_path


def test_invalid_model_name_raises():
    with pytest.raises(ValueError):
        WordEmbedder(model="unknown-model")


def test_embed_known_token(dummy_model_path):
    we = WordEmbedder(model="fasttext-d100", model_path=dummy_model_path)
    vec = we.embed("سیب")
    assert isinstance(vec, np.ndarray)
    assert np.allclose(vec, np.array([1.0, 0.0, 0.0], dtype=np.float32))


@pytest.mark.parametrize("oov_strategy", ["zero", "none", "error"])
def test_embed_oov_strategies(dummy_model_path, oov_strategy):
    we = WordEmbedder(
        model="fasttext-d100", model_path=dummy_model_path, oov_strategy=oov_strategy
    )
    token = "ناشناخته"
    if oov_strategy == "zero":
        vec = we.embed(token)
        assert isinstance(vec, np.ndarray)
        assert np.allclose(vec, np.zeros(3))
    elif oov_strategy == "none":
        assert we.embed(token) is None
    elif oov_strategy == "error":
        with pytest.raises(KeyError):
            we.embed(token)


def test_transform_is_alias_of_embed(dummy_model_path):
    we = WordEmbedder(model="fasttext-d100", model_path=dummy_model_path)
    token = "موز"
    assert np.allclose(we.transform(token), we.embed(token))


def test_similarity_between_tokens(dummy_model_path):
    we = WordEmbedder(model="fasttext-d100", model_path=dummy_model_path)
    sim = we.similarity("سیب", "هلو")
    # Cosine similarity of [1,0,0] and [1,1,0] is 1 / sqrt(2)
    assert np.isclose(sim, 1 / np.sqrt(2), atol=1e-6)


def test_most_similar_returns_sorted_list(dummy_model_path):
    we = WordEmbedder(model="fasttext-d100", model_path=dummy_model_path)
    result = we.most_similar("سیب", top_n=2)
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
    # Ensure it's sorted by similarity
    sims = [s for _, s in result]
    assert sims == sorted(sims, reverse=True)
    # Check top_n limit
    assert len(result) == 2


def test_most_similar_empty_for_oov(dummy_model_path):
    we = WordEmbedder(
        model="fasttext-d100", model_path=dummy_model_path, oov_strategy="none"
    )
    assert we.most_similar("ناشناخته") == []
