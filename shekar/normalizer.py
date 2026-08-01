from collections.abc import Iterable

from shekar.pipeline import Pipeline
from shekar.preprocessing import (
    AlphabetNormalizer,
    ArabicUnicodeNormalizer,
    DigitNormalizer,
    PunctuationNormalizer,
    RemoveDiacritics,
    RepeatedLetterNormalizer,
    SpacingNormalizer,
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
                ("YaNormalizer", YaNormalizer()),
            ]
        super().__init__(steps=steps)

    def normalize(self, text: Iterable[str] | str):
        return self(text)
