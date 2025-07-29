from pathlib import Path
import onnxruntime
import numpy as np

from shekar.hub import Hub
from .base import BaseEmbedder
from shekar.tokenization import AlbertTokenizer


class AlbertEmbedder(BaseEmbedder):
    def __init__(self, model_path: str | Path = None):
        super().__init__()
        resource_name = "albert_persian_mlm_embeddings.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = onnxruntime.InferenceSession(model_path)
        self.tokenizer = AlbertTokenizer()
        self.vector_size = 768

    def embed(self, phrase: str) -> np.ndarray:
        inputs = self.tokenizer(phrase)

        logits, last_hidden_state = self.session.run(None, inputs)
        attention_mask = inputs["attention_mask"][0][:, np.newaxis]
        masked_embeddings = last_hidden_state[0] * attention_mask
        sum_embeddings = masked_embeddings.sum(axis=0)
        valid_token_count = attention_mask.sum()
        mean_pooled_embedding = sum_embeddings / valid_token_count
        return mean_pooled_embedding.astype(np.float32)
