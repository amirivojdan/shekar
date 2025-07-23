from collections import Counter
from shekar.tokenization import WordTokenizer
from shekar import data


class StatisticalSpellChecker:
    """
        A statistical spell checker using Levenshtein distance and word frequencies.

        This class suggests corrections for misspelled Persian words based on edit distance 
        and corpus-based word frequencies.
    """

    def __init__(
        self,
        n_edit=2,
        words: Counter = None,
    ):
        """
        Initialize the AutoCorrect instance.
        Args:
            n_edit (int, optional): The maximum number of edits allowed for a word. Defaults to 2.
            words (Counter, optional): A Counter object containing words and their frequencies. if None, the default words will be loaded. Defaults to None.
        """

        if words is None:
            # Load the default words from data directory
            pass

        self.tokenizer = WordTokenizer()
        self.n_words = sum(words.values())
        self.words = {word: freq / self.n_words for word, freq in words.items()}
        self.n_edit = n_edit

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

    def correct(self, word, n_best=5):
        suggestions = []
        if word in self.words:
            suggestions.append((word, self.words[word]))

        for n in range(1, self.n_edit + 1):
            suggestions += sorted(
                [
                    (w, self.words[w])
                    for w in self.generate_n_edits(word, n=n)
                    if w in self.words
                ],
                key=lambda x: x[1],
                reverse=True,
            )

        seen = set()
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion[0] not in seen:
                unique_suggestions.append(suggestion[0])
            seen.add(suggestion[0])

        return unique_suggestions[:n_best]

    def correct_text(self, text):
        tokens = self.tokenizer.tokenize(text)
        return " ".join(self.correct(token)[0] for token in tokens)
