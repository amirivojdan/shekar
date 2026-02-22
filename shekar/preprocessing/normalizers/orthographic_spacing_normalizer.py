from shekar.base import BaseTextTransform
from shekar import data


class OrthographicSpacingNormalizer(BaseTextTransform):
    def __init__(self):
        super().__init__()

        _arabic_script = (
            r"\u0600-\u06FF"
            r"\u0750-\u077F"
            r"\u08A0-\u08FF"
            r"\uFB50-\uFDFF"
            r"\uFE70-\uFEFF"
        )

        # Remove invisible control marks except ZWNJ
        self._invisible_translation_table = dict.fromkeys(
            map(
                ord,
                "\u200b\u200d\u200e\u200f\u2066\u2067\u202a\u202b\u202d",
            ),
            None,
        )

        # Small orthographic corrections
        self._other_mappings = [
            (r"هها", f"ه{data.ZWNJ}ها"),
        ]

        # Core spacing + ZWNJ normalization rules (purely structural)
        self._spacing_mappings = [
            # Collapse horizontal whitespace (keep newlines)
            (r"[^\S\r\n]+", " "),
            # Reduce excessive newlines
            (r"\n{3,}", "\n\n"),
            # Remove ZWNJ around spaces
            (r"\u200c+(?= )|(?<= )\u200c+", ""),
            # Collapse multiple ZWNJs
            (r"\u200c{2,}", "\u200c"),
            # Remove ZWNJ at token edges (not between Persian chars/digits)
            (
                rf"(?<![{_arabic_script}0-9]){data.ZWNJ}+|"
                rf"{data.ZWNJ}+(?![{_arabic_script}0-9])",
                "",
            ),
            # Remove ZWNJ after non-left-joiner letters
            (rf"(?<=[{data.non_left_joiner_letters}]){data.ZWNJ}", ""),
            # Final collapse of extra spaces
            (r" {2,}", " "),
        ]

        self._spacing_patterns = self._compile_patterns(self._spacing_mappings)
        self._other_patterns = self._compile_patterns(self._other_mappings)

    def _function(self, text: str) -> str:
        if not text:
            return text

        # 1. Remove invisible unicode control marks
        text = text.translate(self._invisible_translation_table)

        # 2. Normalize structural spacing & ZWNJ
        text = self._map_patterns(text, self._spacing_patterns)

        # 3. Apply minor orthographic fixes
        text = self._map_patterns(text, self._other_patterns)

        return text.strip()
