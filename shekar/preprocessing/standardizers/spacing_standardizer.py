from shekar.base import BaseTextTransform
import re


class SpacingStandardizer(BaseTextTransform):
    """
    Standardizes spacing in the text regarding the offical Persian script standard published by the Iranian Academy of Language and Literature.
    reference: https://apll.ir/
    This class is also used to remove extra spaces, newlines, zero width nonjoiners, and other unicode space characters.
    """

    def __init__(self):
        super().__init__()
        self._spacing_mappings = [
            (r" {2,}", " "),  # remove extra spaces
            (r"\n{3,}", "\n\n"),  # remove extra newlines
            (r"\u200c{2,}", "\u200c"),  # remove extra ZWNJs
            (r"\u200c{1,} ", " "),  # remove ZWNJs before space
            (r" \u200c{1,}", " "),  # remove ZWNJs after space
            (r"\b\u200c*\B", ""),  # remove ZWNJs at the beginning of words
            (r"\B\u200c*\b", ""),  # remove ZWNJs at the end of words
            (
                r"[\u200b\u200d\u200e\u200f\u2066\u2067\u202a\u202b\u202d]",
                "",
            ),  # remove other unicode space characters
        ]

        self._patterns = self._compile_patterns(self._spacing_mappings)

    def _function(self, text: str) -> str:
        # A POS tagger is needed to identify part of speech tags in the text.

        text = re.sub(r"^(بی|می|نمی)( )", r"\1‌", text)  # verb_prefix
        text = re.sub(r"( )(می|نمی)( )", r"\1\2‌ ", text)  # verb_prefix
        text = re.sub(r"([^ ]ه) ی ", r"\1‌ی ", text)

        return self._map_patterns(text, self._patterns).strip()
