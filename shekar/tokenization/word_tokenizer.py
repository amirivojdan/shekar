import re
from typing import Iterable
from shekar import data, BaseTextTransform


class WordTokenizer(BaseTextTransform):
    """
    A class used to tokenize text into words based on spaces and punctuation marks.
    Methods:
        tokenize(text: str) -> List[str]: Tokenizes the input text into a list of words.
    Example:
        >>> tokenizer = WordTokenizer()
        >>> text = "چه سیب‌های قشنگی! حیات نشئه تنهایی است."
        >>> tokenizer.tokenize(text)
        ['چه', 'سیب‌های', 'قشنگی', '!', 'حیات', 'نشئه', 'تنهایی', 'است', '.']
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(rf"([{re.escape(data.punctuations)}])|\s+")

    def tokenize(self, text: str) -> Iterable[str]:
        """
        Tokenizes the input text into a list of words, keeping punctuations as separate tokens.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            Iterable[str]: A Iterable of tokenized words and punctuations.
        """
        return self._function(text)

    def _function(self, text: str) -> Iterable[str]:
        """
        Tokenizes the input text into a list of words, keeping punctuations as separate tokens.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            List[str]: A list of tokenized words and punctuations.
        """
        tokens = self.pattern.split(text)
        return (token for token in tokens if token and not token.isspace())
