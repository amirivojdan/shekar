from shekar.base import BaseTransform
from .albert_sentiment_binary import AlbertBinarySentimentClassifier

SENTIMENT_REGISTRY = {
    "albert-binary": AlbertBinarySentimentClassifier,
}


class SentimentClassifier(BaseTransform):
    """A wrapper class for sentiment analysis models.
    Currently, it supports only the "albert-binary" model.
     Args:
        model (str): The sentiment analysis model to use. Default is "albert-binary".
        model_path (str, optional): Path to a custom model file. If None, the default model will be used.
    """

    def __init__(self, model: str = "albert-binary", model_path=None):
        model = model.lower()
        if model not in SENTIMENT_REGISTRY:
            raise ValueError(
                f"Unknown sentiment model '{model}'. Available: {list(SENTIMENT_REGISTRY.keys())}"
            )

        self.model = SENTIMENT_REGISTRY[model](model_path=model_path)

    def transform(self, X: str) -> tuple:
        """Perform sentiment analysis on the input text.
        Args:
            X (str): Input text.
            Returns:
                tuple: A tuple containing the predicted sentiment label and its confidence score.

        Example:
            >>> model = AlbertBinarySentimentClassifier()
            >>> model.transform("فیلم ۳۰۰ افتضاح بود.")
            ('negative', 0.998765468120575)
            >>> model.transform("سریال قصه‌های مجید عالی بود!")
            ('positive', 0.9976541996002197)
        """
        return self.model.transform(X)
