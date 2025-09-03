from pathlib import Path
from typing import Optional, Dict, Any
import numpy as np
from tokenizers import Tokenizer
from shekar.base import BaseTransform
from shekar.hub import Hub


class AlbertTokenizer(BaseTransform):
    """
    Tokenize text with an ALBERT tokenizer and return fixed-length chunks.

    - Splits long inputs into multiple chunks of size `model_max_length`
    - Adds special tokens per tokenizer's post-processor
    - Returns stacked NumPy arrays ready for model input
    """

    def __init__(
        self,
        model_path: Optional[str | Path] = None,
        enable_padding: bool = False,
        enable_truncation: bool = False,
        stride: int = 0,
    ):
        super().__init__()
        resource_name = "albert_persian_tokenizer.json"

        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.tokenizer = Tokenizer.from_file(str(model_path))

        self.pad_token = "<pad>"
        self.unk_token = "<unk>"

        pad_id = self.tokenizer.token_to_id(self.pad_token)
        if pad_id is None:
            # Safely register a pad token if it was not present in the vocab
            self.tokenizer.add_special_tokens([self.pad_token])
            pad_id = self.tokenizer.token_to_id(self.pad_token)

        self.pad_token_id = pad_id
        self.unk_token_id = self.tokenizer.token_to_id(self.unk_token)
        self.model_max_length = 512
        self.stride = stride

        if enable_truncation:
            self.tokenizer.enable_truncation(
                max_length=self.model_max_length,
                stride=self.stride,
            )

        if enable_padding:
            self.tokenizer.enable_padding(
                length=self.model_max_length,
                pad_id=self.pad_token_id,
                pad_token=self.pad_token,
                pad_type_id=0,
                direction="right",
            )

    def transform(self, X: str) -> Dict[str, Any]:
        """
        Tokenize `X` into one or more chunks of size `model_max_length`.

        Args:
            X: Input text.

        Returns:
            dict with:
              - input_ids:    np.ndarray[int64] of shape (num_chunks, model_max_length)
              - attention_mask: np.ndarray[int64] of shape (num_chunks, model_max_length)
              - token_type_ids: np.ndarray[int64] of shape (num_chunks, model_max_length)
              - num_chunks:   int
        """

        first = self.tokenizer.encode(X)
        overflow = list(getattr(first, "overflowing", []))
        encodings = [first] + overflow

        input_ids = np.stack(
            [np.asarray(enc.ids, dtype=np.int64) for enc in encodings], axis=0
        )
        attention_mask = np.stack(
            [np.asarray(enc.attention_mask, dtype=np.int64) for enc in encodings],
            axis=0,
        )

        token_type_ids = np.stack(
            [np.asarray(enc.type_ids, dtype=np.int64) for enc in encodings], axis=0
        )

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids,
        }
