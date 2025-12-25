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

        _emoji_base = (
            r"\u2600-\u26FF"  # Misc symbols
            r"\u2700-\u27BF"  # Dingbats
            r"\U0001F000-\U0001F02F"  # Mahjong, domino
            r"\U0001F0A0-\U0001F0FF"  # Playing cards
            r"\U0001F100-\U0001F1FF"  # Enclosed alnum + Regional indicators live here too
            r"\U0001F200-\U0001F2FF"  # Enclosed ideographic
            r"\U0001F300-\U0001F5FF"  # Misc symbols and pictographs
            r"\U0001F600-\U0001F64F"  # Emoticons
            r"\U0001F680-\U0001F6FF"  # Transport and map
            r"\U0001F700-\U0001F77F"  # Alchemical
            r"\U0001F780-\U0001F7FF"  # Geometric extended
            r"\U0001F800-\U0001F8FF"  # Supplemental arrows C
            r"\U0001F900-\U0001F9FF"  # Supplemental symbols and pictographs
            r"\U0001FA00-\U0001FA6F"  # Chess, symbols
            r"\U0001FA70-\U0001FAFF"  # Symbols and pictographs extended A
        )

        _skin_tone_modifiers = r"\U0001F3FB-\U0001F3FF"
        _regional = r"\U0001F1E6-\U0001F1FF"
        _VS16 = r"\uFE0F"
        _ZWJ = r"\u200D"

        self._emoji_mappings = [
            (
                rf"(?:"
                rf"(?:"
                rf"[{_emoji_base}]"
                rf"(?:[{_skin_tone_modifiers}])?"
                rf"(?:{_VS16})?"
                rf"(?:{_ZWJ}"
                rf"[{_emoji_base}]"
                rf"(?:[{_skin_tone_modifiers}])?"
                rf"(?:{_VS16})?"
                rf")*"
                rf")"
                rf"|"
                rf"(?:[{_regional}]{{2}})"
                rf")",
                self._mask_token,
            ),
        ]

        self._patterns = self._compile_patterns(self._emoji_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
