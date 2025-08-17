import pytest
from shekar.morphology.lemmatizer import Lemmatizer
from shekar import data


@pytest.fixture
def lemmatizer():
    return Lemmatizer()


def test_conjugated_verb(lemmatizer, monkeypatch):
    # Example: "رفتند" -> "رفت/رو"
    monkeypatch.setitem(data.conjugated_verbs, "رفتند", ("رفت", "رو"))
    assert lemmatizer("رفتند") == "رفت/رو"


def test_stemmer_and_vocab(lemmatizer, monkeypatch):
    # Example: "کتاب‌ها" -> "کتاب"
    # Simulate stemmer returning "کتاب" and "کتاب" in vocab
    monkeypatch.setattr(lemmatizer.stemmer, "__call__", lambda self, text: "کتاب")
    monkeypatch.setitem(data.vocab, "کتاب", True)
    assert lemmatizer("کتاب‌ها") == "کتاب"


def test_vocab_only(lemmatizer, monkeypatch):
    # If word is in vocab, return as is
    monkeypatch.setitem(data.vocab, "مدرسه", True)
    assert lemmatizer("مدرسه") == "مدرسه"


def test_no_match(lemmatizer, monkeypatch):
    # If word is not in conjugated_verbs, stemmer result not in vocab, and not in vocab
    monkeypatch.setattr(lemmatizer.stemmer, "__call__", lambda self, text: "ناشناخته")
    monkeypatch.setitem(data.vocab, "ناشناخته", False)
    assert lemmatizer("ناشناخته") == "ناشناخته"
