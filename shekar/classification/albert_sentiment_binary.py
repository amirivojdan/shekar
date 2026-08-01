from pathlib import Path

import numpy as np
import onnxruntime

from shekar.base import BaseTransform
from shekar.hub import Hub
from shekar.tokenization import AlbertTokenizer
from shekar.utils import get_onnx_providers


class AlbertBinarySentimentClassifier(BaseTransform):
    """Albert model for binary sentiment classification (positive/negative).
    This model is fine-tuned on the snapfood dataset.
     Args:
        model_path (str | Path, optional): Path to a custom model file. If None, the default model will be used.
    """

    def __init__(self, model_path: str | Path | None = None):
        super().__init__()
        resource_name = "albert_persian_sentiment_binary_q8.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = onnxruntime.InferenceSession(
            model_path, providers=get_onnx_providers()
        )
        self.tokenizer = AlbertTokenizer(enable_truncation=True)

        self.id2tag = {0: "negative", 1: "positive"}

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
        batched = self.tokenizer(X)  # dict with (num_chunks, L) arrays
        input_ids = batched["input_ids"]  # (B, L)
        attention_mask = batched["attention_mask"]  # (B, L)

        inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }
        outputs = self.session.run(None, inputs)
        logits = outputs[0]
        shifted_logits = logits - np.max(logits, axis=-1, keepdims=True)
        exponentials = np.exp(shifted_logits)
        scores = exponentials / exponentials.sum(axis=-1, keepdims=True)
        predicted_class = int(np.argmax(logits, axis=1)[0])
        predicted_class_score = float(scores[0, predicted_class])

        return (self.id2tag[predicted_class], predicted_class_score)
