# test_base_transformer.py
import pytest
from shekar.base import BaseTransform
from shekar.pipeline import Pipeline


# Covers the abstract NotImplementedError lines directly
def test_transform_abstract_error():
    with pytest.raises(NotImplementedError):
        BaseTransform.transform(None, [1, 2, 3])  # directly call on class


# Covers fit_transform and __call__ via a concrete subclass
class DummyTransformer(BaseTransform):
    def fit(self, X, y=None):
        self.was_fitted = True
        return self

    def transform(self, X):
        assert hasattr(self, "was_fitted")
        return X


class DummyTransformerA(BaseTransform):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


class DummyTransformerB(BaseTransform):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


def test_fit_transform_works():
    d = DummyTransformer()
    out = d.fit_transform([1, 2, 3])
    assert out == [1, 2, 3]


def test_call_works():
    d = DummyTransformer()
    out = d([4, 5, 6])
    assert out == [4, 5, 6]


def test_or_with_pipeline():
    d1 = DummyTransformerA()
    d2 = DummyTransformerB()
    pipe = Pipeline(steps=[("DummyTransformerB", d2)])
    combined_pipe = d1 | pipe
    assert isinstance(combined_pipe, Pipeline)
    assert combined_pipe.steps[0][0] == "DummyTransformerA"
    assert isinstance(combined_pipe.steps[0][1], DummyTransformerA)
    assert combined_pipe.steps[1][0] == "DummyTransformerB"
    assert isinstance(combined_pipe.steps[1][1], DummyTransformerB)


def test_or_with_transformer():
    d1 = DummyTransformerA()
    d2 = DummyTransformerB()
    combined_pipe = d1 | d2
    assert isinstance(combined_pipe, Pipeline)
    assert combined_pipe.steps[0][0] == "DummyTransformerA"
    assert isinstance(combined_pipe.steps[0][1], DummyTransformerA)
    assert combined_pipe.steps[1][0] == "DummyTransformerB"
    assert isinstance(combined_pipe.steps[1][1], DummyTransformerB)


def test_or_with_invalid_type():
    d1 = DummyTransformerA()
    with pytest.raises(TypeError):
        _ = d1 | 123  # not a Pipeline or BaseTransformer
