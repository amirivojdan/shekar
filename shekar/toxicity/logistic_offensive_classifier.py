from shekar.base import BaseTransform
from shekar.hub import Hub
from pathlib import Path
import onnxruntime
import numpy as np
from shekar.utils import get_onnx_providers
from shekar.preprocessing import StopWordRemover


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

    def __init__(self, model_path: str | Path = None):
        super().__init__()
        resource_name = "tfidf_logistic_offensive.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = onnxruntime.InferenceSession(
            model_path, providers=get_onnx_providers()
        )

        self.id2label = {0: "neutral", 1: "offensive"}
        self.stopword_remover = StopWordRemover()

    def transform(self, X: str) -> tuple:
        X = self.stopword_remover(X)

        in_name = self.session.get_inputs()[0].name
        out_names = [o.name for o in self.session.get_outputs()]
        arr = np.array([[X]], dtype=object)
        onnx_label, onnx_proba = self.session.run(out_names, {in_name: arr})

        if onnx_proba.ndim != 2:
            onnx_label, onnx_proba = onnx_proba, onnx_label

        return (self.id2label[onnx_label[0]], float(onnx_proba[0][onnx_label[0]]))
