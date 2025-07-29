from shekar.base import BaseTextTransform


class DigitNormalizer(BaseTextTransform):
    """
    A text transformation class for normalizing Arabic, English, and other Unicode number signs to Persian numbers.

    This class inherits from `BaseTextTransform` and provides functionality to replace
    various numeric characters from Arabic, English, and other Unicode representations with their Persian equivalents.
    It uses predefined mappings to substitute characters such as "1", "٢", and other numeric signs with their standard Persian representations.

    The `NumericNormalizer` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by normalizing numbers.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> numeric_normalizer = NumericNormalizer()
        >>> normalized_text = numeric_normalizer("1𝟮3٤٥⓺")
        >>> print(normalized_text)
        "۱۲۳۴۵۶"
    """

    def __init__(self):
        super().__init__()
        self._number_mappings = [
            (r"[0٠𝟢𝟬]", "۰"),
            (r"[1١𝟣𝟭⑴⒈⓵①❶𝟙𝟷ı]", "۱"),
            (r"[2٢𝟤𝟮⑵⒉⓶②❷²𝟐𝟸𝟚ᒿշ]", "۲"),
            (r"[3٣𝟥𝟯⑶⒊⓷③❸³ვ]", "۳"),
            (r"[4٤𝟦𝟰⑷⒋⓸④❹⁴]", "۴"),
            (r"[5٥𝟧𝟱⑸⒌⓹⑤❺⁵]", "۵"),
            (r"[6٦𝟨𝟲⑹⒍⓺⑥❻⁶]", "۶"),
            (r"[7٧𝟩𝟳⑺⒎⓻⑦❼⁷]", "۷"),
            (r"[8٨𝟪𝟴⑻⒏⓼⑧❽⁸۸]", "۸"),
            (r"[9٩𝟫𝟵⑼⒐⓽⑨❾⁹]", "۹"),
            (r"[⑽⒑⓾⑩]", "۱۰"),
            (r"[⑾⒒⑪]", "۱۱"),
            (r"[⑿⒓⑫]", "۱۲"),
            (r"[⒀⒔⑬]", "۱۳"),
            (r"[⒁⒕⑭]", "۱۴"),
            (r"[⒂⒖⑮]", "۱۵"),
            (r"[⒃⒗⑯]", "۱۶"),
            (r"[⒄⒘⑰]", "۱۷"),
            (r"[⒅⒙⑱]", "۱۸"),
            (r"[⒆⒚⑲]", "۱۹"),
            (r"[⒇⒛⑳]", "۲۰"),
        ]
        self._patterns = self._compile_patterns(self._number_mappings)

    def _function(self, X, y=None):
        return self._map_patterns(X, self._patterns)
