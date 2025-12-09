from shekar.base import BaseTextTransform
from shekar import data
import re


class Stemmer(BaseTextTransform):
    """
    This class implements a simple stemming algorithm for Persian words.
    It removes suffixes from words to obtain their root forms.

    Example:
        >>> stemmer = Stemmer()
        >>> stemmer("کتاب‌ها")
        "کتاب"
        >>> stemmer("نوه‌ام")
        "نوه"

    """

    def __init__(self):
        super().__init__()

        ZWNJ = re.escape(data.ZWNJ)
        NLJ_CLASS = "[" + "".join(map(re.escape, data.non_left_joiner_letters)) + "]"

        self._possessive_mappings = [
            # possessive clitics: remove if joined by ZWNJ or base ends with a non-left-joiner
            (rf"(?:(?:{ZWNJ})|(?<={NLJ_CLASS}))(?:مان|تان|ام|ات|شان)$", ""),
            (
                rf"(?:(?:{ZWNJ})|(?<={NLJ_CLASS}))(?:هایشان|هایش|هایت|هایم|هایتان|هایمان)$",
                "",
            ),
            (
                rf"(?:(?:{ZWNJ})|(?<={NLJ_CLASS}))(?:هاشون|هاش|هات|هام|هاتون|هامون)$",
                "",
            ),  # informal plurals
            (rf"(?:{ZWNJ})?(?:م|ت|ش)$", ""),
        ]

        self._plural_mappings = [
            # plurals: remove if joined by ZWNJ or base ends with a non-left-joiner
            (rf"(?:(?:{ZWNJ})|(?<={NLJ_CLASS}))(?:هایی|های|ها)$", ""),
            (r"(?<=.{2})(?<!ی)گان$", "ه"),
            (r"(?<=.{2})یان$", ""),
            (r"(?<=.{2})یون$", ""),
            (r"(?<=.{2})ان$", ""),
            (r"(?<=.{2})ات$", ""),
        ]

        self._other_mappings = [
            # comparative/superlative: only when explicitly joined with ZWNJ or hyphen
            (rf"(?:(?:{ZWNJ})|(?<={NLJ_CLASS}))(?:ترین|تر)$", ""),
            # ezafe after vowel or heh written as ZWNJ + ی / یی; be conservative, do not strip bare 'ی'
            (rf"{ZWNJ}(?:ی|ای)$", ""),
            (r"(?<=[او])یی$", ""),
            (
                r"ی$",
                "",
            ),  # this should be the last rule to not mess up with other suffix removals
        ]

        self._possessive_patterns = self._compile_patterns(self._possessive_mappings)
        self._plural_patterns = self._compile_patterns(self._plural_mappings)
        self._other_patterns = self._compile_patterns(self._other_mappings)

        self._all_patterns = [
            self._possessive_patterns,
            self._plural_patterns,
            self._other_patterns,
        ]

    def _function(self, text: str) -> str:
        # special cases not plural but eding with "ان"
        if (
            text in data.vocab
            and text.endswith("ان")
            and not text.endswith("یان")
            and not text.endswith("گان")
        ):
            return text

        for patterns in self._all_patterns:
            stem = self._map_patterns(text, patterns)

            if stem != text and len(stem) > 2 and stem in data.vocab:
                if stem in data.informal_words:
                    stem = data.informal_words[stem]
                return stem

        if text in data.informal_words:
            return data.informal_words[text]

        return text
