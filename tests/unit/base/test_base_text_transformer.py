import pytest
import re
import regex
from shekar.base import BaseTextTransform


class TestBaseTextTransformer:
    class MockTextTransformer(BaseTextTransform):
        def _function(self, X: str, y=None) -> str:
            # Example implementation for testing purposes
            return X.replace("گربه", "سگ")

    @pytest.fixture
    def transformer(self):
        return self.MockTextTransformer()

    def test_transform_single_string(self, transformer):
        input_text = "گربه روی دیوار نشست."
        expected_output = "سگ روی دیوار نشست."
        assert transformer.transform(input_text) == expected_output

    def test_transform_iterable_strings(self, transformer):
        input_texts = ["گربه روی دیوار نشست.", "گربه در حیاط بود."]
        expected_output = ["سگ روی دیوار نشست.", "سگ در حیاط بود."]
        assert list(transformer.transform(input_texts)) == expected_output

    def test_transform_invalid_input(self, transformer):
        with pytest.raises(
            ValueError, match="Input must be a string or a Iterable of strings."
        ):
            transformer.transform(123)

    def test_fit(self, transformer):
        input_text = "گربه روی دیوار نشست."
        assert transformer.fit(input_text) is transformer

    def test_fit_transform(self, transformer):
        input_text = "گربه روی دیوار نشست."
        expected_output = "سگ روی دیوار نشست."
        assert transformer.fit_transform(input_text) == expected_output

    def test_compile_patterns(self):
        mappings = [
            (r"\bگربه\b", "سگ"),
            (r"\bدیوار\b", "حیاط"),
        ]

        compiled_patterns = BaseTextTransform._compile_patterns(mappings)
        print(compiled_patterns)
        assert len(compiled_patterns) == 2
        assert isinstance(compiled_patterns[0][0], (re.Pattern, regex.Pattern))
        assert compiled_patterns[0][1] == "سگ"

    def test_map_patterns(self):
        text = "گربه روی دیوار نشست."
        patterns = BaseTextTransform._compile_patterns(
            [("گربه", "سگ"), ("دیوار", "حیاط")]
        )
        expected_output = "سگ روی حیاط نشست."
        assert BaseTextTransform._map_patterns(text, patterns) == expected_output

    def test_abstract_function_error(self):
        with pytest.raises(NotImplementedError):
            BaseTextTransform._function(None, None)
