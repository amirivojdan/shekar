from shekar.base import BaseTransform
from .albert import AlbertNER

NER_REGISTRY = {
    "albert": AlbertNER,
}

class NER(BaseTransform):
    def __init__(self, model_name: str = "albert", model_path=None):
        model_name = model_name.lower()
        if model_name not in NER_REGISTRY:
            raise ValueError(f"Unknown NER model '{model_name}'. Available: {list(NER_REGISTRY.keys())}")
        
        self.model = NER_REGISTRY[model_name](model_path=model_path)

    def fit(self, X, y=None):
        return self.model.fit(X, y)

    def transform(self, X: str) -> list:
        return self.model.transform(X)
