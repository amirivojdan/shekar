from typing import Iterable
from shekar import data
from shekar.base import BaseTextTransform
import re


class OffensiveWordMasker(BaseTextTransform):
    """
    A text transformation class for removing Persian offensive words from the text.

    This class inherits from `WordMasker` and provides functionality to identify
    and remove Persian offensive words from the text. It uses a predefined list of offensive words
    to filter out inappropriate content from the text.

    The `OffensiveWordMasker` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Args:
        offensive_words (Iterable[str], optional): A list of offensive words to be removed from the text.
            If not provided, a default list of Persian offensive words will be used.

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
        >>> offensive_word_masker = OffensiveWordMasker(offensive_words=["تاپاله","فحش", "بد", "زشت"], mask_token="[بوق]")
        >>> cleaned_text = offensive_word_masker("عجب آدم تاپاله‌ای هستی!")
        >>> print(cleaned_text)
        "عجب آدم [بوق]‌ای هستی!"
    """

    def __init__(self, words: Iterable[str] = None, mask_token: str = ""):
        super().__init__()
        if words is None:
            words = data.offensive_words
        self._mask_token = mask_token
        self._word_mappings = []
        self._word_mappings.append(
            (rf"\b({'|'.join(map(re.escape, words))})\b", mask_token)
        )

        self._patterns = self._compile_patterns(self._word_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
