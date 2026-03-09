from functools import partial
from typing import Set
import re
from flashtext import KeywordProcessor
from shekar.base import BaseTextTransform
from shekar import data


class WordSpacingNormalizer(BaseTextTransform):
    def __init__(self):
        super().__init__()

        self.compound_kp = KeywordProcessor(case_sensitive=True)
        compound_words = data.compound_words

        for correct_word in compound_words:
            # Handle words stored with # as placeholder for ZWNJ
            if "#" not in correct_word:
                self.compound_kp.add_keyword(
                    correct_word.replace(data.ZWNJ, " "), correct_word
                )
            else:
                self.compound_kp.add_keyword(
                    correct_word.replace("#", " "), correct_word.replace("#", "")
                )

        _punc_class = re.escape(data.punctuations)
        _word_prefix_alt = "|".join(map(re.escape, data.prefixes))
        _word_suffix_alt = "|".join(map(re.escape, data.suffixes))
        _morph_suffix_alt = "|".join(map(re.escape, data.morph_suffixes))
        _attached_morph_suffix_alt = "|".join(
            map(
                re.escape,
                data.plural_morph_suffixes + data.comparative_superlative_suffixes,
            )
        )

        self._word_prefix_space_pattern = re.compile(
            rf"(?<!\S)(?P<prefix>(?:{_word_prefix_alt}))\s+(?P<stem>[{data.persian_letters}]+)(?=$|[\s{_punc_class}])"
        )
        self._word_suffix_space_pattern = re.compile(
            rf"(?<!\S)(?P<stem>[{data.persian_letters}]+)\s+(?P<suffix>(?:{_word_suffix_alt}))(?=$|[\s{_punc_class}])"
        )
        self._morph_suffix_space_pattern = re.compile(
            rf"(?<!\S)(?P<stem>[{data.persian_letters}]+)\s+(?P<suffix>(?:{_morph_suffix_alt}))(?=$|[\s{_punc_class}])"
        )

        self._attached_morph_suffix_space_pattern = re.compile(
            rf"(?P<stem>[{data.persian_letters}]+)(?P<suffix>(?:{_attached_morph_suffix_alt}))(?=$|[\s{_punc_class}])",
            re.MULTILINE,
        )

        self._attached_morph_suffix_corrector = partial(
            self._suffix_spacing, vocab=data.vocab, only_stem=True
        )

        self._word_prefix_corrector = partial(
            self._prefix_spacing,
            vocab=data.vocab,
        )
        self._word_suffix_corrector = partial(
            self._suffix_spacing,
            vocab=data.vocab,
        )
        self._morph_suffix_corrector = partial(
            self._suffix_spacing, vocab=data.vocab, only_stem=True
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

        if m.group(0) in vocab:
            return m.group(0)

        candidate = (
            f"{stem}{data.ZWNJ}{suffix}"
            if stem[-1] not in data.non_left_joiner_letters
            else f"{stem}{suffix}"
        )

        if only_stem:
            return candidate if stem in vocab else m.group(0)

        # handle "ی" variants
        no_y_candidate = candidate.removesuffix("یی").removesuffix("ی")
        return (
            candidate
            if ((candidate in vocab) or (no_y_candidate in vocab))
            else m.group(0)
        )

    def _function(self, text: str) -> str:
        text = self.compound_kp.replace_keywords(text)

        text = self._word_prefix_space_pattern.sub(self._word_prefix_corrector, text)
        text = self._word_suffix_space_pattern.sub(self._word_suffix_corrector, text)
        text = self._morph_suffix_space_pattern.sub(self._morph_suffix_corrector, text)
        text = self._attached_morph_suffix_space_pattern.sub(
            self._attached_morph_suffix_corrector, text
        )
        return text
