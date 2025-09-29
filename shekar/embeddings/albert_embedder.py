from pathlib import Path
import onnxruntime
import numpy as np
from shekar.hub import Hub
from .base import BaseEmbedder
from shekar.tokenization import AlbertTokenizer
from shekar.utils import get_onnx_providers


class AlbertEmbedder(BaseEmbedder):
    def __init__(self, model_path: str | Path = None):
        super().__init__()
        resource_name = "albert_persian_mlm_embeddings.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)
        self.session = onnxruntime.InferenceSession(
            model_path, providers=get_onnx_providers()
        )
        self.tokenizer = AlbertTokenizer(enable_padding=True, enable_truncation=True)
        self.vector_size = 768

    def embed(self, phrase: str) -> np.ndarray:
        inputs = self.tokenizer(phrase)

        logits, last_hidden_state = self.session.run(None, inputs)

        mask = inputs["attention_mask"].astype(last_hidden_state.dtype)[:, :, None]

        # drop special tokens
        # if "input_ids" in inputs:
        #     ids = inputs["input_ids"]
        #     for tid in [cls_id, sep_id]:  # define these ids if available
        #         if tid is not None:
        #             mask[ids == tid] = 0

        sum_all = (last_hidden_state * mask).sum(axis=(0, 1))  # (H,)
        count = np.clip(mask.sum(), 1e-9, None)  # scalar

        return (sum_all / count).astype(np.float32)
