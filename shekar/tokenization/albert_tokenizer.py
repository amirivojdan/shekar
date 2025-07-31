from pathlib import Path
from shekar.base import BaseTransform
from shekar.hub import Hub
from tokenizers import Tokenizer
import numpy as np


class AlbertTokenizer(BaseTransform):
    """
    A class used to tokenize text using the ALBERT tokenizer.
    """

    def __init__(self, model_path: str | Path = None):
        super().__init__()
        resource_name = "albert_persian_tokenizer.json"

        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.tokenizer = Tokenizer.from_file(str(model_path))
        self.pad_token_id = self.tokenizer.token_to_id("<pad>")
        self.unk_token_id = self.tokenizer.token_to_id("<unk>")
        self.model_max_length = 512

    def transform(self, X: str) -> dict:
        """
        Tokenize a batch of texts using the ALBERT tokenizer.

        Args:
            X (str): The input text to be tokenized.
        Returns:
            dict: A dictionary containing tokenized inputs with keys 'input_ids', 'attention_mask',
            and 'token_type_ids'.
        """

        encoding = self.tokenizer.encode(X)

        input_ids = np.array([encoding.ids], dtype=np.int64)
        attention_mask = np.array([encoding.attention_mask], dtype=np.int64)
        token_type_ids = np.zeros_like(input_ids, dtype=np.int64)

        tokenized_inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids,
        }

        return tokenized_inputs
