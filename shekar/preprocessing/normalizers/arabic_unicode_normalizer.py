from shekar.base import BaseTextTransform


class ArabicUnicodeNormalizer(BaseTextTransform):
    """
    A text transformation class for normalizing special Arabic Unicode characters to their Persian equivalents.

    This class inherits from `BaseTextTransform` and provides functionality to replace
    various special Arabic Unicode characters with their Persian equivalents. It uses predefined mappings
    to substitute characters such as "﷽", "﷼", and other Arabic ligatures with their standard Persian representations.

    The `ArabicUnicodeNormalizer` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by normalizing special Arabic Unicode characters.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> unicode_normalizer = ArabicUnicodeNormalizer()
        >>> normalized_text = unicode_normalizer("﷽ ﷼ ﷴ")
        >>> print(normalized_text)
        "بسم الله الرحمن الرحیم ریال محمد"
    """

    def __init__(self):
        super().__init__()
        self.unicode_mappings = [
            ("﷽", "بسم الله الرحمن الرحیم"),
            ("﷼", "ریال"),
            ("(ﷰ|ﷹ)", "صلی"),
            ("ﷲ", "الله"),
            ("ﷳ", "اکبر"),
            ("ﷴ", "محمد"),
            ("ﷵ", "صلعم"),
            ("ﷶ", "رسول"),
            ("ﷷ", "علیه"),
            ("ﷸ", "وسلم"),
            ("ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ", "لا"),
        ]

        self._patterns = self._compile_patterns(self.unicode_mappings)

    def _function(self, X, y=None):
        return self._map_patterns(X, self._patterns)
