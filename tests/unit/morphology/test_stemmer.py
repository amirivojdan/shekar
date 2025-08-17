import pytest
from shekar.morphology.stemmer import Stemmer
from shekar import data


@pytest.fixture
def stemmer():
    return Stemmer()


def test_stemmer_removes_plural_suffix(stemmer):
    assert stemmer("کتاب‌ها") == "کتاب"
    assert stemmer("خانه‌ها") == "خانه"


def test_stemmer_removes_possessive_suffix(stemmer):
    assert stemmer("نوه‌ام") == "نوه"
    assert stemmer("کتابم") == "کتاب"
    assert stemmer("خانه‌مان") == "خانه"
    assert stemmer("دوستت") == "دوست"


def test_stemmer_removes_comparative_superlative(stemmer):
    word = f"خوب{data.ZWNJ}ترین"
    assert stemmer(word) == "خوب"
    word2 = f"سریع{data.ZWNJ}تر"
    assert stemmer(word2) == "سریع"


def test_stemmer_removes_ezafe_after_zwnj(stemmer):
    word = f"خانه{data.ZWNJ}ی"
    assert stemmer(word) == "خانه"
    word2 = f"خانه{data.ZWNJ}یی"
    assert stemmer(word2) == "خانه"


def test_stemmer_no_change_for_no_suffix(stemmer):
    assert stemmer("کتاب") == "کتاب"
    assert stemmer("خانه") == "خانه"
