import random
from shekar.base import BaseTextTransform


class KeyboardNoise(BaseTextTransform):
    """Simulates keyboard typos by perturbing characters based on adjacency
    on the standard Persian keyboard layout.

    For each character that exists on the keyboard, the following operations
    are tried in order: deletion, insertion, repeat, substitution, shift.
    Each operation is an independent Bernoulli trial with its own probability,
    but they are evaluated in priority order and at most one fires per
    character. As a result, the *effective* rate of a later operation is
    conditional on no earlier operation having fired. Every
    probability is independently valid in [0.0, 1.0].

    Characters not on the keyboard layout (spaces, ZWNJ, newlines, unmapped
    punctuation) always pass through unchanged.
    """

    def __init__(
        self,
        substitution_prob=0.01,
        insertion_prob=0.01,
        deletion_prob=0.01,
        repeat_prob=0.01,
        shifted_prob=0.005,
        shift_letters=False,
        seed=None,
    ):
        for name, value in (
            ("substitution_prob", substitution_prob),
            ("insertion_prob", insertion_prob),
            ("deletion_prob", deletion_prob),
            ("repeat_prob", repeat_prob),
            ("shifted_prob", shifted_prob),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0.0, 1.0], got {value}.")

        self.substitution_prob = substitution_prob
        self.insertion_prob = insertion_prob
        self.deletion_prob = deletion_prob
        self.repeat_prob = repeat_prob
        self.shifted_prob = shifted_prob
        self.shift_letters = shift_letters

        self._rng = random.Random(seed)

        self.keyboard_layout = [
            "1234567890-=",
            "ضصثقفغعهخحجچپ",
            "شسیبلاتنمکگ",
            "ظطزرذدئو./",
        ]

        self.shifted_keyboard_layout = [
            "!@#$%^&*)(_+",
            r"ًٌٍ﷼،؛,][\}{|",
            'َُِّۀآـ«»:"',
            "ةيژؤأإء<>؟",
        ]

        for i, (row, shifted_row) in enumerate(
            zip(self.keyboard_layout, self.shifted_keyboard_layout)
        ):
            if len(row) != len(shifted_row):
                raise ValueError(
                    f"Keyboard layout row {i} length mismatch: "
                    f"base={len(row)}, shifted={len(shifted_row)}."
                )

        self._position = {
            char: (r, c)
            for r, row in enumerate(self.keyboard_layout)
            for c, char in enumerate(row)
        }

        if shift_letters:
            self._shiftable = set(self._position)
        else:
            self._shiftable = {ch for ch in self._position if not ch.isalpha()}

        self.neighbor_map = self._build_neighbor_map(self.keyboard_layout)

    def _build_neighbor_map(self, layout):
        neighbor_map = {}
        for r, row in enumerate(layout):
            for i, char in enumerate(row):
                neighbors = set()
                if i > 0:
                    neighbors.add(row[i - 1])  # left
                if i < len(row) - 1:
                    neighbors.add(row[i + 1])  # right

                for dr in (-1, 1):
                    nr = r + dr
                    if 0 <= nr < len(layout):
                        adj_row = layout[nr]
                        nc = min(i, len(adj_row) - 1)
                        neighbors.add(adj_row[nc])
                neighbors.discard(char)
                neighbor_map[char] = neighbors
        return neighbor_map

    def _shifted_char(self, char):
        r, c = self._position[char]
        return self.shifted_keyboard_layout[r][c]

    def _function(self, text: str) -> str:
        result = []
        for char in text:
            if char not in self.neighbor_map:
                result.append(char)
                continue

            neighbors = self.neighbor_map[char]

            if self._rng.random() < self.deletion_prob:
                continue

            if self._rng.random() < self.insertion_prob and neighbors:
                result.append(self._rng.choice(sorted(neighbors)))
                result.append(char)
                continue

            if self._rng.random() < self.repeat_prob:
                result.append(char)
                result.append(char)
                continue

            if self._rng.random() < self.substitution_prob and neighbors:
                result.append(self._rng.choice(sorted(neighbors)))
                continue

            if char in self._shiftable and self._rng.random() < self.shifted_prob:
                result.append(self._shifted_char(char))
                continue

            result.append(char)

        return "".join(result)
