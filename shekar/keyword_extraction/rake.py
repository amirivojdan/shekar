from shekar import BaseTransform
from shekar.preprocessing import (
    RemoveStopWords,
    RemovePunctuations,
    RemoveDigits,
)

from shekar.transforms import (
    Flatten,
    NGramExtractor,
)

from collections import defaultdict
from shekar.tokenization import SentenceTokenizer, WordTokenizer


class RAKE(BaseTransform):
    """
    Extracts keywords from text using tokenization, filtering, and frequency-based scoring.
    """

    def __init__(self, max_length=3, top_n=5):
        self._sentence_tokenizer = SentenceTokenizer()
        self._word_tokenizer = WordTokenizer()
        self._preprocessor = (
            RemoveStopWords(replace_with="|")
            | RemovePunctuations(replace_with="|")
            | RemoveDigits(replace_with="|")
        )
        self._ngram_extractor = NGramExtractor(range=(1, max_length)) | Flatten()
        self.top_n = top_n
        super().__init__()

    def _extract_phrases(self, text: str) -> list[str]:
        phrases = []
        for sentence in self._sentence_tokenizer.tokenize(text):
            clean_sentence = self._preprocessor(sentence)
            for phrase in (p.strip() for p in clean_sentence.split("|")):
                if phrase:
                    ngrams = list(self._ngram_extractor(phrase))
                    phrases.extend([ng for ng in ngrams if len(ng) > 2])
        return phrases

    def _calculate_word_scores(self, phrases: list[str]) -> dict[str, float]:
        word_frequency = defaultdict(int)
        word_degree = defaultdict(int)
        for phrase in phrases:
            words = [
                w.strip() for w in self._word_tokenizer.tokenize(phrase) if len(w) > 2
            ]
            degree = len(words) - 1
            for word in words:
                word_frequency[word] += 1
                word_degree[word] += degree
        return {
            word: (word_degree[word] + word_frequency[word]) / word_frequency[word]
            for word in word_frequency
        }

    def _generate_candidate_keyword_scores(
        self, phrases: list[str], word_scores: dict[str, float]
    ) -> dict[str, float]:
        candidates = {}
        for phrase in phrases:
            words = [
                w.strip() for w in self._word_tokenizer.tokenize(phrase) if len(w) > 2
            ]
            candidates[phrase] = sum(word_scores.get(word, 0) for word in words)
        return candidates

    def transform(self, X: str) -> list[str]:
        phrases = self._extract_phrases(X)
        word_scores = self._calculate_word_scores(phrases)
        candidates = self._generate_candidate_keyword_scores(phrases, word_scores)
        return [
            kw
            for kw, score in sorted(
                candidates.items(), key=lambda x: x[1], reverse=True
            )[: self.top_n]
        ]
