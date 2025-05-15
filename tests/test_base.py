# test_base_transformer.py
import pytest
from shekar.base import BaseTransformer


# Covers the abstract NotImplementedError lines directly
def test_transform_abstract_error():
    with pytest.raises(NotImplementedError):
        BaseTransformer.transform(None, [1, 2, 3])  # directly call on class


def test_fit_abstract_error():
    with pytest.raises(NotImplementedError):
        BaseTransformer.fit(None, [1, 2, 3])  # directly call on class


# Covers fit_transform and __call__ via a concrete subclass
class DummyTransformer(BaseTransformer):
    def fit(self, X, y=None):
        self.was_fitted = True
        return self

    def transform(self, X):
        assert hasattr(self, "was_fitted")
        return X


def test_fit_transform_works():
    d = DummyTransformer()
    out = d.fit_transform([1, 2, 3])
    assert out == [1, 2, 3]


def test_call_works():
    d = DummyTransformer()
    out = d([4, 5, 6])
    assert out == [4, 5, 6]
