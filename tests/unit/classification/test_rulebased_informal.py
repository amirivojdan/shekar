import pytest

from shekar import data
from shekar.classification.informal_rule_based import (
    RuleBasedInformalClassifier,
    _get_informal_conjugations,
)


def test_informal_sentence():
    classifier = RuleBasedInformalClassifier()
    assert classifier.is_informal("نون بگیر بیار داری میای خونه") is True


def test_threshold():
    classifier = RuleBasedInformalClassifier(occurrence_threshold=5)
    assert classifier.is_informal("نون بگیر بیار داری میای خونه") is False


def test_formal_sentence():
    classifier = RuleBasedInformalClassifier()
    assert classifier.is_informal("من به خانه می‌آیم") is False


@pytest.mark.parametrize(
    "sentence",
    [
        "او خواب دید",
        "آنها به خانه می‌روند",
        "او روی صندلی نشسته است",
    ],
)
def test_formal_conjugations_are_not_informal(sentence):
    classifier = RuleBasedInformalClassifier()
    assert classifier.is_informal(sentence) is False


def test_dictionary_word_does_not_match_informal_conjugation():
    assert "آن" in data.vocab
    assert "آن" not in _get_informal_conjugations()

    classifier = RuleBasedInformalClassifier()
    sentence = "جهانی است که در آن سحر و واقعیت به‌طور همزمان پذیرفته می‌شوند."
    assert classifier.is_informal(sentence) is False


@pytest.mark.parametrize("word", ["باشه", "داره", "بگم", "می‌ده", "خوندن"])
def test_genuine_informal_conjugation_is_not_filtered_by_dictionary(word):
    assert word not in data.vocab
    assert word in _get_informal_conjugations()
