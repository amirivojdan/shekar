import pytest
from shekar.morphology.inflector import Inflector
from shekar import data


class TestInflector:
    @pytest.fixture
    def inflector(self):
        return Inflector()

    # Tests for comparative method
    def test_comparative_irregular(self, inflector):
        assert inflector.comparative("خوب") == "بهتر"
        assert inflector.comparative("که") == "کهتر"
        assert inflector.comparative("به") == "بهتر"
        assert inflector.comparative("کم") == "کمتر"
        assert inflector.comparative("بیش") == "بیشتر"
        assert inflector.comparative("مه") == "مهتر"

    def test_comparative_with_zwnj(self, inflector):
        assert inflector.comparative("ناراحت") == f"ناراحت{data.ZWNJ}تر"
        assert inflector.comparative("بزرگ") == f"بزرگ{data.ZWNJ}تر"

    def test_comparative_without_zwnj(self, inflector):
        # Test with letters that don't need ZWNJ
        for letter in data.non_left_joiner_letters:
            test_word = "تست" + letter
            assert inflector.comparative(test_word) == test_word + "تر"

    # Tests for superlative method
    def test_superlative_irregular(self, inflector):
        assert inflector.superlative("خوب") == "بهترین"
        assert inflector.superlative("که") == "کهترین"
        assert inflector.superlative("به") == "بهترین"
        assert inflector.superlative("کم") == "کمترین"
        assert inflector.superlative("بیش") == "بیشترین"
        assert inflector.superlative("مه") == "مهترین"

    def test_superlative_with_zwnj(self, inflector):
        assert inflector.superlative("ناراحت") == f"ناراحت{data.ZWNJ}ترین"
        assert inflector.superlative("بزرگ") == f"بزرگ{data.ZWNJ}ترین"

    def test_superlative_without_zwnj(self, inflector):
        # Test with letters that don't need ZWNJ
        for letter in data.non_left_joiner_letters:
            test_word = "تست" + letter
            assert inflector.superlative(test_word) == test_word + "ترین"

    # Tests for plural method
    def test_plural_with_zwnj(self, inflector):
        assert inflector.plural("کتاب") == f"کتاب{data.ZWNJ}ها"
        assert inflector.plural("درخت") == f"درخت{data.ZWNJ}ها"

    def test_plural_without_zwnj(self, inflector):
        assert inflector.plural("میز") == "میزها"

        # Test with letters that don't need ZWNJ
        for letter in data.non_left_joiner_letters:
            test_word = "تست" + letter
            assert inflector.plural(test_word) == test_word + "ها"

    def test_all_irregular_adjectives(self, inflector):
        # Test that all irregular adjectives in the dictionary work correctly
        for adj, (comp, sup) in inflector.irregular_adjectives.items():
            assert inflector.comparative(adj) == comp
            assert inflector.superlative(adj) == sup
