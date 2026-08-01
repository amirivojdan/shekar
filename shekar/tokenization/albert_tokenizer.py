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

    - Optionally truncates long inputs to ``model_max_length``
    - Optionally returns truncated content as overlapping windows
    - Adds [CLS] and [SEP]
    - Pads to model_max_length if enabled
    - Returns dense NumPy arrays

    When multiple overflow windows are returned, the final shorter window is
    padded even if ``enable_padding`` is false. This keeps the returned batch
    rectangular and representable as a NumPy array.
    """

    def __init__(
        self,
        model_path: Optional[str | Path] = None,
        enable_padding: bool = False,
        enable_truncation: bool = False,
        stride: int = 0,
        model_max_length: int = 512,
        return_overflowing_tokens: bool = False,
    ):
        super().__init__()

        if (
            not isinstance(model_max_length, int)
            or isinstance(model_max_length, bool)
            or model_max_length <= 2
        ):
            raise ValueError("model_max_length must be an integer greater than 2.")

        max_body_len = model_max_length - 2
        if (
            not isinstance(stride, int)
            or isinstance(stride, bool)
            or not 0 <= stride < max_body_len
        ):
            raise ValueError(
                "stride must be an integer in the range "
                f"[0, {max_body_len - 1}] for model_max_length={model_max_length}."
            )

        if return_overflowing_tokens and not enable_truncation:
            raise ValueError(
                "return_overflowing_tokens=True requires enable_truncation=True."
            )

        if stride and not return_overflowing_tokens:
            raise ValueError("stride is only used when return_overflowing_tokens=True.")

        resource_name = "albert_persian_tokenizer.model"

        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.sp = spm.SentencePieceProcessor()
        self.sp.load(str(model_path))

        self.model_max_length = model_max_length
        self.stride = stride
        self.enable_padding = enable_padding
        self.enable_truncation = enable_truncation
        self.return_overflowing_tokens = return_overflowing_tokens

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
        Add special tokens and apply the configured long-input policy.

        With truncation disabled, a single sequence of any length is returned.
        With truncation enabled, the sequence is capped at model_max_length.
        Additional overlapping windows are only returned when requested.
        """
        max_body_len = self.model_max_length - 2

        if not self.enable_truncation or len(ids) <= max_body_len:
            return [[self.cls_token_id, *ids, self.sep_token_id]]

        first_chunk = [
            self.cls_token_id,
            *ids[:max_body_len],
            self.sep_token_id,
        ]
        if not self.return_overflowing_tokens:
            return [first_chunk]

        chunks = []
        step = max_body_len - self.stride

        for start in range(0, len(ids), step):
            body = ids[start : start + max_body_len]
            chunks.append([self.cls_token_id, *body, self.sep_token_id])

            if start + max_body_len >= len(ids):
                break

        return chunks

    def _pad(self, ids: List[int], target_length: int) -> List[int]:
        pad_len = target_length - len(ids)
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
        # Encode without special tokens
        ids = self.sp.encode(X, out_type=int)

        chunks = self._chunk_ids(ids)
        pad_batch = self.enable_padding or len(chunks) > 1
        target_length = max(len(chunk) for chunk in chunks)
        if self.enable_padding:
            target_length = max(target_length, self.model_max_length)

        input_ids = []
        attention_mask = []
        token_type_ids = []

        for chunk in chunks:
            if pad_batch:
                padded = self._pad(chunk, target_length)
                mask = [1] * len(chunk) + [0] * (target_length - len(chunk))
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
