from functools import lru_cache
import re
import string

from shekar import data
from shekar.base import BaseTextTransform


class NonPersianLetterMasker(BaseTextTransform):
    def __init__(self, keep_english=False, keep_diacritics=False):
        super().__init__()
        self._disallowed_pattern = self._get_disallowed_pattern(
            keep_english,
            keep_diacritics,
        )

    @staticmethod
    @lru_cache(maxsize=4)
    def _get_disallowed_pattern(
        keep_english: bool,
        keep_diacritics: bool,
    ) -> re.Pattern:
        allowed_chars = (
            data.persian_letters + data.spaces + data.persian_digits + data.punctuations
        )

        if keep_diacritics:
            allowed_chars += data.diacritics

        if keep_english:
            allowed_chars += string.ascii_letters + string.digits + string.punctuation

        return re.compile(f"[^{re.escape(allowed_chars)}]+")

    def _function(self, text: str) -> str:
        return self._disallowed_pattern.sub("", text).strip()
