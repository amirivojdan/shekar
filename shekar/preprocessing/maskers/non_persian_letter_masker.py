from shekar.base import BaseTextTransform
from shekar import data
import re
import string


class NonPersianLetterMasker(BaseTextTransform):
    """
    A text transformation class for removing non-Persian characters from the text.

    This class inherits from `BaseTextTransform` and provides functionality to identify
    and remove non-Persian characters from the text. It uses predefined character sets
    to filter out unwanted characters while optionally retaining English characters and diacritics.

    The `NonPersianLetterMasker` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Args:
        keep_english (bool): If True, retains English characters. Default is False.
        keep_diacritics (bool): If True, retains diacritics. Default is False.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing non-Persian characters.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.
    Example:
        >>> non_persian_masker = NonPersianLetterMasker(keep_english=True, keep_diacritics=False)
        >>> cleaned_text = non_persian_masker("این یک متن نمونه است! Hello!")
        >>> print(cleaned_text)
        "این یک متن نمونه است! Hello!"
    """

    def __init__(self, keep_english=False, keep_diacritics=False):
        super().__init__()

        self.characters_to_keep = (
            data.persian_letters + data.spaces + data.persian_digits + data.punctuations
        )

        if keep_diacritics:
            self.characters_to_keep += data.diacritics

        if keep_english:
            self.characters_to_keep += (
                string.ascii_letters + string.digits + string.punctuation
            )

        allowed_chars = re.escape(self.characters_to_keep)
        self._filter_mappings = [(r"[^" + allowed_chars + r"]+", "")]

        self._patterns = self._compile_patterns(self._filter_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
