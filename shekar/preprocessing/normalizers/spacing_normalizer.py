from shekar.pipeline import Pipeline

from .orthographic_spacing_normalizer import OrthographicSpacingNormalizer
from .punctuation_spacing_normalizer import PunctuationSpacingNormalizer
from .verbal_spacing_normalizer import VerbalSpacingNormalizer
from .word_spacing_normalizer import WordSpacingNormalizer


class SpacingNormalizer(Pipeline):
    def __init__(self, steps=None):
        if steps is None:
            steps = [
                ("OrthographicSpacingNormalizer", OrthographicSpacingNormalizer()),
                ("PunctuationSpacingNormalizer", PunctuationSpacingNormalizer()),
                ("WordSpacingNormalizer", WordSpacingNormalizer()),
                ("VerbalSpacingNormalizer", VerbalSpacingNormalizer()),
            ]
        super().__init__(steps=steps)
