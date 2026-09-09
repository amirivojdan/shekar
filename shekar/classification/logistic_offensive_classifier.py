from pathlib import Path

import numpy as np

from shekar.base import BaseTransform
from shekar.hub import Hub
from shekar.preprocessing import StopWordRemover
from shekar.utils import create_onnx_session


class LogisticOffensiveClassifier(BaseTransform):
    """Logistic model for offensive language detection.
    This model is trained on Naseza(ناسزا) Persian offensive language dataset.
    Args:
        model_path (str | Path, optional): Path to a custom model file. If None, the default model will be used.

    Example:
        >>> model = LogisticOffensiveClassifier()
        >>> model.transform("این یک متن معمولی است.")
        ('neutral', 0.987654321)
        >>> model.transform("تو خیلی احمق و بی‌شرفی!")
        ('offensive', 0.9987654321)
    """

    supports_batching = True

    def __init__(self, model_path: str | Path | None = None, *, batch_size=32):
        super().__init__()
        self.batch_size = self._validate_batch_size(batch_size)
        resource_name = "tfidf_logistic_offensive.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = create_onnx_session(model_path)
        self._session_batch_size(self.session, self.batch_size)

        self.id2label = {0: "neutral", 1: "offensive"}
        self.stopword_remover = StopWordRemover()

    def transform(self, X: str) -> tuple:
        if not isinstance(X, str):
            return self.transform_batch(X)
        X = self.stopword_remover(X)

        in_name = self.session.get_inputs()[0].name
        out_names = [o.name for o in self.session.get_outputs()]
        arr = np.array([[X]], dtype=object)
        onnx_label, onnx_proba = self.session.run(out_names, {in_name: arr})

        if onnx_proba.ndim != 2:
            onnx_label, onnx_proba = onnx_proba, onnx_label

        return (self.id2label[onnx_label[0]], float(onnx_proba[0][onnx_label[0]]))

    def _transform_batch(self, texts, batch_size):
        size = self._session_batch_size(self.session, batch_size)
        results = []
        name = self.session.get_inputs()[0].name
        for start in range(0, len(texts), size):
            arr = np.array(
                [[self.stopword_remover(text)] for text in texts[start : start + size]],
                dtype=object,
            )
            labels, probabilities = self.session.run(None, {name: arr})
            if probabilities.ndim != 2:
                labels, probabilities = probabilities, labels
            results.extend(
                (self.id2label[int(label)], float(probabilities[i, int(label)]))
                for i, label in enumerate(labels)
            )
        return results
