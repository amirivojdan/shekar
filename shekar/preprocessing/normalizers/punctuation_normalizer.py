from shekar.base import BaseTextTransform


class PunctuationNormalizer(BaseTextTransform):
    """
    A text transformation class for normalizing punctuation marks in text.

    This class inherits from `BaseTextTransform` and provides functionality to replace
    various punctuation symbols with their normalized equivalents. It uses predefined
    mappings to substitute characters such as dashes, underscores, question marks,
    exclamation marks, and others with consistent representations.

    The `PunctuationNormalizer` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by normalizing punctuation marks.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> punc_normalizer = PunctuationNormalizer()
        >>> normalized_text = punc_normalizer("فارسی شکر است❕نوشته کیست?")
        >>> print(normalized_text)
        "فارسی شکر است! نوشته کیست؟"
    """

    def __init__(self):
        super().__init__()
        self.punctuation_mappings = [
            ("▕❘❙❚▏│", "|"),
            ("ㅡ一—–ー̶", "-"),
            ("▁_̲", "_"),
            ("❔?�؟ʕʔ🏻\x08\x97\x9d", "؟"),
            ("❕！", "!"),
            ("⁉", "!؟"),
            ("‼", "!!"),
            ("℅%", "٪"),
            ("÷", "/"),
            ("×", "*"),
            ("：", ":"),
            ("›", ">"),
            ("‹＜", "<"),
            ("《", "«"),
            ("》", "»"),
            ("•", "."),
            ("٬,", "،"),
            (";；", "؛"),
        ]

        self._translation_table = self._create_translation_table(
            self.punctuation_mappings
        )

    def _function(self, X, y=None):
        return X.translate(self._translation_table)
