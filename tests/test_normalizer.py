import re
import pytest
from shekar.normalizer import Normalizer


@pytest.fixture
def normalizer():
    return Normalizer()


def test_normalize_basic_spacing_and_quotes(normalizer):
    # Exercises punctuation spacing, ZWNJ for "می + verb", and Persian quotes
    inp = "ناصر گفت:«من میروم.»  \u200c 🎉 she+kar@she-kar.io"
    out = normalizer.normalize(inp)
    # Email should be removed (mask="")
    assert "@" not in out
    # Emoji removed
    assert "🎉" not in out
    # Space after colon and before opening quote
    assert "گفت:" in out and "گفت: «" in out
    # ZWNJ in "می‌روم"
    assert "می‌روم" in out
    # Balanced Persian quotes around sentence
    assert "«" in out and "»" in out


def test_email_and_url_masking(normalizer):
    inp = "تماس: user@example.com و وبگاه: https://example.com/page"
    out = normalizer.normalize(inp)
    # Both should be masked to empty by default
    assert "@" not in out
    assert "http" not in out
    # No leftover double spaces from masking
    assert "  " not in out


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


def test_html_tag_filter(normalizer):
    inp = "<p>سلام</p> <a href='#'>دنیا</a>"
    out = normalizer.normalize(inp)
    # Tags removed but content preserved
    assert "<" not in out and ">" not in out
    assert "سلام" in out and "دنیا" in out


def test_emoji_filter(normalizer):
    inp = "سلام 🌍🇮🇷😊"
    out = normalizer.normalize(inp)
    for ch in "🌍🇮🇷😊":
        assert ch not in out


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


def test_iterable_input_list(normalizer):
    texts = ["می روم", "سلام😊", "user@mail.com"]
    outs = normalizer.normalize(texts)
    # Pipeline may return a generator or list; convert to list
    outs = list(outs)
    assert len(outs) == 3
    assert "می‌روم" in outs[0]
    assert "😊" not in outs[1]
    assert "@" not in outs[2]


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
