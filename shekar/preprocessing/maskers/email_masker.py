from shekar.base import BaseTextTransform


class EmailMasker(BaseTextTransform):
    """
    A text transformation class for masking email addresses in the text.

    This class inherits from `BaseTextTransform` and provides functionality to identify
    and mask email addresses in the text. It replaces email addresses with a specified
    mask, ensuring privacy and anonymization of sensitive information.

    The `EmailMasker` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Args:
        mask (str): The mask to replace the email addresses with. Default is "<EMAIL>".

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by masking email addresses.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> email_masker = EmailMasker(mask="<EMAIL>")
        >>> masked_text = email_masker("برای تماس با ما به info@shekar.io ایمیل بزنید.")
        >>> print(masked_text)
        "برای تماس با ما به <EMAIL> ایمیل بزنید."
    """

    def __init__(self, mask_token: str = "<EMAIL>"):
        super().__init__()
        self._mask_token = mask_token
        self._email_mappings = [
            (r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", self._mask_token),
        ]
        self._patterns = self._compile_patterns(self._email_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns).strip()
