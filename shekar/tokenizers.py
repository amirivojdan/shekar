import re
from typing import List
from shekar import utils


class SentenceTokenizer:
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

    def __init__(self) -> None:
        self.pattern = re.compile(f"([{re.escape(utils.punctuations)}]+)", re.UNICODE)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes the input text into a list of sentences.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            List[str]: A list of tokenized sentences.
        """
        text = re.sub(r"\s+", " ", text)
        tokens = self.pattern.split(text)
        sentences = [
            tokens[i].strip() + tokens[i + 1].strip()
            for i in range(0, len(tokens) - 1, 2)
        ]
        if len(tokens) % 2 == 1 and tokens[-1].strip():
            sentences.append(tokens[-1].strip())
        return sentences


class WordTokenizer:
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

    def __init__(self) -> None:
        self.pattern = re.compile(rf"([{re.escape(utils.punctuations)}])|\s+")

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes the input text into a list of words, keeping punctuations as separate tokens.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            List[str]: A list of tokenized words and punctuations.
        """
        tokens = self.pattern.split(text)
        return [token for token in tokens if token and not token.isspace()]

    def __call__(self, *args, **kwds):
        return self.tokenize(*args, **kwds)
