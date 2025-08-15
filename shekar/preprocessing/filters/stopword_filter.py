from typing import Iterable
from shekar.base import BaseTextTransform
from shekar import data
import re


class StopWordFilter(BaseTextTransform):
    """
    A text transformation class for removing Persian stopwords from the text.

    This class inherits from `BaseTextTransform` and provides functionality to identify
    and remove Persian stopwords from the text. It uses a predefined list of stopwords
    to filter out common words that do not contribute significant meaning to the text.

    The `StopWordRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Args:
        stopwords (Iterable[str], optional): A list of stopwords to be removed from the text.
            If not provided, a default list of Persian stopwords will be used.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing stopwords.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.
    Example:
        >>> stopword_remover = StopWordFilter(stopwords=["و", "به", "از"])
        >>> cleaned_text = stopword_remover("این یک متن نمونه است و به شما کمک می‌کند.")
        >>> print(cleaned_text)
        "این یک متن نمونه است شما کمک می‌کند."
    """

    def __init__(self, stopwords: Iterable[str] = None, replace_with: str = ""):
        super().__init__()
        self.stopwords = stopwords or data.stopwords

        self.replace_with = replace_with
        self._stopword_mappings = []
        for stopword in self.stopwords:
            escaped_word = re.escape(stopword)
            self._stopword_mappings.append(
                (
                    rf"(?<![{data.persian_full_set}]){escaped_word}(?![{data.persian_full_set}])",
                    replace_with,
                )
            )

        self._patterns = self._compile_patterns(self._stopword_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
