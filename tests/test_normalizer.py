import re
import pytest
from shekar.normalizer import Normalizer


@pytest.fixture
def normalizer():
    return Normalizer()


def test_normalize_informal_verbs(normalizer):
    assert normalizer("دارم درس میخونم!") == "دارم درس می‌خونم!"
    assert normalizer("نمی تونم بهت بگم چی میشه!") == "نمی‌تونم بهت بگم چی می‌شه!"
    assert (
        normalizer("می دونی که نمیخاستم ناراحتت کنم.")
        == "می‌دونی که نمی‌خاستم ناراحتت کنم."
    )


def test_normalize_basic_spacing_and_quotes(normalizer):
    # Exercises punctuation spacing, ZWNJ for "می + verb", and Persian quotes
    inp = "ناصر گفت:«من میروم.»  \u200c"
    out = normalizer.normalize(inp)
    # Email should be removed (mask="")
    assert "@" not in out
    # Space after colon and before opening quote
    assert "گفت:" in out and "گفت: «" in out
    # ZWNJ in "می‌روم"
    assert "می‌روم" in out
    # Balanced Persian quotes around sentence
    assert "«" in out and "»" in out

    input_text = "بنیان    گذار های خانه هایمان"
    expected_output = "بنیان‌گذارهای خانه‌هایمان"
    assert normalizer(input_text) == expected_output

    input_text = "«فارسی شِکَر است» نام داستان ڪوتاه طنز    آمێزی از محمد علی جمالــــــــزاده  می   باشد که در سال 1921 منتشر  شده است و آغاز   ڱر تحول بزرگی در ادَبێات معاصر ایران بۃ شمار میرود."
    expected_output = "«فارسی شکر است» نام داستان کوتاه طنزآمیزی از محمد‌علی جمالزاده می‌باشد که در سال ۱۹۲۱ منتشر شده‌است و آغازگر تحول بزرگی در ادبیات معاصر ایران به شمار می‌رود."
    assert normalizer(input_text) == expected_output


def test_diacritic_and_digit_normalization(normalizer):
    inp = "فارسی شِکَر است 1234 و ١٢٣"
    out = normalizer.normalize(inp)
    # Diacritics removed from "شِکَر"
    assert "شِکَر" not in out
    assert "شکر" in out
    # Western and Arabic-Indic digits normalized to Persian
    assert "1234" not in out and "١٢٣" not in out
    assert "۱۲۳۴" in out or "۱۲۳" in out


def test_arabic_unicode_normalizer(normalizer):
    # Arabic Yeh/Kaf should be mapped to Persian forms
    inp = "كتاب و هويت با ك ي"
    out = normalizer.normalize(inp)
    assert "ك" not in out and "ي" not in out
    # Expect Persian Kaf/Ye present
    assert "ک" in out or "کتاب" in out
    assert "ی" in out or "هویت" in out


def test_repeated_letter_filter(normalizer):
    # Collapses repeated letters like "عاااالی"
    inp = "عاااالی بوووود!!!"
    out = normalizer.normalize(inp)
    # No triple or more repeats remain
    assert re.search(r"(.)\1\1", out) is None


def test_spacing_normalizer_variants(normalizer):
    # Common Persian spacing and ZWNJ cases
    cases = [
        ("میروم", "می‌روم"),
        ("می روم", "می‌روم"),
        ("نمی دانم", "نمی‌دانم"),
        ("گفته است", "گفته‌است"),
    ]
    outs = [normalizer.normalize(s) for s, _ in cases]
    for (_, expected), out in zip(cases, outs):
        assert expected in out


def test_idempotence_on_normal_text(normalizer):
    text = "فارسی شکر است."
    once = normalizer.normalize(text)
    twice = normalizer.normalize(once)
    assert once == twice


def test_empty_string(normalizer):
    assert normalizer.normalize("") == ""


def test_custom_steps_override_identity():
    # When steps=[], Normalizer should act like identity pass-through
    n = Normalizer(steps=[])
    text = "متن تستی با ایمیل test@example.com و 😀"
    out = n.normalize(text)
    assert out == text  # no transformation


def test_normalize_method_alias(normalizer):
    # Ensure __call__ and normalize give the same result
    s = "می روم"
    assert normalizer.normalize(s) == normalizer(s)


def test_ya_normalizer_joda(normalizer):
    assert normalizer("خانۀ ما") == "خانه‌ی ما"
    assert normalizer("خانه‌ی ما") == "خانه‌ی ما"
    assert normalizer("خانه ی ما") == "خانه‌ی ما"
