from .alphabet_normalizer import AlphabetNormalizer
from .arabic_unicode_normalizer import ArabicUnicodeNormalizer
from .digit_normalizer import DigitNormalizer
from .orthographic_spacing_normalizer import OrthographicSpacingNormalizer
from .punctuation_normalizer import PunctuationNormalizer
from .punctuation_spacing_normalizer import PunctuationSpacingNormalizer
from .repeated_letter_normalizer import RepeatedLetterNormalizer
from .spacing_normalizer import SpacingNormalizer
from .verbal_spacing_normalizer import VerbalSpacingNormalizer
from .word_spacing_normalizer import WordSpacingNormalizer
from .ya_normalizer import YaNormalizer

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
    "NormalizeAlphabets",
    "NormalizeArabicUnicodes",
    "NormalizeDigits",
    "NormalizeOrthographicSpacings",
    "NormalizePunctuationSpacings",
    "NormalizePunctuations",
    "NormalizeRepeatedLetters",
    "NormalizeSpacings",
    "NormalizeVerbalSpacings",
    "NormalizeWordSpacings",
    "NormalizeYas",
    "OrthographicSpacingNormalizer",
    "PunctuationNormalizer",
    "PunctuationSpacingNormalizer",
    "RepeatedLetterNormalizer",
    "SpacingNormalizer",
    "VerbalSpacingNormalizer",
    "WordSpacingNormalizer",
    "YaNormalizer",
]
