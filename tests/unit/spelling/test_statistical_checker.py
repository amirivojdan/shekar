from collections import Counter
from shekar.spelling.statistical_checker import StatisticalSpellChecker


def test_generate_1edits_has_reasonable_variants():
    word = "کتاب"
    edits = StatisticalSpellChecker.generate_1edits(word)
    assert isinstance(edits, set)
    assert any(len(e) == len(word) for e in edits)  # replacements or transposes
    assert any(len(e) == len(word) - 1 for e in edits)  # deletions
    assert any(len(e) == len(word) + 1 for e in edits)  # insertions


def test_generate_n_edits_expands_with_n():
    word = "کتاب"
    edits_1 = StatisticalSpellChecker.generate_n_edits(word, n=1)
    edits_2 = StatisticalSpellChecker.generate_n_edits(word, n=2)
    assert edits_2.issuperset(edits_1)
    assert len(edits_2) > len(edits_1)


def test_correct_returns_known_word_if_exists():
    checker = StatisticalSpellChecker()
    assert checker.correct("سلام")[0] == "سلام"


def test_correct_returns_best_match_for_misspelled_word():
    words = Counter({"سلام": 10, "سللم": 1})
    checker = StatisticalSpellChecker(words=words)
    suggestions = checker.correct("سلاا")
    assert isinstance(suggestions, list)
    assert "سلام" in suggestions


def test_correct_text_with_mixed_words():
    words = Counter({"سلام": 5, "علیکم": 3, "دوست": 2})
    checker = StatisticalSpellChecker(words=words)
    text = "سلاام علیکم دوصت"
    corrected = checker.correct_text(text)
    assert "سلام" in corrected
    assert "علیکم" in corrected
    assert "دوست" in corrected


def test_transform_applies_correction_to_sentence():
    checker = StatisticalSpellChecker()
    input_text = "سلاام بر شوم"
    corrected = checker.transform(input_text)
    assert isinstance(corrected, str)
    assert len(corrected.split()) == len(input_text.split())
