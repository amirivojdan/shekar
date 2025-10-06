from shekar.base import BaseTextTransform
from shekar import data
import re
import string


class PunctuationMasker(BaseTextTransform):
    """
    A text transformation class for filtering out specified punctuation characters from the text.
    This class inherits from `BaseTextTransform` and provides functionality to remove
    various punctuation symbols based on user-defined or default settings. It uses regular
    expressions to identify and replace specified punctuation characters with a given replacement string.
    The `PunctuationMasker` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.
    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by filtering out specified punctuation characters.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.
    Example:
        >>> punctuation_masker = PunctuationMasker()
        >>> filtered_text = punctuation_masker("دریغ است ایران که ویران شود!")
        >>> print(filtered_text)
        "دریغ است ایران که ویران شود"
    """

    def __init__(self, punctuations: str | None = None, mask_token: str = ""):
        super().__init__()
        if not punctuations:
            self._punctuation_mappings = [
                (rf"[{re.escape(data.punctuations)}]", mask_token),
                (rf"[{re.escape(string.punctuation)}]", mask_token),
            ]

        else:
            self._punctuation_mappings = [
                (rf"[{re.escape(punctuations)}]", mask_token),
            ]

        self._patterns = self._compile_patterns(self._punctuation_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
