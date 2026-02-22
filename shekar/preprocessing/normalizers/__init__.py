from .alphabet_normalizer import AlphabetNormalizer
from .arabic_unicode_normalizer import ArabicUnicodeNormalizer
from .digit_normalizer import DigitNormalizer
from .punctuation_normalizer import PunctuationNormalizer
from .ya_normalizer import YaNormalizer
from .repeated_letter_normalizer import RepeatedLetterNormalizer

from .spacing_normalizer import SpacingNormalizer
from .orthographic_spacing_normalizer import OrthographicSpacingNormalizer
from .verbal_spacing_normalizer import VerbalSpacingNormalizer
from .punctuation_spacing_normalizer import PunctuationSpacingNormalizer
from .word_spacing_normalizer import WordSpacingNormalizer

# aliases
NormalizeDigits = DigitNormalizer
NormalizePunctuations = PunctuationNormalizer
NormalizeArabicUnicodes = ArabicUnicodeNormalizer
NormalizeYas = YaNormalizer
NormalizeAlphabets = AlphabetNormalizer
NormalizeRepeatedLetters = RepeatedLetterNormalizer
NormalizePunctuationSpacings = PunctuationSpacingNormalizer
NormalizeOrthographicSpacings = OrthographicSpacingNormalizer
NormalizeVerbalSpacings = VerbalSpacingNormalizer
NormalizeWordSpacings = WordSpacingNormalizer
NormalizeSpacings = SpacingNormalizer

__all__ = [
    "AlphabetNormalizer",
    "ArabicUnicodeNormalizer",
    "DigitNormalizer",
    "PunctuationNormalizer",
    "YaNormalizer",
    "RepeatedLetterNormalizer",
    "SpacingNormalizer",
    "OrthographicSpacingNormalizer",
    "VerbalSpacingNormalizer",
    "PunctuationSpacingNormalizer",
    "WordSpacingNormalizer",
    # aliases
    "NormalizeDigits",
    "NormalizePunctuations",
    "NormalizeArabicUnicodes",
    "NormalizeAlphabets",
    "NormalizeYas",
    "NormalizeRepeatedLetters",
    "NormalizeSpacings",
    "NormalizeOrthographicSpacings",
    "NormalizeVerbalSpacings",
    "NormalizePunctuationSpacings",
    "NormalizeWordSpacings",
]
