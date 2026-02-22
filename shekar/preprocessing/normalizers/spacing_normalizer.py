from shekar import Pipeline
from .word_spacing_normalizer import WordSpacingNormalizer
from .orthographic_spacing_normalizer import OrthographicSpacingNormalizer
from .verbal_spacing_normalizer import VerbalSpacingNormalizer
from .punctuation_spacing_normalizer import PunctuationSpacingNormalizer


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
