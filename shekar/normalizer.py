from typing import Iterable
from shekar import Pipeline
from shekar.preprocessing import (
    PunctuationNormalizer,
    AlphabetNormalizer,
    DigitNormalizer,
    SpacingNormalizer,
    RemoveDiacritics,
    RepeatedLetterNormalizer,
    ArabicUnicodeNormalizer,
    YaNormalizer,
)


class Normalizer(Pipeline):
    def __init__(self, steps=None):
        if steps is None:
            steps = [
                ("AlphabetNormalizer", AlphabetNormalizer()),
                ("ArabicUnicodeNormalizer", ArabicUnicodeNormalizer()),
                ("DigitNormalizer", DigitNormalizer()),
                ("PunctuationNormalizer", PunctuationNormalizer()),
                ("DiacriticRemover", RemoveDiacritics()),
                ("RepeatedLetterNormalizer", RepeatedLetterNormalizer()),
                ("SpacingNormalizer", SpacingNormalizer()),
                ("YaNormalizer", YaNormalizer(style="joda")),
            ]
        super().__init__(steps=steps)

    def normalize(self, text: Iterable[str] | str):
        return self(text)
