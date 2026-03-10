from collections import defaultdict
from math import log

from shekar import BaseTransform
from shekar.preprocessing import RemoveStopWords, RemovePunctuations, RemoveDigits
from shekar.tokenization import SentenceTokenizer, WordTokenizer


class TextRank(BaseTransform):
    """
    Extracts keywords using the TextRank graph-based ranking algorithm.

    Words are nodes in a co-occurrence graph; edges are weighted by how often
    two words appear within the same window.  PageRank-style scores are
    computed iteratively and the top-n words (or multi-word phrases built from
    adjacent high-scoring words) are returned.
    """

    def __init__(self, max_length=3, top_n=5, window=2, damping=0.85, iterations=30):
        self._sentence_tokenizer = SentenceTokenizer()
        self._word_tokenizer = WordTokenizer()
        self._preprocessor = (
            RemoveStopWords(mask_token="|")
            | RemovePunctuations(mask_token="|")
            | RemoveDigits(mask_token="|")
        )
        self.top_n = top_n
        self.window = window
        self.damping = damping
        self.iterations = iterations
        self.max_length = max_length
        super().__init__()

    def _tokenize_sentences(self, text: str) -> list[list[str]]:
        """Return a list of sentences, each as a list of clean word tokens."""
        sentences = []
        for sentence in self._sentence_tokenizer.tokenize(text):
            clean = self._preprocessor(sentence)
            words = []
            for segment in clean.split("|"):
                for w in self._word_tokenizer.tokenize(segment):
                    w = w.strip()
                    if len(w) > 1:
                        words.append(w)
            if words:
                sentences.append(words)
        return sentences

    def _build_graph(self, sentences: list[list[str]]) -> dict[str, dict[str, float]]:
        """Build a co-occurrence graph with edge weights = co-occurrence count."""
        graph: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        for words in sentences:
            for i, word in enumerate(words):
                start = max(0, i - self.window)
                end = min(len(words), i + self.window + 1)
                for j in range(start, end):
                    if i != j:
                        graph[word][words[j]] += 1.0
                        graph[words[j]][word] += 1.0
        return graph

    def _pagerank(self, graph: dict[str, dict[str, float]]) -> dict[str, float]:
        """Iterative PageRank computation."""
        nodes = list(graph.keys())
        if not nodes:
            return {}

        scores = {n: 1.0 / len(nodes) for n in nodes}

        for _ in range(self.iterations):
            new_scores: dict[str, float] = {}
            for node in nodes:
                rank = 0.0
                for neighbor, weight in graph[node].items():
                    out_weight = sum(graph[neighbor].values()) or 1.0
                    rank += (weight / out_weight) * scores.get(neighbor, 0.0)
                new_scores[node] = (1 - self.damping) + self.damping * rank
            scores = new_scores

        return scores

    def _extract_keyphrases(
        self, sentences: list[list[str]], scores: dict[str, float]
    ) -> dict[str, float]:
        """
        Combine adjacent high-scoring words into multi-word keyphrases.
        The phrase score is the average of its constituent word scores,
        boosted logarithmically by phrase length (longer phrases are rarer
        and more specific).
        """
        candidates: dict[str, float] = {}
        for words in sentences:
            i = 0
            while i < len(words):
                if words[i] not in scores:
                    i += 1
                    continue
                phrase_words = [words[i]]
                j = i + 1
                while j < len(words) and j - i < self.max_length and words[j] in scores:
                    phrase_words.append(words[j])
                    j += 1
                phrase = " ".join(phrase_words)
                phrase_score = (
                    sum(scores[w] for w in phrase_words) / len(phrase_words)
                ) * (1 + log(len(phrase_words)))
                if phrase not in candidates or candidates[phrase] < phrase_score:
                    candidates[phrase] = phrase_score
                i = j if j > i + 1 else i + 1
        return candidates

    def transform(self, X: str) -> list[str]:
        sentences = self._tokenize_sentences(X)
        graph = self._build_graph(sentences)
        scores = self._pagerank(graph)
        candidates = self._extract_keyphrases(sentences, scores)
        return [
            kw
            for kw, _ in sorted(candidates.items(), key=lambda x: x[1], reverse=True)[
                : self.top_n
            ]
        ]
