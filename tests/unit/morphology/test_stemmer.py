import pytest
from shekar.morphology.stemmer import Stemmer
from shekar import data


@pytest.fixture
def stemmer():
    return Stemmer()


def test_stemmer_removes_plural_suffix(stemmer):
    assert stemmer("کتاب‌ها") == "کتاب"
    assert stemmer("خانه‌ها") == "خانه"
    assert stemmer("خونه‌هامون") == "خانه"
    assert stemmer("حیوون") == "حیوان"
    assert stemmer("دوستان") == "دوست"
    assert stemmer("زورگیران") == "زورگیر"
    assert stemmer("مدیران") == "مدیر"
    assert stemmer("حیوانات") == "حیوان"
    assert stemmer("دانش‌آموزان") == "دانش‌آموز"
    assert stemmer("کشته‌شدگان") == "کشته‌شده"
    assert stemmer("رزمندگان") == "رزمنده"

    assert stemmer("زعفران") != "زعفر"
    assert stemmer("زعفرون") == "زعفران"

    assert stemmer("بیکران") == "بیکران"
    assert stemmer("شوکران") == "شوکران"
    assert stemmer("میهمان") == "میهمان"
    assert stemmer("ایران") == "ایران"
    assert stemmer("امان") == "امان"
    assert stemmer("پایان") == "پایان"
    assert stemmer("پهلوان") == "پهلوان"

    assert stemmer("شاتگان") != "شاته"
    assert stemmer("یگان") != "یه"
    assert stemmer("رایگان") != "رایه"
    assert stemmer("شایگان") != "شایه"

    assert stemmer("آقایون") == "آقا"


def test_stemmer_removes_possessive_suffix(stemmer):
    assert stemmer("نوه‌ام") == "نوه"
    assert stemmer("کتابم") == "کتاب"
    assert stemmer("خانه‌مان") == "خانه"
    assert stemmer("دوستت") == "دوست"

    assert stemmer("کتاب‌هامون") == "کتاب"
    assert stemmer("کتاب‌هام") == "کتاب"
    assert stemmer("رفیق‌هامون") == "رفیق"


def test_stemmer_removes_comparative_superlative(stemmer):
    word = f"خوب{data.ZWNJ}ترین"
    assert stemmer(word) == "خوب"

    word2 = f"سریع{data.ZWNJ}تر"
    assert stemmer(word2) == "سریع"

    word3 = "دشوارترین"
    assert stemmer(word3) == "دشوار"

    word4 = "شدیدترین"
    assert stemmer(word4) == "شدید"


def test_stemmer_removes_ezafe_after_zwnj(stemmer):
    word = f"خانه{data.ZWNJ}ی"
    assert stemmer(word) == "خانه"

    word = "پیتزایی"
    assert stemmer(word) == "پیتزا"

    word = "صهیونیستی"
    assert stemmer(word) == "صهیونیست"

    word = "شورای"
    assert stemmer(word) == "شورا"

    word = "هندویی"
    assert stemmer(word) == "هندو"

    word = "کمردردی"
    assert stemmer(word) == "کمردرد"


def test_stemmer_no_change_for_no_suffix(stemmer):
    assert stemmer("کتاب") == "کتاب"
    assert stemmer("خانه") == "خانه"
