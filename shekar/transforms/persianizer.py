from flashtext import KeywordProcessor
from shekar.base import BaseTextTransform
from shekar import data


class Persianizer(BaseTextTransform):
    """
    A text transformation class for suggesting and substituting Persian alternatives for loanwords and foreign words in Persian text.
    The loanword mapping data is sourced from beparsi.com, which publishes and makes this data publicly available.
    """

    def __init__(self):
        super().__init__()
        self._processor = KeywordProcessor()
        for word in data.loanwords:
            self._processor.add_keyword(word)

    def _function(self, text: str) -> str:
        matches = self._processor.extract_keywords(text, span_info=True)
        for match, start, end in reversed(matches):
            first_alt = data.loanwords[match].split(";")[0].strip()
            text = text[:start] + first_alt + text[end:]
        return text

    def suggest(self, text: str) -> list[tuple[list[str], tuple[int, int]]]:
        """
        Returns all loanwords found in the text with their Persian alternatives and positions.
        Each item is (alternatives, (start_index, end_index)).
        """
        results = []
        for match, start, end in self._processor.extract_keywords(text, span_info=True):
            alternatives = [alt.strip() for alt in data.loanwords[match].split(";")]
            results.append((alternatives, (start, end)))
        return results
