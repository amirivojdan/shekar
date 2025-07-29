from shekar.base import BaseTransform
from .rake import RAKE

KEYWORD_EXTRACTION_REGISTRY = {
    "rake": RAKE,
}


class KeywordExtractor(BaseTransform):
    def __init__(self, model: str = "rake", max_length=3, top_n=5):
        model = model.lower()
        if model not in KEYWORD_EXTRACTION_REGISTRY:
            raise ValueError(
                f"Unknown keyword extraction model '{model}'. Available: {list(KEYWORD_EXTRACTION_REGISTRY.keys())}"
            )

        self.model = KEYWORD_EXTRACTION_REGISTRY[model](
            max_length=max_length, top_n=top_n
        )

    def fit(self, X, y=None):
        return self.model.fit(X, y)

    def transform(self, X: str) -> list:
        return self.model.transform(X)
