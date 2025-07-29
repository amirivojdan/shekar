from shekar.base import BaseTransform
from .word_tokenizer import WordTokenizer
from .sentence_tokenizer import SentenceTokenizer
from .albert_tokenizer import AlbertTokenizer

TOKENIZATION_REGISTRY = {
    "word": WordTokenizer,
    "sentence": SentenceTokenizer,
    "albert": AlbertTokenizer,
}


class Tokenizer(BaseTransform):
    def __init__(self, model: str = "word"):
        model = model.lower()
        if model not in TOKENIZATION_REGISTRY:
            raise ValueError(
                f"Unknown tokenizer model '{model}'. Available: {list(TOKENIZATION_REGISTRY.keys())}"
            )

        self.model = TOKENIZATION_REGISTRY[model]()

    def fit(self, X, y=None):
        return self.model.fit(X, y)

    def transform(self, X: str) -> str:
        return self.model.transform(X)
