from pathlib import Path

import numpy as np

from shekar.base import BaseTransform
from shekar.hub import Hub
from shekar.tokenization import AlbertTokenizer
from shekar.utils import create_onnx_session


class AlbertBinarySentimentClassifier(BaseTransform):
    """Albert model for binary sentiment classification (positive/negative).
    This model is fine-tuned on the snapfood dataset.
     Args:
        model_path (str | Path, optional): Path to a custom model file. If None, the default model will be used.
    """

    supports_batching = True

    def __init__(self, model_path: str | Path | None = None, *, batch_size=32):
        super().__init__()
        self.batch_size = self._validate_batch_size(batch_size)
        resource_name = "albert_persian_sentiment_binary_q8.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = create_onnx_session(model_path)
        self._session_batch_size(self.session, self.batch_size)
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
        if not isinstance(X, str):
            return self.transform_batch(X)
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

    def _transform_batch(self, texts, batch_size):
        results = []
        size = self._session_batch_size(self.session, batch_size)
        encoded = (self.tokenizer(text) for text in texts)
        for inputs, owners in AlbertTokenizer._encoded_batches(
            encoded, size, self.tokenizer.pad_token_id
        ):
            logits = self.session.run(
                None, {k: inputs[k] for k in ("input_ids", "attention_mask")}
            )[0]
            shifted = logits - logits.max(axis=-1, keepdims=True)
            scores = np.exp(shifted)
            scores /= scores.sum(axis=-1, keepdims=True)
            for row, predicted in enumerate(logits.argmax(axis=-1)):
                results.append(
                    (self.id2tag[int(predicted)], float(scores[row, predicted]))
                )
        return results
