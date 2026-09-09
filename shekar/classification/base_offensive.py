from shekar.base import BaseTransform

from .logistic_offensive_classifier import LogisticOffensiveClassifier

OFFENSIVE_REGISTRY = {
    "logistic": LogisticOffensiveClassifier,
}


class OffensiveLanguageClassifier(BaseTransform):
    supports_batching = True

    def __init__(self, model: str = "logistic", model_path=None, *, batch_size=32):
        self.batch_size = self._validate_batch_size(batch_size)
        model = model.lower()
        if model not in OFFENSIVE_REGISTRY:
            raise ValueError(
                f"Unknown model '{model}'. Available: {list(OFFENSIVE_REGISTRY.keys())}"
            )

        self.model = OFFENSIVE_REGISTRY[model](model_path=model_path)
        if getattr(self.model, "supports_batching", False) is True:
            self.model.batch_size = self.batch_size

    def transform(self, X: str):
        if not isinstance(X, str):
            return self.transform_batch(X)
        return self.model.transform(X)

    def _transform_batch(self, texts, batch_size):
        if getattr(self.model, "supports_batching", False) is True:
            return self.model.transform_batch(texts, batch_size=batch_size)
        return [self.model.transform(text) for text in texts]
