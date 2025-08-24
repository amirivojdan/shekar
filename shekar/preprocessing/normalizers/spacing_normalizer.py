from functools import partial
from typing import Set
from shekar.base import BaseTextTransform
from shekar import data
import re


class SpacingNormalizer(BaseTextTransform):
    """
    Standardizes spacing in the text regarding the offical Persian script standard published by the Iranian Academy of Language and Literature.
    reference: https://apll.ir/
    This class is also used to remove extra spaces, newlines, zero width nonjoiners, and other unicode space characters.
    """

    def __init__(self):
        super().__init__()

        self._other_mappings = [
            (r"هها", f"ه{data.ZWNJ}ها"),
        ]

        self._spacing_mappings = [
            (
                r"[\u200b\u200d\u200e\u200f\u2066\u2067\u202a\u202b\u202d]",
                "",
            ),  # Remove invisible control marks except ZWNJ
            (
                r"[^\S\r\n]+",
                " ",
            ),  # Collapse all horizontal whitespace (except newlines) to a single space
            (r"\n{3,}", "\n\n"),  # Reduce 3+ newlines to exactly 2
            (r"\u200c+(?= )|(?<= )\u200c+", ""),  # Remove ZWNJ before or after a space
            (r"\u200c{2,}", "\u200c"),  # Collapse multiple ZWNJs
            (
                r"(?<![\p{Arabic}0-9])\u200c+|\u200c+(?![\p{Arabic}0-9])",
                "",
            ),  # Remove ZWNJ at edges of tokens (not between Arabic letters/digits)
            (r" {2,}", " "),  # Final collapse of extra spaces
            # Remove ZWNJ after non-left-joiner letters
            (rf"(?<=[{data.non_left_joiner_letters}]){data.ZWNJ}", ""),
        ]

        self._punctuation_spacing_mappings = [
            (r"([{op}])\s+".format(op=re.escape(data.opener_punctuations)), r"\1"),
            (r"\s+([{cl}])".format(cl=re.escape(data.closer_punctuations)), r"\1"),
            (
                r"(?<=\S)\s*([{op}])".format(op=re.escape(data.opener_punctuations)),
                r" \1",
            ),
            (
                r"([{cl}])(?=(?![{sg}{cl}])\S)".format(
                    cl=re.escape(data.closer_punctuations),
                    sg=re.escape(data.single_punctuations),
                ),
                r"\1 ",
            ),
            (r"\s+([{sg}])".format(sg=re.escape(data.single_punctuations)), r"\1"),
            (
                r"([{sg}])(?=(?![{cl}])\S)".format(
                    sg=re.escape(data.single_punctuations),
                    cl=re.escape(data.closer_punctuations),
                ),
                r"\1 ",
            ),
            (r"^\s+|\s+$", ""),
        ]

        self._mi_joined_pattern = re.compile(
            rf"(?<!\S)(?P<prefix>ن?می)(?![ ‌])(?P<stem>[{data.persian_letters}]+)"
        )

        self._mi_space_pattern = re.compile(
            rf"(?<!\S)(?P<prefix>ن?می)\s+(?P<stem>[{data.persian_letters}]+)"
        )

        _verbal_suffix_alt = "|".join(
            map(re.escape, ["ام", "ای", "است", "ایم", "اید", "اند"])
        )
        _punc_class = re.escape(data.punctuations)
        self._verbal_suffix_space_pattern = re.compile(
            rf"(?<!\S)(?P<stem>[{data.persian_letters}]+)\s+(?P<suffix>(?:{_verbal_suffix_alt}))(?=$|[\s{_punc_class}])"
        )

        _word_prefix_alt = "|".join(map(re.escape, data.prefixes))
        self._word_prefix_space_pattern = re.compile(
            rf"(?<!\S)(?P<prefix>(?:{_word_prefix_alt}))\s+(?P<stem>[{data.persian_letters}]+)(?=$|[\s{_punc_class}])"
        )

        _word_suffix_alt = "|".join(map(re.escape, data.suffixes))
        self._word_suffix_space_pattern = re.compile(
            rf"(?<!\S)(?P<stem>[{data.persian_letters}]+)\s+(?P<suffix>(?:{_word_suffix_alt}))(?=$|[\s{_punc_class}])"
        )

        self._punctuation_spacing_patterns = self._compile_patterns(
            self._punctuation_spacing_mappings
        )
        self._spacing_patterns = self._compile_patterns(self._spacing_mappings)
        self._other_patterns = self._compile_patterns(self._other_mappings)

        self.verbal_prefix_corrector = partial(
            self._prefix_spacing, vocab=data.conjugated_verbs
        )
        self.verbal_suffix_corrector = partial(
            self._suffix_spacing, vocab=data.conjugated_verbs
        )

        self._word_suffix_corrector = partial(
            self._suffix_spacing, vocab=data.vocab, only_stem=True
        )

        self._word_prefix_corrector = partial(
            self._prefix_spacing, vocab=data.vocab, only_stem=True
        )

        self.compound_words_pattern = re.compile(
            "|".join(map(re.escape, data.compound_words_space.keys()))
        )

    def _compound_replacer(self, m):
        return data.compound_words_space[m.group(0)]

    def _prefix_spacing(
        self, m: re.Match, vocab: Set[str], only_stem: bool = False
    ) -> str:
        prefix = m.group("prefix")
        stem = m.group("stem")
        if prefix[-1] in data.non_left_joiner_letters:
            candidate = f"{prefix}{stem}"
        else:
            candidate = f"{prefix}{data.ZWNJ}{stem}"
        if only_stem:
            return candidate if stem in vocab else m.group(0)
        return candidate if candidate in vocab else m.group(0)

    def _suffix_spacing(
        self, m: re.Match, vocab: Set[str], only_stem: bool = False
    ) -> str:
        stem = m.group("stem")
        suffix = m.group("suffix")
        if stem[-1] in data.non_left_joiner_letters:
            candidate = f"{stem}{suffix}"
        else:
            candidate = f"{stem}{data.ZWNJ}{suffix}"
        if only_stem:
            return candidate if stem in vocab else m.group(0)
        return candidate if candidate in vocab else m.group(0)

    def _function(self, text: str) -> str:
        text = self._map_patterns(text, self._spacing_patterns)
        text = self._map_patterns(text, self._other_patterns)
        text = self._map_patterns(text, self._punctuation_spacing_patterns).strip()

        text = self._word_prefix_space_pattern.sub(self._word_prefix_corrector, text)
        text = self._word_suffix_space_pattern.sub(self._word_suffix_corrector, text)

        # Apply the verbal suffix spacing patterns
        text = self._verbal_suffix_space_pattern.sub(self.verbal_suffix_corrector, text)

        # Apply the mi spacing patterns
        text = self._mi_space_pattern.sub(self.verbal_prefix_corrector, text)
        text = self._mi_joined_pattern.sub(self.verbal_prefix_corrector, text)

        text = self.compound_words_pattern.sub(self._compound_replacer, text)

        return text.strip()
