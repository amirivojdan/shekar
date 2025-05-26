from shekar.base import BaseTextTransform
from shekar import data
import re

class PunctuationSpacingStandardizer(BaseTextTransform):
    """
    A text transformation class for standardizing spacing around punctuation marks in the text.

    This class inherits from `BaseTextTransform` and provides functionality to ensure
    consistent spacing around punctuation marks in the text. It removes extra spaces before
    and after punctuation marks, ensuring a clean and standardized representation.

    The `PunctuationSpacingStandardizer` class includes `fit` and `fit_transform` methods,
    and it is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by standardizing spacing around punctuation marks.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.
    Example:
        >>> punctuation_spacing_standardizer = PunctuationSpacingStandardizer()
        >>> cleaned_text = punctuation_spacing_standardizer("این یک متن نمونه است !")
        >>> print(cleaned_text)
        "این یک متن نمونه است!"
    """

    def __init__(self):
        super().__init__()

        self._spacing_mappings = [
            (
                r"\s*([{}])\s*".format(
                    re.escape(data.single_punctuations + data.closer_punctuations)
                ),
                r"\1 ",
            ),
            (
                r"\s*([{}])\s*".format(re.escape(data.opener_punctuations)),
                r" \1",
            ),
        ]

        self._patterns = self._compile_patterns(self._spacing_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns)
    
