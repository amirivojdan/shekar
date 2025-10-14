from shekar.base import BaseTransform
from .logistic_offensive_classifier import LogisticOffensiveClassifier

OFFENSIVE_REGISTRY = {
    "logistic": LogisticOffensiveClassifier,
}


class OffensiveLanguageClassifier(BaseTransform):
    def __init__(self, model: str = "logistic", model_path=None):
        model = model.lower()
        if model not in OFFENSIVE_REGISTRY:
            raise ValueError(
                f"Unknown model '{model}'. Available: {list(OFFENSIVE_REGISTRY.keys())}"
            )

        self.model = OFFENSIVE_REGISTRY[model](model_path=model_path)

    def transform(self, X: str):
        return self.model.transform(X)
