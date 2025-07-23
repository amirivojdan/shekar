from shekar.base import BaseTransform
from .statistical import StatisticalSpellChecker

SPELL_CHECKING_REGISTRY = {
    "statistical": StatisticalSpellChecker,
}

class SpellChecker(BaseTransform):
    def __init__(self, model: str = "statistical", model_path=None):
        model = model.lower()
        if model not in SPELL_CHECKING_REGISTRY:
            raise ValueError(f"Unknown spell checking model '{model}'. Available: {list(SPELL_CHECKING_REGISTRY.keys())}")

        self.model = SPELL_CHECKING_REGISTRY[model](model_path=model_path)

    def fit(self, X, y=None):
        return self.model.fit(X, y)

    def transform(self, X: str) -> str:
        return self.model.transform(X)
