from shekar.base import BaseTransform
from .albert_pos import AlbertPOS

POS_REGISTRY = {
    "albert": AlbertPOS,
}


class POSTagger(BaseTransform):
    def __init__(self, model: str = "albert", model_path=None):
        model = model.lower()
        if model not in POS_REGISTRY:
            raise ValueError(
                f"Unknown POS model '{model}'. Available: {list(POS_REGISTRY.keys())}"
            )

        self.model = POS_REGISTRY[model](model_path=model_path)

    def transform(self, X: str) -> list:
        return self.model.transform(X)
