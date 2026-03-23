from functools import partial
from typing import Set
import re

from shekar.base import BaseTextTransform
from shekar import data
from shekar.morphology.conjugator import get_conjugated_verbs


class VerbalSpacingNormalizer(BaseTextTransform):
    def __init__(self):
        super().__init__()

        self.conjugated_verbs: Set[str] = get_conjugated_verbs()
        _punc_class = re.escape(data.punctuations)

        _verbal_suffix_alt = "|".join(
            map(re.escape, ["ام", "ای", "است", "ایم", "اید", "اند"])
        )
        self._verbal_suffix_space_pattern = re.compile(
            rf"(?<!\S)(?P<stem>[{data.persian_letters}]+)\s+"
            rf"(?P<suffix>(?:{_verbal_suffix_alt}))"
            rf"(?=$|[\s{_punc_class}])"
        )

        self._ast_zwnj_pattern = re.compile(
            rf"(?<=ه){data.ZWNJ}(است)(?=$|[\s{_punc_class}])"
        )

        self._mi_space_pattern = re.compile(
            rf"(?<!\S)(?P<prefix>ن?می)\s+(?P<stem>[{data.persian_letters}]+)"
        )

        self._mi_joined_pattern = re.compile(
            rf"(?<!\S)(?P<prefix>ن?می)(?![ ‌])(?P<stem>[{data.persian_letters}]+)"
        )

        _verbal_prefixes_alt = "|".join(map(re.escape, data.verbal_prefixes))
        self._preverb_mi_stem_pattern = re.compile(
            rf"(?<!\S)"
            rf"(?P<preverb>(?:{_verbal_prefixes_alt}))"
            rf"(?P<sep>{data.ZWNJ}|\s+|)"
            rf"(?:(?P<mi>ن?می)(?:{data.ZWNJ}|\s+|))?"
            rf"(?P<verb>[{data.persian_letters}]+)"
            rf"(?=$|[\s{_punc_class}])"
        )

        _prefixed_simple_future_alt = "|".join(
            map(
                re.escape,
                ["خواهم", "خواهی", "خواهد", "خواهیم", "خواهید", "خواهند"],
            )
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

        self._verbal_prefix_corrector = partial(
            self._prefix_spacing,
            vocab=self.conjugated_verbs,
        )
        self._verbal_suffix_corrector = partial(
            self._suffix_spacing,
            vocab=self.conjugated_verbs,
        )
        self._prefixed_verbs_corrector = partial(self._preverb_mi_stem_replacer)
        self._prefixed_simple_future_verbs_corrector = partial(
            self._prefixed_simple_future_verb_replacer
        )

    def _prefix_spacing(
        self, m: re.Match, vocab: Set[str], only_stem: bool = False
    ) -> str:
        prefix = m.group("prefix")
        stem = m.group("stem")

        candidate = (
            f"{prefix}{data.ZWNJ}{stem}"
            if prefix[-1] not in data.non_left_joiner_letters
            else f"{prefix}{stem}"
        )

        if only_stem:
            return candidate if stem in vocab else m.group(0)

        return candidate if candidate in vocab else m.group(0)

    def _suffix_spacing(
        self, m: re.Match, vocab: Set[str], only_stem: bool = False
    ) -> str:
        stem = m.group("stem")
        suffix = m.group("suffix")

        candidate = (
            f"{stem}{data.ZWNJ}{suffix}"
            if stem[-1] not in data.non_left_joiner_letters
            else f"{stem}{suffix}"
        )

        if only_stem:
            return candidate if stem in vocab else m.group(0)

        no_y_candidate = candidate.removesuffix("یی").removesuffix("ی")
        return (
            candidate
            if ((candidate in vocab) or (no_y_candidate in vocab))
            else m.group(0)
        )

    def _preverb_mi_stem_replacer(self, m: re.Match) -> str:
        preverb = m.group("preverb")
        sep = m.group("sep")
        mi = m.group("mi")
        verb = m.group("verb")

        if " " in (sep or "") and verb in data.stopwords:
            return m.group(0)

        if preverb[-1] not in data.non_left_joiner_letters:
            preverb = preverb + data.ZWNJ

        if mi:
            candidate = f"{preverb}{mi}{data.ZWNJ}{verb}"
        else:
            candidate = f"{preverb}{verb}"

        return candidate if candidate in self.conjugated_verbs else m.group(0)

    def _prefixed_simple_future_verb_replacer(self, m: re.Match) -> str:
        preverb = m.group("preverb")
        aux = m.group("aux")
        verb = m.group("verb")
        candidate = f"{preverb} {aux} {verb}"

        return candidate if candidate in self.conjugated_verbs else m.group(0)

    def _function(self, text: str) -> str:
        # verbal suffix spacing (رفته ام -> رفته‌ام)
        text = self._verbal_suffix_space_pattern.sub(
            self._verbal_suffix_corrector, text
        )

        # prefixed verbs (بر می دارم -> برمی‌دارم)
        text = self._preverb_mi_stem_pattern.sub(self._prefixed_verbs_corrector, text)

        # prefixed simple future verbs
        text = self._prefixed_simple_future_pattern.sub(
            self._prefixed_simple_future_verbs_corrector, text
        )

        # mi / nemi spacing (می روم / میروم -> می‌روم)
        text = self._mi_space_pattern.sub(self._verbal_prefix_corrector, text)
        text = self._mi_joined_pattern.sub(self._verbal_prefix_corrector, text)

        text = self._ast_zwnj_pattern.sub(r" \1", text)

        return text
