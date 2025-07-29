from .alphabet_normalizer import AlphabetNormalizer
from .arabic_unicode_normalizer import ArabicUnicodeNormalizer
from .digit_normalizer import DigitNormalizer
from .punctuation_normalizer import PunctuationNormalizer

# aliases
NormalizeDigits = DigitNormalizer
NormalizePunctuations = PunctuationNormalizer
NormalizeArabicUnicodes = ArabicUnicodeNormalizer
NormalizeAlphabets = AlphabetNormalizer

__all__ = [
    "AlphabetNormalizer",
    "ArabicUnicodeNormalizer",
    "DigitNormalizer",
    "PunctuationNormalizer",
    # aliases
    "NormalizeDigits",
    "NormalizePunctuations",
    "NormalizeArabicUnicodes",
    "NormalizeAlphabets",
]
