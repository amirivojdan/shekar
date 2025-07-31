import pytest
from unittest.mock import patch, MagicMock
from shekar.spelling import SpellChecker


def test_spellchecker_initialization_default_model():
    # Patch where it's used, not where it's defined!
    with patch(
        "shekar.spelling.checker.SPELL_CHECKING_REGISTRY",
        {"statistical": MagicMock()},
    ) as fake_registry:
        spell = SpellChecker()
        assert callable(spell.model) or hasattr(spell.model, "transform")

    fake_registry.keys


def test_spellchecker_invalid_model():
    with pytest.raises(ValueError) as exc_info:
        SpellChecker(model="unknown")
    assert "Unknown spell checking model" in str(exc_info.value)


def test_spellchecker_fit_calls_underlying_model():
    fake_model = MagicMock()
    with patch(
        "shekar.spelling.checker.SPELL_CHECKING_REGISTRY",
        {"statistical": lambda: fake_model},
    ):
        spell = SpellChecker()
        X = ["متن تستی"]
        spell.fit(X)
        fake_model.fit.assert_called_once_with(X, None)


def test_spellchecker_transform_calls_underlying_model():
    fake_model = MagicMock()
    fake_model.transform.return_value = "متن اصلاح‌شده"
    with patch(
        "shekar.spelling.checker.SPELL_CHECKING_REGISTRY",
        {"statistical": lambda: fake_model},
    ):
        spell = SpellChecker()
        result = spell.transform("متن تستی")
        fake_model.transform.assert_called_once_with("متن تستی")
        assert result == "متن اصلاح‌شده"
