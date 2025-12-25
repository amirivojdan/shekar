from functools import partial
from typing import Set
from shekar.base import BaseTextTransform
from shekar import data
from shekar.morphology.conjugator import get_conjugated_verbs
import re
from flashtext import KeywordProcessor


class SpacingNormalizer(BaseTextTransform):
    """
    Standardizes spacing in the text regarding the offical Persian script standard published by the Iranian Academy of Language and Literature.
    reference: https://apll.ir/
    This class is also used to remove extra spaces, newlines, zero width nonjoiners, and other unicode space characters.
    """

    def __init__(self):
        super().__init__()

        self.conjugated_verbs = get_conjugated_verbs()
        compound_words = data.compound_words - set(self.conjugated_verbs.keys())

        self.compound_kp = KeywordProcessor(case_sensitive=True)
        for correct_word in compound_words:
            if "#" not in correct_word:
                self.compound_kp.add_keyword(
                    correct_word.replace(data.ZWNJ, " "), correct_word
                )
            else:
                self.compound_kp.add_keyword(
                    correct_word.replace("#", " "), correct_word.replace("#", "")
                )

        self._other_mappings = [
            (r"هها", f"ه{data.ZWNJ}ها"),
        ]

        _arabic_script = (
            r"\u0600-\u06FF"  # Arabic
            r"\u0750-\u077F"  # Arabic Supplement
            r"\u08A0-\u08FF"  # Arabic Extended-A
            r"\uFB50-\uFDFF"  # Arabic Presentation Forms-A
            r"\uFE70-\uFEFF"  # Arabic Presentation Forms-B
        )

        # Remove invisible control marks except ZWNJ
        self._invisible_translation_table = dict.fromkeys(
            map(ord, "\u200b\u200d\u200e\u200f\u2066\u2067\u202a\u202b\u202d"),
            None,
        )

        self._spacing_mappings = [
            (
                r"[^\S\r\n]+",
                " ",
            ),  # Collapse all horizontal whitespace (except newlines) to a single space
            (r"\n{3,}", "\n\n"),  # Reduce 3+ newlines to exactly 2
            (r"\u200c+(?= )|(?<= )\u200c+", ""),  # Remove ZWNJ before or after a space
            (r"\u200c{2,}", "\u200c"),  # Collapse multiple ZWNJs
            (
                rf"(?<![{_arabic_script}0-9]){data.ZWNJ}+|{data.ZWNJ}+(?![{_arabic_script}0-9])",
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

        _morph_suffix_alt = "|".join(map(re.escape, data.morph_suffixes))
        self._morph_suffix_space_pattern = re.compile(
            rf"(?<!\S)(?P<stem>[{data.persian_letters}]+)\s+(?P<suffix>(?:{_morph_suffix_alt}))(?=$|[\s{_punc_class}])"
        )

        _verbal_prefixes_alt = "|".join(map(re.escape, data.verbal_prefixes))
        self._preverb_mi_stem_pattern = re.compile(
            rf"(?<!\S)"
            rf"(?P<preverb>(?:{_verbal_prefixes_alt}))"
            rf"(?:{data.ZWNJ}|\s+|)"
            rf"(?:(?P<mi>ن?می)(?:{data.ZWNJ}|\s+|))?"
            rf"(?P<verb>[{data.persian_letters}]+)"
            rf"(?=$|[\s{_punc_class}])"
        )

        _prefixed_simple_future_alt = "|".join(
            map(re.escape, ["خواهم", "خواهی", "خواهد", "خواهیم", "خواهید", "خواهند"])
        )
        self._prefixed_simple_future_pattern = re.compile(
            rf"(?<!\S)"
            rf"(?P<preverb>(?:{_verbal_prefixes_alt}))"
            rf"(?:{data.ZWNJ}|\s+|)"
            rf"(?P<aux>ن?(?:{_prefixed_simple_future_alt}))"
            rf"(?:{data.ZWNJ}|\s+|)"
            rf"(?P<verb>[{data.persian_letters}]+)"
            rf"(?=$|[\s{_punc_class}])"
        )

        self._punctuation_spacing_patterns = self._compile_patterns(
            self._punctuation_spacing_mappings
        )
        self._spacing_patterns = self._compile_patterns(self._spacing_mappings)
        self._other_patterns = self._compile_patterns(self._other_mappings)

        self.verbal_prefix_corrector = partial(
            self._prefix_spacing, vocab=self.conjugated_verbs
        )
        self.verbal_suffix_corrector = partial(
            self._suffix_spacing, vocab=self.conjugated_verbs
        )

        self._word_suffix_corrector = partial(
            self._suffix_spacing,
            vocab=data.vocab,
        )

        self._word_prefix_corrector = partial(
            self._prefix_spacing,
            vocab=data.vocab,
        )

        self._morph_suffix_corrector = partial(
            self._suffix_spacing, vocab=data.vocab, only_stem=True
        )

        self.prefixed_verbs_corrector = partial(self._preverb_mi_stem_replacer)
        self.prefixed_simple_future_verbs_corrector = partial(
            self._prefixed_simple_future_verb_replacer
        )

    def _preverb_mi_stem_replacer(self, m: re.Match) -> str:
        preverb = m.group("preverb")
        mi = m.group("mi")
        verb = m.group("verb")

        if preverb[-1] not in data.non_left_joiner_letters:
            preverb = preverb + data.ZWNJ

        if mi:
            # preverb + mi + ZWNJ + verb  -> برمی‌دارم / برنمی‌دارم
            candidate = f"{preverb}{mi}{data.ZWNJ}{verb}"
        else:
            # preverb + stem -> بر‌گردم
            candidate = f"{preverb}{verb}"

        return candidate if candidate in self.conjugated_verbs else m.group(0)

    def _prefixed_simple_future_verb_replacer(self, m: re.Match) -> str:
        preverb = m.group("preverb")
        aux = m.group("aux")
        verb = m.group("verb")
        candidate = f"{preverb} {aux} {verb}"

        return candidate if candidate in self.conjugated_verbs else m.group(0)

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

        no_y_candidate = candidate.removesuffix("یی").removesuffix("ی")
        return (
            candidate
            if ((candidate in vocab) or (no_y_candidate in vocab))
            else m.group(0)
        )

    def _function(self, text: str) -> str:
        # remove invisible control marks
        text = text.translate(self._invisible_translation_table)

        text = self._map_patterns(text, self._spacing_patterns)
        text = self._map_patterns(text, self._other_patterns)
        text = self._map_patterns(text, self._punctuation_spacing_patterns).strip()

        # correct compound words spacing
        text = self.compound_kp.replace_keywords(text)

        # correct word prefixes/suffix spacing
        text = self._word_prefix_space_pattern.sub(self._word_prefix_corrector, text)
        text = self._word_suffix_space_pattern.sub(self._word_suffix_corrector, text)

        # correct morphological suffix spacing
        text = self._morph_suffix_space_pattern.sub(self._morph_suffix_corrector, text)

        # Apply the verbal suffix spacing patterns
        text = self._verbal_suffix_space_pattern.sub(self.verbal_suffix_corrector, text)

        # Apply prefixed verb spacing patterns
        text = self._preverb_mi_stem_pattern.sub(self.prefixed_verbs_corrector, text)
        text = self._prefixed_simple_future_pattern.sub(
            self.prefixed_simple_future_verbs_corrector, text
        )

        # Apply the mi spacing patterns
        text = self._mi_space_pattern.sub(self.verbal_prefix_corrector, text)
        text = self._mi_joined_pattern.sub(self.verbal_prefix_corrector, text)

        return text.strip()
