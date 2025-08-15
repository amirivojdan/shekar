from typing import Iterable
from shekar import Pipeline
from shekar.preprocessing import (
    PunctuationNormalizer,
    AlphabetNormalizer,
    DigitNormalizer,
    SpacingNormalizer,
    EmojiFilter,
    EmailMasker,
    URLMasker,
    DiacriticFilter,
    # NonPersianLetterFilter,
    HTMLTagFilter,
    RepeatedLetterFilter,
    ArabicUnicodeNormalizer,
)


class Normalizer(Pipeline):
    def __init__(self, steps=None):
        if steps is None:
            steps = [
                ("AlphabetNormalizer", AlphabetNormalizer()),
                ("ArabicUnicodeNormalizer", ArabicUnicodeNormalizer()),
                ("DigitNormalizer", DigitNormalizer()),
                ("PunctuationNormalizer", PunctuationNormalizer()),
                ("EmailMasker", EmailMasker(mask="")),
                ("URLMasker", URLMasker(mask="")),
                ("EmojiFilter", EmojiFilter()),
                ("HTMLTagFilter", HTMLTagFilter()),
                ("DiacriticFilter", DiacriticFilter()),
                ("RepeatedLetterFilter", RepeatedLetterFilter()),
                # ("NonPersianLetterFilter", NonPersianLetterFilter()),
                ("SpacingNormalizer", SpacingNormalizer()),
            ]
        super().__init__(steps=steps)

    def normalize(self, text: Iterable[str] | str):
        return self(text)
