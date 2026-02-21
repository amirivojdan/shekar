from shekar.base import BaseTextTransform
from shekar import data
import string


class NonPersianLetterMasker(BaseTextTransform):
    def __init__(self, keep_english=False, keep_diacritics=False):
        super().__init__()

        allowed_chars = set(
            data.persian_letters + data.spaces + data.persian_digits + data.punctuations
        )

        if keep_diacritics:
            allowed_chars.update(data.diacritics)

        if keep_english:
            allowed_chars.update(
                string.ascii_letters + string.digits + string.punctuation
            )

        self._translation_table = {
            i: None for i in range(0x110000) if chr(i) not in allowed_chars
        }

    def _function(self, text: str) -> str:
        return text.translate(self._translation_table).strip()
