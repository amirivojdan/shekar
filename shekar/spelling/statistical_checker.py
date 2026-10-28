from shekar import data
from shekar.base import BaseTransform
from shekar.morphology import Stemmer
from shekar.normalizer import Normalizer
from shekar.tokenization import WordTokenizer


class StatisticalSpellChecker(BaseTransform):
    """
    A statistical spell checker using Levenshtein distance and word frequencies.

    This class suggests corrections for misspelled Persian words based on edit distance
    and corpus-based word frequencies.
    """

    def __init__(
        self,
        n_edit=2,
        words: dict | None = None,
    ):
        """
        Initialize the AutoCorrect instance.
        Args:
            n_edit (int, optional): The maximum number of edits allowed for a word. Defaults to 2.
            words (Counter, optional): A Counter object containing words and their frequencies. if None, the default words will be loaded. Defaults to None.
        """

        if words is None:
            # Load the default words from data directory
            words = data.vocab

        self.normalizer = Normalizer()
        self.tokenizer = WordTokenizer()
        self.stemmer = Stemmer()
        self.n_words = sum(words.values())
        self.words = {word: freq / self.n_words for word, freq in words.items()}
        self.n_edit = n_edit
        self._index = None

    def _is_word_token(self, token: str) -> bool:
        """
        Check if token is a valid Persian word candidate for spell correction.
        """
        if not token:
            return False

        if all(ch in data.punctuations for ch in token):
            return False

        if all(ch in data.numbers for ch in token):
            return False

        # token should contain at least one Persian letter (or ZWNJ)
        has_persian = any(ch in data.persian_letters for ch in token)

        return has_persian

    @classmethod
    def generate_1edits(cls, word):
        deletes = [word[:i] + word[i + 1 :] for i in range(len(word))]
        inserts = [
            word[:i] + c + word[i:]
            for i in range(len(word) + 1)
            for c in data.persian_letters
        ]
        replaces = [
            word[:i] + c + word[i + 1 :]
            for i in range(len(word))
            for c in data.persian_letters
        ]
        transposes = [
            word[:i] + word[i + 1] + word[i] + word[i + 2 :]
            for i in range(len(word) - 1)
        ]
        return set(deletes + inserts + replaces + transposes)

    @classmethod
    def generate_n_edits(cls, word, n=1):
        edits_1 = cls.generate_1edits(word)
        if n == 1:
            return edits_1
        else:
            edits_n = set()
            for edit in edits_1:
                edits_n |= cls.generate_n_edits(edit, n=n - 1)
            return edits_n

    def _deletion_index(self) -> dict[str, str | tuple[str, ...]]:
        """
        Map every vocabulary word with one Persian letter deleted back to the word.

        Looking a string up here finds the known words one letter insertion away
        from it, so those candidates never have to be generated. Built on first use.
        """
        if self._index is None:
            index = {}
            for word in self.words:
                for i, ch in enumerate(word):
                    if ch not in data.persian_letters:
                        continue
                    key = word[:i] + word[i + 1 :]
                    entry = index.get(key)
                    if entry is None:
                        index[key] = word
                    elif isinstance(entry, str):
                        if entry != word:
                            index[key] = (entry, word)
                    elif word not in entry:
                        index[key] = (*entry, word)
            self._index = index
        return self._index

    def _known_1edits(self, word):
        """Return the vocabulary words in ``generate_1edits(word)``."""
        index = self._deletion_index()

        def indexed(key):
            entry = index.get(key, ())
            return (entry,) if isinstance(entry, str) else entry

        known = set()
        for i in range(len(word)):
            head, tail = word[:i], word[i + 1 :]
            if head + tail in self.words:
                known.add(head + tail)
            # Replacing word[i]: known words that differ from it only at position i.
            for candidate in indexed(head + tail):
                if (
                    len(candidate) == len(word)
                    and candidate[:i] == head
                    and candidate[i + 1 :] == tail
                    and candidate[i] in data.persian_letters
                ):
                    known.add(candidate)
        for i in range(len(word) - 1):
            transposed = word[:i] + word[i + 1] + word[i] + word[i + 2 :]
            if transposed in self.words:
                known.add(transposed)
        known.update(indexed(word))
        return known

    def correct(self, word, n_best=5):
        """
        Rank known words by edit distance, then by frequency, then alphabetically.

        Matches ranking each ``generate_n_edits(word, n)`` level in turn, without
        generating the insertions and substitutions of the final level.
        """
        suggestions = [word] if word in self.words else []
        seen = set(suggestions)
        frontier = {word}
        for n in range(1, self.n_edit + 1):
            # Later levels only rank below the suggestions already found.
            if len(suggestions) >= n_best:
                break
            known = set().union(*map(self._known_1edits, frontier)) - seen
            suggestions += sorted(known, key=lambda w: (-self.words[w], w))
            seen |= known
            if n < self.n_edit:
                frontier = set().union(*map(self.generate_1edits, frontier))

        return suggestions[:n_best]

    def suggest(self, word, n_best=5):
        """
        Suggest corrections for a given word.
        """
        return self.correct(word, n_best=n_best)

    def correct_text(self, text):
        text = self.normalizer(text)
        tokens = self.tokenizer.tokenize(text)
        corrected_tokens = []
        for token in tokens:
            # Only correct valid word tokens, skip all other tokens (punctuations, numbers, etc.)
            if not self._is_word_token(token) or token in self.words:
                corrected_tokens.append(token)
                continue

            stem = self.stemmer(token)
            if stem != token and stem in self.words:
                corrected_tokens.append(token)
                continue

            suggestions = self.correct(token)
            if suggestions:
                corrected_tokens.append(suggestions[0])
            else:
                corrected_tokens.append(token)
        return self.normalizer(" ".join(corrected_tokens))

    def transform(self, X: str) -> str:
        """
        Correct a given text using the spell checker.

        Args:
            X (str): The input text to be corrected.

        Returns:
            str: The corrected text.
        """
        return self.correct_text(X)
