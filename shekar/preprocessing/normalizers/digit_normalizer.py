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

        self.digit_mappings = [
            ("0٠𝟢𝟬", "۰"),
            ("1١𝟣𝟭⑴⒈⓵①❶𝟙𝟷ı", "۱"),
            ("2٢𝟤𝟮⑵⒉⓶②❷²𝟐𝟸𝟚ᒿշ", "۲"),
            ("3٣𝟥𝟯⑶⒊⓷③❸³ვ", "۳"),
            ("4٤𝟦𝟰⑷⒋⓸④❹⁴", "۴"),
            ("5٥𝟧𝟱⑸⒌⓹⑤❺⁵", "۵"),
            ("6٦𝟨𝟲⑹⒍⓺⑥❻⁶", "۶"),
            ("7٧𝟩𝟳⑺⒎⓻⑦❼⁷", "۷"),
            ("8٨𝟪𝟴⑻⒏⓼⑧❽⁸۸", "۸"),
            ("9٩𝟫𝟵⑼⒐⓽⑨❾⁹", "۹"),
            ("⑽⒑⓾⑩", "۱۰"),
            ("⑾⒒⑪", "۱۱"),
            ("⑿⒓⑫", "۱۲"),
            ("⒀⒔⑬", "۱۳"),
            ("⒁⒕⑭", "۱۴"),
            ("⒂⒖⑮", "۱۵"),
            ("⒃⒗⑯", "۱۶"),
            ("⒄⒘⑰", "۱۷"),
            ("⒅⒙⑱", "۱۸"),
            ("⒆⒚⑲", "۱۹"),
            ("⒇⒛⑳", "۲۰"),
        ]

        self._translation_table = self._create_translation_table(self.digit_mappings)

    def _function(self, X, y=None):
        return X.translate(self._translation_table)
