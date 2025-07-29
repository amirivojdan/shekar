from shekar.base import BaseTextTransform
import html


class HTMLTagFilter(BaseTextTransform):
    """
    A text transformation class for removing HTML tags and entities from the text.

    This class inherits from `BaseTextTransform` and provides functionality to identify
    and remove HTML tags and entities from the text. It ensures a clean and tag-free
    representation of the text by unescaping HTML entities and removing all HTML tags.

    The `HTMLTagRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing HTML tags and entities.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> html_tag_remover = HTMLTagFilter()
        >>> cleaned_text = html_tag_remover("<p>این یک <strong>متن</strong> نمونه است.</p>")
        >>> print(cleaned_text)
        "این یک متن نمونه است."
    """

    def __init__(self, replace_with: str = " "):
        super().__init__()
        self._html_tag_mappings = [
            (r"<[^>]+>", replace_with),
        ]

        self._patterns = self._compile_patterns(self._html_tag_mappings)

    def _function(self, text: str) -> str:
        text = html.unescape(text)
        return self._map_patterns(text, self._patterns).strip()
