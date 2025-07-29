import re
from typing import Iterable
from shekar import data, BaseTextTransform


class SentenceTokenizer(BaseTextTransform):
    """
    A class used to tokenize text into sentences based on punctuation marks.
    Attributes:
        pattern (Pattern): A compiled regular expression pattern used to identify sentence-ending punctuation.
    Methods:
        tokenize(text: str) -> List[str]: Tokenizes the input text into a list of sentences.
    Example:
        >>> tokenizer = SentenceTokenizer()
        >>> text = "چه سیب‌های قشنگی! حیات نشئه تنهایی است."
        >>> tokenizer.tokenize(text)
        ['.چه سیب‌های قشنگی!', 'حیات نشئه تنهایی است']
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            f"([{re.escape(data.end_sentence_punctuations)}]+)", re.UNICODE
        )

    def _function(self, text: str) -> Iterable[str]:
        """
        Tokenizes the input text into a list of sentences.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            List[str]: A list of tokenized sentences.
        """

        tokens = self.pattern.split(text)
        for i in range(0, len(tokens) - 1, 2):
            if tokens[i].strip() or tokens[i + 1].strip():
                yield tokens[i].strip() + tokens[i + 1].strip()
        if len(tokens) % 2 == 1 and tokens[-1].strip():
            yield tokens[-1].strip()

    def tokenize(self, text: str) -> Iterable[str]:
        """
        Tokenizes the input text into a list of sentences.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            List[str]: A list of tokenized sentences.
        """
        return self._function(text)
