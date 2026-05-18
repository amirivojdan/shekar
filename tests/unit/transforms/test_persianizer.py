import pytest

from shekar.transforms import Persianizer


@pytest.fixture(scope="module")
def persianizer():
    return Persianizer()


def test_suggest_single_loanword(persianizer):
    results = persianizer.suggest("آرشیو را مرتب کن")
    assert len(results) == 1
    alternatives, (start, end) = results[0]
    assert "بایگانی" in alternatives
    assert "آرشیو را مرتب کن"[start:end] == "آرشیو"


def test_suggest_multiple_loanwords(persianizer):
    results = persianizer.suggest("آرشیو و آسانسور")
    assert len(results) == 2
    all_alternatives = [alts for alts, _ in results]
    assert any("بایگانی" in alts for alts in all_alternatives)
    assert any("بالابر" in alts for alts in all_alternatives)


def test_suggest_multiple_alternatives(persianizer):
    results = persianizer.suggest("آسانسور")
    assert len(results) == 1
    alternatives, _ = results[0]
    assert len(alternatives) > 1
    assert "بالابر" in alternatives


def test_suggest_no_loanword(persianizer):
    results = persianizer.suggest("خانه زیباست")
    assert results == []


def test_suggest_returns_correct_span(persianizer):
    text = "آرشیو"
    results = persianizer.suggest(text)
    assert len(results) == 1
    _, (start, end) = results[0]
    assert text[start:end] == "آرشیو"


def test_suggest_empty_string(persianizer):
    assert persianizer.suggest("") == []


def test_suggest_alternatives_are_strings(persianizer):
    results = persianizer.suggest("ابتکار تازه‌ای داشت")
    assert len(results) == 1
    alternatives, _ = results[0]
    assert all(isinstance(alt, str) for alt in alternatives)
    assert all(len(alt) > 0 for alt in alternatives)


def test_transform_replaces_loanword(persianizer):
    result = persianizer("آرشیو را مرتب کن")
    assert "آرشیو" not in result
    assert "بایگانی" in result


def test_transform_replaces_multiple_loanwords(persianizer):
    result = persianizer("آرشیو و آسانسور")
    assert "آرشیو" not in result
    assert "آسانسور" not in result


def test_transform_no_loanword_unchanged(persianizer):
    text = "خانه زیباست"
    assert persianizer(text) == text
