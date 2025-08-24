from .alphabet_normalizer import AlphabetNormalizer
from .arabic_unicode_normalizer import ArabicUnicodeNormalizer
from .digit_normalizer import DigitNormalizer
from .punctuation_normalizer import PunctuationNormalizer
from .spacing_normalizer import SpacingNormalizer
from .ya_normalizer import YaNormalizer

# aliases
NormalizeDigits = DigitNormalizer
NormalizePunctuations = PunctuationNormalizer
NormalizeArabicUnicodes = ArabicUnicodeNormalizer
NormalizeYas = YaNormalizer
NormalizeSpacings = SpacingNormalizer
NormalizeAlphabets = AlphabetNormalizer

__all__ = [
    "AlphabetNormalizer",
    "ArabicUnicodeNormalizer",
    "DigitNormalizer",
    "PunctuationNormalizer",
    "SpacingNormalizer",
    "YaNormalizer",
    # aliases
    "NormalizeDigits",
    "NormalizePunctuations",
    "NormalizeArabicUnicodes",
    "NormalizeSpacings",
    "NormalizeAlphabets",
    "NormalizeYas",
]
