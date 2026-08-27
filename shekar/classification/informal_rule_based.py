from functools import lru_cache

from flashtext import KeywordProcessor

from shekar import data
from shekar.base import BaseTransform
from shekar.morphology.conjugator import Conjugator


@lru_cache(maxsize=1)
def _get_informal_conjugations() -> frozenset[str]:
    conjugator = Conjugator()
    formal_forms: set[str] = set()
    informal_forms: set[str] = set()

    for (
        past_stem,
        present_stem,
        informal_past_stem,
        informal_present_stem,
    ) in data.verbs:
        base_past_stem, prefix = conjugator.get_verb_prefix(past_stem)
        base_present_stem, _ = conjugator.get_verb_prefix(present_stem)
        informal_base_past_stem, _ = conjugator.get_verb_prefix(informal_past_stem)
        informal_base_present_stem, _ = conjugator.get_verb_prefix(
            informal_present_stem
        )

        formal, informal = conjugator.conjugate(
            base_past_stem,
            base_present_stem,
            informal_base_past_stem,
            informal_base_present_stem,
            prefix=prefix,
        )

        formal_forms.update(formal)
        informal_forms.update(informal)

    return frozenset(
        form for form in informal_forms - formal_forms if form not in data.vocab
    )


class RuleBasedInformalClassifier(BaseTransform):
    """A simple rule-based classifier for informal language based on keyword matching.
    It uses a predefined list of informal words and conjugated verbs to determine if a sentence is informal.
    The occurrence_threshold parameter allows tuning the sensitivity of the classifier.
    Inspired by https://github.com/MahtaFetrat/Persian-Informal-Text-Detector
    """

    def __init__(self, model_path=None, occurrence_threshold=1):
        super().__init__()
        self._kp = KeywordProcessor()
        self._kp.non_word_boundaries |= {chr(c) for c in range(0x0600, 0x0700)}
        self._kp.add_keywords_from_list(list(_get_informal_conjugations()))
        self._kp.add_keywords_from_list(list(data.informal_words.keys()))
        self.occurrence_threshold = occurrence_threshold

    def transform(self, X: str) -> tuple:
        count = len(self._kp.extract_keywords(X))
        label = 1 if count >= self.occurrence_threshold else 0
        return ("informal", label)

    def is_informal(self, X: str) -> bool:
        return self.transform(X)[1] == 1
