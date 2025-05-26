from .punctuation_spacing_standardizer import PunctuationSpacingStandardizer
from .spacing_standardizer import SpacingStandardizer

#aliases 

StandardizeSpacings = SpacingStandardizer
StandardizePunctuationSpacings = PunctuationSpacingStandardizer

__all__ = [
    "PunctuationSpacingStandardizer",
    "SpacingStandardizer",

    # Aliases
    "StandardizeSpacings",
    "StandardizePunctuationSpacings",
]