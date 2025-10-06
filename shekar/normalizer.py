from typing import Iterable
from shekar import Pipeline
from shekar.preprocessing import (
    PunctuationNormalizer,
    AlphabetNormalizer,
    DigitNormalizer,
    SpacingNormalizer,
    MaskEmojis,
    MaskEmails,
    MaskURLs,
    RemoveDiacritics,
    # NonPersianLetterMasker,
    MaskHTMLTags,
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
                ("EmailMasker", MaskEmails(mask_token=" ")),
                ("URLMasker", MaskURLs(mask_token=" ")),
                ("EmojiMasker", MaskEmojis(mask_token=" ")),
                ("HTMLTagMasker", MaskHTMLTags(mask_token=" ")),
                ("DiacriticRemover", RemoveDiacritics()),
                ("RepeatedLetterNormalizer", RepeatedLetterNormalizer()),
                # ("NonPersianLetterFilter", NonPersianLetterFilter()),
                ("SpacingNormalizer", SpacingNormalizer()),
                ("YaNormalizer", YaNormalizer(style="joda")),
            ]
        super().__init__(steps=steps)

    def normalize(self, text: Iterable[str] | str):
        return self(text)
