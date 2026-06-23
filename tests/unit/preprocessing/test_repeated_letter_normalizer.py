from shekar.preprocessing.normalizers.repeated_letter_normalizer import (
    RepeatedLetterNormalizer,
)


def test_repeated_letters_collapsed():
    n = RepeatedLetterNormalizer()
    assert n("اینجاااا") == "اینجاا"
    assert n("سلاممم") == "سلامم"


def test_keshida_removed():
    n = RepeatedLetterNormalizer()
    assert n("اینــــجا") == "اینجا"


def test_digits_preserved():
    n = RepeatedLetterNormalizer()
    assert n("۲۰۰۰") == "۲۰۰۰"
    assert n("۱۰۰۰۰") == "۱۰۰۰۰"
    assert n("10000") == "10000"
    assert n("5555") == "5555"
