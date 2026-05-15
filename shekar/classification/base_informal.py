from shekar.base import BaseTransform
from .informal_rule_based import RuleBasedInformalClassifier

INFORMAL_REGISTRY = {
    "rule_based": RuleBasedInformalClassifier,
}


class InformalLanguageClassifier(BaseTransform):
    def __init__(self, model: str = "rule_based", model_path=None):
        model = model.lower()
        if model not in INFORMAL_REGISTRY:
            raise ValueError(
                f"Unknown model '{model}'. Available: {list(INFORMAL_REGISTRY.keys())}"
            )

        self.model = INFORMAL_REGISTRY[model](model_path=model_path)

    def transform(self, X: str):
        return self.model.transform(X)
