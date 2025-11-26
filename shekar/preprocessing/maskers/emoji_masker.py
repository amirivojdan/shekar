from shekar.base import BaseTextTransform


class EmojiMasker(BaseTextTransform):
    """
    A text transformation class for removing emojis from the text.
    This class inherits from `BaseTextTransform` and provides functionality to remove
    emojis from the text. It identifies and eliminates a wide range of emojis, ensuring a clean and emoji-free text representation.
    The `EmojiMasker` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing emojis.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> emoji_masker = EmojiMasker()
        >>> cleaned_text = emoji_masker("درود بر شما😊!🌟")
        >>> print(cleaned_text)
        "درود بر شما!"
    """

    def __init__(self, mask_token: str = ""):
        super().__init__()
        self._mask_token = mask_token

        self._emoji_mappings = [
            (
                r"(?:"
                r"\p{Extended_Pictographic}(?:\p{Emoji_Modifier})?(?:\uFE0F)?"
                r"(?:\u200D\p{Extended_Pictographic}(?:\p{Emoji_Modifier})?(?:\uFE0F)?)*"
                r"|"
                r"(?:\p{Regional_Indicator}{2})"  # country flags
                r")",
                self._mask_token,
            ),
        ]

        self._patterns = self._compile_patterns(self._emoji_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
