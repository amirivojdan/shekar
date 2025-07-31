from shekar.base import BaseTransform
from .albert_ner import AlbertNER

NER_REGISTRY = {
    "albert": AlbertNER,
}


class NER(BaseTransform):
    def __init__(self, model: str = "albert", model_path=None):
        model = model.lower()
        if model not in NER_REGISTRY:
            raise ValueError(
                f"Unknown NER model '{model}'. Available: {list(NER_REGISTRY.keys())}"
            )

        self.model = NER_REGISTRY[model](model_path=model_path)

    def transform(self, X: str) -> list:
        return self.model.transform(X)
