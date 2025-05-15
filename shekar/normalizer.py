from typing import Iterable
from shekar import Pipeline
from shekar.preprocessing import (
    PunctuationNormalizer,
    AlphabetNormalizer,
    NumericNormalizer,
    SpacingStandardizer,
    EmojiRemover,
    EmailMasker,
    URLMasker,
    DiacriticsRemover,
    NonPersianRemover,
    HTMLTagRemover,
    RedundantCharacterRemover,
    ArabicUnicodeNormalizer,
)


class Normalizer(Pipeline):
    def __init__(self, steps=None):
        if steps is None:
            steps = [
                ("AlphaNumericUnifier", AlphabetNormalizer()),
                ("ArabicUnicodeNormalizer", ArabicUnicodeNormalizer()),
                ("NumericNormalizer", NumericNormalizer()),
                ("PunctuationUnifier", PunctuationNormalizer()),
                ("EmailMasker", EmailMasker(mask="")),
                ("URLMasker", URLMasker(mask="")),
                ("EmojiRemover", EmojiRemover()),
                ("HTMLTagRemover", HTMLTagRemover()),
                ("DiacriticsRemover", DiacriticsRemover()),
                ("RedundantCharacterRemover", RedundantCharacterRemover()),
                ("NonPersianRemover", NonPersianRemover()),
                ("SpacingStandardizer", SpacingStandardizer()),
            ]
        super().__init__(steps=steps)

    def normalize(self, text: Iterable[str] | str):
        return self(text)
