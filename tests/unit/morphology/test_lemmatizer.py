import pytest
from unittest.mock import MagicMock
from shekar.morphology.lemmatizer import Lemmatizer
from shekar.morphology.conjugator import get_conjugated_verbs
from shekar import data


@pytest.fixture
def lemmatizer():
    return Lemmatizer()


def test_return_infinitive_option():
    lemmatizer = Lemmatizer(return_infinitive=True)
    assert lemmatizer("رفتند") == "رفتن"
    assert lemmatizer("می‌خونم") == "خواندن"
    assert lemmatizer("رفته بودم") == "رفتن"
    assert lemmatizer("خواهم رفت") == "رفتن"


def test_conjugated_verb(lemmatizer, monkeypatch):
    conjugated_verbs = get_conjugated_verbs()
    # Example: "رفتند" -> "رفت/رو"
    monkeypatch.setitem(conjugated_verbs, "رفتند", ("رفت", "رو"))
    assert lemmatizer("رفتند") == "رفت/رو"

    # test هست
    monkeypatch.setitem(conjugated_verbs, "هستند", (None, "هست"))
    assert lemmatizer("هستند") == "هست"


def test_informal_verb(lemmatizer, monkeypatch):
    assert lemmatizer("می‌خونم") == "خواند/خوان"
    assert lemmatizer("می‌خوابم") == "خوابید/خواب"
    assert lemmatizer("نمی‌رم") == "رفت/رو"


def test_stemmer_and_vocab(lemmatizer, monkeypatch):
    monkeypatch.setattr(lemmatizer.stemmer, "__call__", lambda self, text: "کتاب")
    monkeypatch.setitem(data.vocab, "کتاب", True)
    assert lemmatizer("کتاب‌ها") == "کتاب"


def test_vocab_only(lemmatizer, monkeypatch):
    monkeypatch.setattr(lemmatizer, "stemmer", MagicMock(return_value=""))
    assert lemmatizer("مدرسه") == "مدرسه"  # "مدرسه" is in data.vocab


def test_no_match(lemmatizer, monkeypatch):
    monkeypatch.setattr(lemmatizer, "stemmer", MagicMock(return_value=""))
    result = lemmatizer("xyzغیرواقعی123")
    assert result == "xyzغیرواقعی123"


def test_prefixed_verbs(lemmatizer):
    assert lemmatizer("فراخواند") == "فراخواند/فراخوان"
    assert lemmatizer("فرابخوان") == "فراخواند/فراخوان"
    assert lemmatizer("فرا نخواهم خواند") == "فراخواند/فراخوان"
    assert lemmatizer("پس‌نمی‌انداخت") == "پس\u200cانداخت/پس\u200cانداز"
    assert lemmatizer("ورنیامد") == "ورآمد/ورآ"
    assert lemmatizer("باز نخواهم گشت") == "بازگشت/بازگرد"


def test_return_infinitive_normal_verb_appends_noon(monkeypatch):
    lemmatizer = Lemmatizer(return_infinitive=True)
    conjugated_verbs = get_conjugated_verbs()
    monkeypatch.setitem(conjugated_verbs, "آزمودند", ("آزمود", "آزما"))
    assert lemmatizer("آزمودند") == "آزمودن"


def test_return_infinitive_real_verb():
    lemmatizer = Lemmatizer(return_infinitive=True)
    assert lemmatizer("رفتند") == "رفتن"


def test_return_infinitive_informal_verb():
    lemmatizer = Lemmatizer(return_infinitive=True)
    assert lemmatizer("می‌خونم") == "خواندن"


def test_return_infinitive_past_stem_none(monkeypatch):
    lemmatizer = Lemmatizer(return_infinitive=True)
    conjugated_verbs = get_conjugated_verbs()
    monkeypatch.setitem(conjugated_verbs, "هستید", (None, "هست"))
    assert lemmatizer("هستید") == "هست"
