from .email_masker import EmailMasker
from .url_masker import URLMasker

# aliases

MaskEmails = EmailMasker
MaskURLs = URLMasker


__all__ = [
    "EmailMasker",
    "URLMasker",
    # aliases
    "MaskEmails",
    "MaskURLs",
]
