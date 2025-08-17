from shekar.base import BaseTextTransform
from .stemmer import Stemmer
from shekar import data


class Lemmatizer(BaseTextTransform):
    """
    A rule-based lemmatizer for Persian text.

    This class reduces words to their lemma (dictionary form) using a combination
    of verb conjugation mappings, a stemming algorithm, and a vocabulary lookup.
    It prioritizes explicit mappings of conjugated verbs, then falls back to a
    stemmer and vocabulary checks.

    Example:
        >>> lemmatizer = Lemmatizer()
        >>> lemmatizer("رفتند")
        'رفت/رو'
        >>> lemmatizer("کتاب‌ها")
        'کتاب'

    """

    def __init__(self):
        super().__init__()
        self.stemmer = Stemmer()

    def _function(self, text):
        if text in data.conjugated_verbs:
            (past_stem, present_stem) = data.conjugated_verbs[text]
            return past_stem + "/" + present_stem

        stem = self.stemmer(text)
        if stem and stem in data.vocab:
            return stem

        if text in data.vocab:
            return text

        return text
