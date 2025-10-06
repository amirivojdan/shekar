from shekar.base import BaseTextTransform


class URLMasker(BaseTextTransform):
    """
    A text transformation class for masking URLs in the text.

    This class inherits from `BaseTextTransform` and provides functionality to identify
    and mask URLs in the text. It replaces URLs with a specified mask, ensuring privacy
    and anonymization of sensitive information.

    The `URLMasker` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Args:
        mask (str): The mask to replace the URLs with. Default is "<URL>".

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by masking URLs.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.
    Example:
        >>> url_masker = URLMasker(mask="<URL>")
        >>> masked_text = url_masker("برای اطلاعات بیشتر به https://shekar.io مراجعه کنید.")
        >>> print(masked_text)
        "برای اطلاعات بیشتر به <URL> مراجعه کنید."
    """

    def __init__(self, mask_token: str = "<URL>"):
        super().__init__()
        self._mask_token = mask_token
        self._url_mappings = [
            (r"(https?://[^\s]+)", self._mask_token),
        ]
        self._patterns = self._compile_patterns(self._url_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
