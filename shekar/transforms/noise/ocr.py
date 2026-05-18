from shekar.base import BaseTextTransform


class OCRNoise(BaseTextTransform):
    """Simulates OCR errors by perturbing characters based on visual similarity.

    For each character that has known OCR confusions, the following operations
    are tried in order: deletion, repeat, substitution. Each operation is an
    independent Bernoulli trial with its own probability, but they are evaluated
    in priority order and at most one fires per character. Characters without
    known confusions (spaces, punctuation, unmapped glyphs) always pass through
    unchanged.
    """

    def __init__(
        self,
        substitution_prob=0.02,
        deletion_prob=0.005,
        repeat_prob=0.005,
        seed=None,
    ):
        import random

        for name, value in (
            ("substitution_prob", substitution_prob),
            ("deletion_prob", deletion_prob),
            ("repeat_prob", repeat_prob),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0.0, 1.0], got {value}.")

        self.substitution_prob = substitution_prob
        self.deletion_prob = deletion_prob
        self.repeat_prob = repeat_prob
        self._rng = random.Random(seed)
        self._ocr_confusions = {
            "ب": ["پ", "ت", "ث"],
            "پ": ["ب", "ت"],
            "ت": ["ب", "پ", "ث"],
            "ث": ["ت", "ش"],
            "ج": ["چ", "ح", "خ"],
            "ح": ["ج", "خ"],
            "خ": ["ح"],
            "س": ["ش", "ص"],
            "ش": ["س", "ث"],
            "ص": ["س", "ض"],
            "ض": ["ص"],
            "ط": ["ظ"],
            "ظ": ["ط"],
            "ق": ["ف"],
            "ف": ["ق"],
            "ع": ["غ"],
            "غ": ["ع", "خ", "ف"],
            "د": ["ذ"],
            "ر": ["ز"],
            "و": ["ن"],
            "ک": ["گ", "ك"],
            "گ": ["ک", "ك"],
            "ه": ["ة"],
            "ی": ["ئ"],
            "ئ": ["ی"],
            "۱": ["ل"],
            "۰": ["."],
        }

    def _function(self, text: str) -> str:
        result = []
        for char in text:
            if char not in self._ocr_confusions:
                result.append(char)
                continue

            if self._rng.random() < self.deletion_prob:
                continue

            if self._rng.random() < self.repeat_prob:
                result.append(char)
                result.append(char)
                continue

            if self._rng.random() < self.substitution_prob:
                result.append(self._rng.choice(self._ocr_confusions[char]))
                continue

            result.append(char)

        return "".join(result)
