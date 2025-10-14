from shekar.base import BaseTransform
from .logistic_offensive_classifier import LogisticOffensiveClassifier

POS_REGISTRY = {
    "logistic_offensive": LogisticOffensiveClassifier,
}


class OffensiveLanguageClassifier(BaseTransform):
    def __init__(self, model: str = "logistic_offensive", model_path=None):
        model = model.lower()
        if model not in POS_REGISTRY:
            raise ValueError(
                f"Unknown model '{model}'. Available: {list(POS_REGISTRY.keys())}"
            )

        self.model = POS_REGISTRY[model](model_path=model_path)

    def transform(self, X: str) -> list:
        return self.model.transform(X)
