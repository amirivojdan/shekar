import re
from shekar.base import BaseTextTransform
from shekar import data


class PunctuationSpacingNormalizer(BaseTextTransform):
    def __init__(self):
        super().__init__()

        self._punctuation_spacing_mappings = [
            # Remove space after leading punctuation like ". این" -> ".این"
            (
                r"^([{sg}])[^\S\r\n]+".format(sg=re.escape(data.single_punctuations)),
                r"\1",
            ),
            # Remove space after opener punctuation: "( سلام" -> "(سلام"
            (
                r"([{op}])[^\S\r\n]+".format(op=re.escape(data.opener_punctuations)),
                r"\1",
            ),
            # Remove space before closer punctuation: "سلام )" -> "سلام)"
            (
                r"[^\S\r\n]+([{cl}])".format(cl=re.escape(data.closer_punctuations)),
                r"\1",
            ),
            # Ensure space before opener punctuation if attached: "سلام(دنیا" -> "سلام (دنیا"
            (
                r"(?<=\S)[^\S\r\n]*([{op}])".format(
                    op=re.escape(data.opener_punctuations)
                ),
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
                r"[^\S\r\n]+([{sg}])".format(sg=re.escape(data.single_punctuations)),
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
