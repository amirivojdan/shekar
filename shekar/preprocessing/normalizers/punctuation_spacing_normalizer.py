import re

from shekar import data
from shekar.base import BaseTextTransform


class PunctuationSpacingNormalizer(BaseTextTransform):
    def __init__(self):
        super().__init__()

        self._punctuation_spacing_mappings = [
            # Remove space after leading punctuation like ". این" -> ".این"
            (
                rf"^([{re.escape(data.single_punctuations)}])[^\S\r\n]+",
                r"\1",
            ),
            # Remove space after opener punctuation: "( سلام" -> "(سلام"
            (
                rf"([{re.escape(data.opener_punctuations)}])[^\S\r\n]+",
                r"\1",
            ),
            # Remove space before closer punctuation: "سلام )" -> "سلام)"
            (
                rf"[^\S\r\n]+([{re.escape(data.closer_punctuations)}])",
                r"\1",
            ),
            # Ensure space before opener punctuation if attached: "سلام(دنیا" -> "سلام (دنیا"
            (
                rf"(?<=\S)[^\S\r\n]*([{re.escape(data.opener_punctuations)}])",
                r" \1",
            ),
            # Ensure one space after closer punctuation when needed
            (
                r"([{cl}])(?=(?![{sg}{cl}])\S)".format(
                    cl=re.escape(data.closer_punctuations),
                    sg=re.escape(data.single_punctuations),
                ),
                r"\1 ",
            ),
            # Remove space before single punctuations: "سلام ،" -> "سلام،"
            (
                rf"[^\S\r\n]+([{re.escape(data.single_punctuations)}])",
                r"\1",
            ),
            # Ensure one space after single punctuations (except at start)
            (
                r"(?<!^)([{sg}])(?=(?![{sg}{cl}])\S)".format(
                    sg=re.escape(data.single_punctuations),
                    cl=re.escape(data.closer_punctuations),
                ),
                r"\1 ",
            ),
            # Trim leading and trailing horizontal spaces (preserve newlines)
            (r"^[^\S\r\n]+|[^\S\r\n]+$", ""),
        ]

        self._patterns = self._compile_patterns(self._punctuation_spacing_mappings)

    def _function(self, text: str) -> str:
        if not text:
            return text
        return self._map_patterns(text, self._patterns)
