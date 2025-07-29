from shekar.base import BaseTextTransform


class MentionFilter(BaseTextTransform):
    """
    A text transformation class for removing mentions from the text.

    This class inherits from `BaseTextTransform` and provides functionality to identify
    and remove mentions from the text. It ensures a clean representation of the text by
    eliminating all mentions.

    The `MentionFilter` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing mentions.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> mention_remover = MentionFilter()
        >>> cleaned_text = mention_remover("سلام @user! چطوری؟")
        >>> print(cleaned_text)
        "سلام ! چطوری؟"
    """

    def __init__(self, replace_with: str = " "):
        super().__init__()
        self._mention_mappings = [
            (r"@([^\s]+)", replace_with),
        ]

        self._patterns = self._compile_patterns(self._mention_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
