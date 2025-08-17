from shekar.base import BaseTextTransform
from shekar import data
import re


class Stemmer(BaseTextTransform):
    """
    This class implements a simple stemming algorithm for Persian words.
    It removes suffixes from words to obtain their root forms.

    Example:
        >>> stemmer = Stemmer()
        >>> stemmer("کتاب‌ها")
        "کتاب"
        >>> stemmer("نوه‌ام")
        "نوه"

    """

    def __init__(self):
        super().__init__()

        ZWNJ = re.escape(data.ZWNJ)
        NLJ_CLASS = "[" + "".join(map(re.escape, data.non_left_joiner_letters)) + "]"

        self._mappings = [
            # possessive clitics: remove if joined by ZWNJ or base ends with a non-left-joiner
            (rf"(?:(?:{ZWNJ})|(?<={NLJ_CLASS}))(?:مان|تان|ام|ات|شان)$", ""),
            (rf"(?:{ZWNJ})?(?:م|ت|ش)$", ""),
            # plurals: remove if joined by ZWNJ or base ends with a non-left-joiner
            (rf"(?:(?:{ZWNJ})|(?<={NLJ_CLASS}))(?:هایی|های|ها)$", ""),
            # comparative/superlative: only when explicitly joined with ZWNJ or hyphen
            (rf"(?:{ZWNJ})(?:ترین|تر)$", ""),
            # ezafe after vowel or heh written as ZWNJ + ی / یی; be conservative, do not strip bare 'ی'
            (rf"{ZWNJ}(?:ی|یی)$", ""),
        ]

        self._patterns = self._compile_patterns(self._mappings)

    def _function(self, text: str) -> str:
        if text not in data.vocab:
            return self._map_patterns(text, self._patterns)
        return text
