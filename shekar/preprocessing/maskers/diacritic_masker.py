from shekar.base import BaseTextTransform
from shekar import data


class DiacriticMasker(BaseTextTransform):
    """
    A text transformation class for removing Arabic diacritics from the text.

    This class inherits from `BaseTextTransform` and provides functionality to remove
    Arabic diacritics from the text. It uses predefined mappings to eliminate diacritics
    such as "َ", "ً", "ُ", and others, ensuring a clean and normalized text representation.

    The `DiacriticMasker` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing diacritics.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> diacritic_masker = DiacriticMasker()
        >>> cleaned_text = diacritic_masker("کُجا نِشانِ قَدَم ناتَمام خواهَد ماند؟")
        >>> print(cleaned_text)
        "کجا نشان قدم ناتمام خواهد ماند؟"
    """

    def __init__(self):
        super().__init__()
        self._diacritic_mappings = [
            (data.diacritics, ""),
        ]

        self._translation_table = self._create_translation_table(
            self._diacritic_mappings
        )

    def _function(self, text: str) -> str:
        return text.translate(self._translation_table)
