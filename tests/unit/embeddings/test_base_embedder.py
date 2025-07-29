import numpy as np
import pytest


from shekar.embeddings.base import BaseEmbedder


class DummyEmbedder(BaseEmbedder):
    """A tiny concrete embedder for testing."""

    def __init__(self, table=None, dim=3):
        self.table = table or {}
        self.dim = dim
        self.calls = 0

    def embed(self, text: str) -> np.ndarray:
        self.calls += 1
        vec = self.table.get(text)
        if vec is None:
            return np.zeros(self.dim, dtype=np.float32)
        return np.asarray(vec, dtype=np.float32)

    def transform(self, X):
        """Dummy implementation required by BaseTransform."""
        if isinstance(X, str):
            return self.embed(X)
        return [self.embed(x) for x in X]


def test_base_embedder_is_abstract():
    with pytest.raises(TypeError):
        BaseEmbedder()


@pytest.mark.parametrize(
    "v1, v2, expected",
    [
        (np.array([1.0, 0.0]), np.array([1.0, 0.0]), 1.0),  # identical
        (np.array([1.0, 0.0]), np.array([0.0, 1.0]), 0.0),  # orthogonal
        (
            np.array([1.0, 1.0]),
            np.array([2.0, 2.0]),
            1.0,
        ),  # same direction different magnitude
    ],
)
def test_cosine_similarity_basic(v1, v2, expected):
    e = DummyEmbedder()
    got = e._cosine_similarity(v1, v2)
    assert np.isclose(got, expected, atol=1e-7)


def test_cosine_similarity_with_zero_vector_returns_0():
    e = DummyEmbedder()
    v1 = np.array([0.0, 0.0])
    v2 = np.array([1.0, 0.0])
    assert e._cosine_similarity(v1, v2) == 0.0
    assert e._cosine_similarity(v2, v1) == 0.0


@pytest.mark.parametrize(
    "v1, v2",
    [
        (None, np.array([1.0, 0.0])),
        (np.array([1.0, 0.0]), None),
        (None, None),
        ([1.0, 0.0], np.array([1.0, 0.0])),
    ],
)
def test_cosine_similarity_invalid_inputs_return_0(v1, v2):
    e = DummyEmbedder()
    assert e._cosine_similarity(v1, v2) == 0.0


def test_similarity_uses_embed_and_returns_expected_value():
    table = {
        "a": np.array([1.0, 0.0, 0.0]),
        "b": np.array([0.0, 1.0, 0.0]),
        "c": np.array([1.0, 0.0, 0.0]),
    }
    e = DummyEmbedder(table=table, dim=3)

    # a vs c should be 1.0, a vs b should be 0.0
    assert np.isclose(e.similarity("a", "c"), 1.0)
    assert np.isclose(e.similarity("a", "b"), 0.0)

    # OOV vs a -> zero vector vs a -> 0.0
    assert np.isclose(e.similarity("oov", "a"), 0.0)

    # embed must have been called twice for each similarity call
    # 3 similarity calls * 2 = 6
    assert e.calls == 6


def test_similarity_returns_float():
    table = {"hello": np.array([1.0, 2.0, 3.0])}
    e = DummyEmbedder(table=table, dim=3)
    sim = e.similarity("hello", "hello")
    assert isinstance(sim, float)
