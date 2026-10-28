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

    input_text = "دییروز با پژنان به کتبخانه رفتیم."
    corrected = checker.transform(input_text)
    assert "دیروز" in corrected
    assert "پژمان" in corrected
    assert "کتابخانه" in corrected


def test_is_word_token_empty_string():
    checker = StatisticalSpellChecker()
    assert checker._is_word_token("") is False


def test_is_word_token_all_numbers():
    checker = StatisticalSpellChecker()
    assert checker._is_word_token("۱۲۳") is False


def test_suggest_returns_list():
    checker = StatisticalSpellChecker()
    suggestions = checker.suggest("سلاام")
    assert isinstance(suggestions, list)
    assert "سلام" in suggestions


def test_correct_text_no_suggestions_keeps_original():
    # Use a tiny vocab with no neighbors of the unknown word
    words = Counter({"سلام": 10})
    checker = StatisticalSpellChecker(words=words, n_edit=1)
    # A word far from the only known vocab word should yield no suggestions
    result = checker.correct("ققققققققق")
    assert result == []
    # correct_text should still return a string (keeping the token as-is)
    corrected = checker.correct_text("ققققققققق")
    assert isinstance(corrected, str)


def _reference_correct(checker, word, n_best=5):
    """Rank candidates by generating every edit, as the original algorithm did."""
    ranked = [word] if word in checker.words else []
    for n in range(1, checker.n_edit + 1):
        known = {w for w in checker.generate_n_edits(word, n) if w in checker.words}
        ranked += sorted(known - set(ranked), key=lambda w: (-checker.words[w], w))
    return ranked[:n_best]


def test_correct_matches_exhaustive_edits_on_custom_vocab():
    # Neighbours by deletion, insertion, substitution and transposition, at
    # one and two edits, plus entries with characters outside the alphabet.
    words = Counter(
        {
            "کتاب": 9,
            "کتب": 7,
            "کتابی": 7,
            "کاتب": 5,
            "کباب": 5,
            "تکاب": 3,
            "کتان": 3,
            "کتابها": 2,
            "قهوه خونه": 2,
            "book": 1,
            "ک": 1,
        }
    )
    for n_edit in (1, 2):
        checker = StatisticalSpellChecker(words=words, n_edit=n_edit)
        for word in ["کتاب", "کتبا", "کاتاب", "تکب", "کبا", "قهوه خون", "boo", "", "ق"]:
            for n_best in (1, 3, 20):
                assert checker.correct(word, n_best) == _reference_correct(
                    checker, word, n_best
                ), (word, n_edit, n_best)


def test_correct_matches_exhaustive_edits_on_default_vocab():
    checker = StatisticalSpellChecker()
    for word in ["درود", "سلاام", "کتبخانه", "دییروز", "پژنان", "ررفتیم", "زبنا"]:
        assert checker.correct(word, n_best=20) == _reference_correct(
            checker, word, n_best=20
        ), word


def test_correct_text_leaves_known_words_untouched():
    words = Counter({"سلام": 5, "سلم": 50})
    checker = StatisticalSpellChecker(words=words)
    # "سلم" is a far more frequent neighbour, but "سلام" is already correct.
    assert checker.correct_text("سلام") == "سلام"
