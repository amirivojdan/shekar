from .alphabet_normalizer import AlphabetNormalizer
from .arabic_unicode_normalizer import ArabicUnicodeNormalizer
from .digit_normalizer import DigitNormalizer
from .punctuation_normalizer import PunctuationNormalizer
from .spacing_normalizer import SpacingNormalizer

# aliases
NormalizeDigits = DigitNormalizer
NormalizePunctuations = PunctuationNormalizer
NormalizeArabicUnicodes = ArabicUnicodeNormalizer
NormalizeSpacings = SpacingNormalizer
NormalizeAlphabets = AlphabetNormalizer

__all__ = [
    "AlphabetNormalizer",
    "ArabicUnicodeNormalizer",
    "DigitNormalizer",
    "PunctuationNormalizer",
    "SpacingNormalizer",
    # aliases
    "NormalizeDigits",
    "NormalizePunctuations",
    "NormalizeArabicUnicodes",
    "NormalizeSpacings",
    "NormalizeAlphabets",
]
