from pathlib import Path

import onnxruntime as ort

from shekar.transliteration.byt5_tokenizer import ByT5Tokenizer
from shekar.utils import create_onnx_session


class ByT5Encoder:
    def __init__(self, model_path: str | Path):
        self._session = self._make_session(Path(model_path))
        self.tokenizer = ByT5Tokenizer()

    @staticmethod
    def _make_session(path: Path) -> ort.InferenceSession:
        so = ort.SessionOptions()
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        return create_onnx_session(path, sess_options=so)

    def encode(self, text: str) -> tuple:
        return self.encode_batch([text])

    def encode_batch(self, texts) -> tuple:
        input_ids, attention_mask = self.tokenizer.batch_tokenize(texts)
        hidden_states = self._session.run(
            ["last_hidden_state"],
            {"input_ids": input_ids, "attention_mask": attention_mask},
        )[0]
        return hidden_states, attention_mask
