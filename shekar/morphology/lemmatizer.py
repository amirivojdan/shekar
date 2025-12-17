from shekar.base import BaseTextTransform
from .stemmer import Stemmer
from shekar import data
from .conjugator import get_conjugated_verbs


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

    def __init__(self, return_infinitive=False):
        super().__init__()
        self.stemmer = Stemmer()
        self.return_infinitive = return_infinitive

    def _function(self, text):
        conjugated_verbs = get_conjugated_verbs()

        if text in conjugated_verbs:
            (past_stem, present_stem) = conjugated_verbs[text]
            if past_stem is None:
                return present_stem
            if self.return_infinitive:
                return past_stem + "ن"
            return past_stem + "/" + present_stem

        stem = self.stemmer(text)
        if stem and stem in data.vocab:
            return stem

        if text in data.vocab:
            return text

        return text
