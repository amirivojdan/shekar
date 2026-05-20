import random
from shekar.base import BaseTextTransform
from shekar.data import ZWNJ


class WhitespaceNoise(BaseTextTransform):
    """Corrupts whitespace structure in Persian text.

    Each ZWNJ is independently deleted, replaced with a space, or kept.
    Each space is independently deleted, replaced with a ZWNJ, or kept.
    Deletion is checked before substitution, so both cannot fire on the
    same character.
    """

    def __init__(
        self,
        zwnj_deletion_prob=0.3,
        zwnj_to_space_prob=0.1,
        space_deletion_prob=0.1,
        space_to_zwnj_prob=0.1,
        seed=None,
    ):
        for name, value in (
            ("zwnj_deletion_prob", zwnj_deletion_prob),
            ("zwnj_to_space_prob", zwnj_to_space_prob),
            ("space_deletion_prob", space_deletion_prob),
            ("space_to_zwnj_prob", space_to_zwnj_prob),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0.0, 1.0], got {value}.")

        self.zwnj_deletion_prob = zwnj_deletion_prob
        self.zwnj_to_space_prob = zwnj_to_space_prob
        self.space_deletion_prob = space_deletion_prob
        self.space_to_zwnj_prob = space_to_zwnj_prob
        self._rng = random.Random(seed)

    def _function(self, text: str) -> str:
        result = []
        for char in text:
            if char == ZWNJ:
                if self._rng.random() < self.zwnj_deletion_prob:
                    continue
                if self._rng.random() < self.zwnj_to_space_prob:
                    result.append(" ")
                    continue
                result.append(char)
            elif char == " ":
                if self._rng.random() < self.space_deletion_prob:
                    continue
                if self._rng.random() < self.space_to_zwnj_prob:
                    result.append(ZWNJ)
                    continue
                result.append(char)
            else:
                result.append(char)
        return "".join(result)
