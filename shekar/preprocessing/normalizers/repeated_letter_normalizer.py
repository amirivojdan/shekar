from shekar import BaseTextTransform


class RepeatedLetterNormalizer(BaseTextTransform):
    """
    A text transformation class for removing redundant characters from the text.

    This class inherits from `BaseTextTransform` and provides functionality to identify
    and remove redundant characters from the text. It removes more than two repeated letters
    and eliminates every keshida (ـ) from the text, ensuring a clean and normalized representation.

    The `RedundantCharacterRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing redundant characters.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> redundant_char_remover = RedundantCharacterRemover()
        >>> cleaned_text = redundant_char_remover("اینــــجاااا یکــــــ متنــــــ نمونه است.")
        >>> print(cleaned_text)
        "اینجاا یک متن نمونه است."
    """

    def __init__(self):
        super().__init__()
        self._redundant_mappings = [
            (r"[ـ]", ""),  # remove keshida
            (r"([^\s])\1{2,}", r"\1\1"),  # remove more than two repeated letters
        ]

        self._patterns = self._compile_patterns(self._redundant_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
