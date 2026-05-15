from flashtext import KeywordProcessor
from shekar.base import BaseTransform
from shekar.morphology.conjugator import get_informal_conjugated_verbs
from shekar import data


class RuleBasedInformalClassifier(BaseTransform):
    def __init__(self, model_path=None, occurrence_threshold=1):
        super().__init__()
        self._kp = KeywordProcessor()
        self._kp.non_word_boundaries |= set(chr(c) for c in range(0x0600, 0x0700))
        self._kp.add_keywords_from_list(list(get_informal_conjugated_verbs().keys()))
        self._kp.add_keywords_from_list(list(data.informal_words.keys()))
        self.occurrence_threshold = occurrence_threshold

    def transform(self, X: str) -> tuple:
        count = len(self._kp.extract_keywords(X))
        label = 1 if count >= self.occurrence_threshold else 0
        return ("informal", label)

    def is_informal(self, X: str) -> bool:
        return self.transform(X)[1] == 1
