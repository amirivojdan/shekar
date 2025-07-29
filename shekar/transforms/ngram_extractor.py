from shekar.base import BaseTextTransform
from shekar.tokenization import WordTokenizer


class NGramExtractor(BaseTextTransform):
    """
    A text transformation class for extracting n-grams from the text.
    This class inherits from `BaseTextTransformer` and provides functionality to extract
    n-grams from the text. It allows for the specification of the range of n-grams to be extracted,
    ensuring flexibility in the extraction process.
    The `NGramExtractor` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.
    Args:
        range (tuple[int, int]): The range of n-grams to be extracted. Default is (1, 2).
    Methods:
        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by extracting n-grams.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.
        __call__(text: str) -> list[str]:
            Allows the class to be called as a function, applying the transformation
            to the input text and returning a list of n-grams.
    Example:
        >>> ngram_extractor = NGramExtractor(range=(1, 3))
        >>> ngrams = ngram_extractor("این یک متن نمونه است.")
        >>> print(ngrams)
        ["این", "یک", "متن", "نمونه", "است", "این یک", "یک متن", "متن نمونه", "نمونه است"]
    """

    def __init__(self, range: tuple[int, int] = (1, 1)):
        super().__init__()
        if not isinstance(range, tuple) or not all(isinstance(i, int) for i in range):
            raise TypeError("N-gram range must be a tuple tuple of integers.")
        elif len(range) != 2:
            raise ValueError("N-gram range must be a tuple of length 2.")
        elif range[0] < 1 or range[1] < 1:
            raise ValueError("N-gram range must be greater than 0.")
        elif range[0] > range[1]:
            raise ValueError("N-gram range must be in the form of (min, max).")

        self.range = range
        self.word_tokenizer = WordTokenizer()

    def _function(self, text: str) -> list[str]:
        tokens = list(self.word_tokenizer(text))
        ngrams = []
        for n in range(self.range[0], self.range[1] + 1):
            ngrams.extend(
                [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]
            )
        return ngrams
