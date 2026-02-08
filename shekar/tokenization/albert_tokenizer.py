from pathlib import Path
from typing import Optional, Dict, Any, List
import numpy as np
import sentencepiece as spm

from shekar.base import BaseTransform
from shekar.hub import Hub


class _Encoding:
    def __init__(self, tokens, ids):
        self.tokens = tokens
        self.ids = ids


class AlbertTokenizer(BaseTransform):
    """
    ALBERT-compatible tokenizer backed by SentencePiece (.model).

    - Splits long inputs into fixed-length chunks
    - Adds [CLS] and [SEP]
    - Pads to model_max_length if enabled
    - Returns NumPy arrays identical to the HF tokenizer output
    """

    def __init__(
        self,
        model_path: Optional[str | Path] = None,
        enable_padding: bool = False,
        enable_truncation: bool = False,
        stride: int = 0,
        model_max_length: int = 512,
    ):
        super().__init__()

        resource_name = "albert_persian_tokenizer.model"

        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.sp = spm.SentencePieceProcessor()
        self.sp.load(str(model_path))

        self.model_max_length = model_max_length
        self.stride = stride
        self.enable_padding = enable_padding
        self.enable_truncation = enable_truncation

        # Special tokens
        self.pad_token = "<pad>"
        self.unk_token = "<unk>"
        self.cls_token = "<cls>"
        self.sep_token = "<sep>"

        self.pad_token_id = self._require_token(self.pad_token)
        self.unk_token_id = self._require_token(self.unk_token)
        self.cls_token_id = self._require_token(self.cls_token)
        self.sep_token_id = self._require_token(self.sep_token)

    def _require_token(self, token: str) -> int:
        tid = self.sp.piece_to_id(token)
        if tid < 0:
            raise ValueError(
                f"Required token missing from SentencePiece model: {token}"
            )
        return tid

    def encode(self, text: str, add_special_tokens: bool = True):
        # SentencePiece pieces (strings)
        pieces = self.sp.encode(text, out_type=str)
        ids = self.sp.encode(text, out_type=int)

        if add_special_tokens:
            pieces = ["[CLS]"] + pieces + ["[SEP]"]
            ids = [self.cls_token_id] + ids + [self.sep_token_id]

        return _Encoding(tokens=pieces, ids=ids)

    def _chunk_ids(self, ids: List[int]) -> List[List[int]]:
        """
        Chunk token ids into model_max_length windows with optional stride.
        Accounts for [CLS] and [SEP].
        """
        max_body_len = self.model_max_length - 2
        chunks = []

        start = 0
        while start < len(ids):
            end = start + max_body_len
            body = ids[start:end]

            chunk = [self.cls_token_id] + body + [self.sep_token_id]
            chunks.append(chunk)

            if not self.enable_truncation:
                break

            if end >= len(ids):
                break

            start = end - self.stride if self.stride > 0 else end

        return chunks

    def _pad(self, ids: List[int]) -> List[int]:
        if len(ids) >= self.model_max_length:
            return ids[: self.model_max_length]

        pad_len = self.model_max_length - len(ids)
        return ids + [self.pad_token_id] * pad_len

    def token_to_id(self, token: str) -> int | None:
        tid = self.sp.piece_to_id(token)
        return tid if tid >= 0 else None

    def id_to_token(self, idx: int) -> str:
        return self.sp.id_to_piece(idx)

    @property
    def tokenizer(self):
        return self

    def transform(self, X: str) -> Dict[str, Any]:
        if X == "" or X.strip() == "":
            ids = [self.cls_token_id, self.sep_token_id]

            padded = ids + [self.pad_token_id] * (self.model_max_length - len(ids))
            mask = [1, 1] + [0] * (self.model_max_length - 2)

            return {
                "input_ids": np.asarray([padded], dtype=np.int64),
                "attention_mask": np.asarray([mask], dtype=np.int64),
                "token_type_ids": np.zeros((1, self.model_max_length), dtype=np.int64),
            }

        # Encode without special tokens
        ids = self.sp.encode(X, out_type=int)

        chunks = self._chunk_ids(ids)

        input_ids = []
        attention_mask = []
        token_type_ids = []

        for chunk in chunks:
            if self.enable_padding:
                padded = self._pad(chunk)
                mask = [1] * len(chunk) + [0] * (self.model_max_length - len(chunk))
            else:
                padded = chunk
                mask = [1] * len(chunk)

            input_ids.append(padded)
            attention_mask.append(mask)
            token_type_ids.append([0] * len(padded))

        return {
            "input_ids": np.asarray(input_ids, dtype=np.int64),
            "attention_mask": np.asarray(attention_mask, dtype=np.int64),
            "token_type_ids": np.asarray(token_type_ids, dtype=np.int64),
        }
