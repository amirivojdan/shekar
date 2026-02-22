import pytest
from shekar.tokenization import SentenceTokenizer


@pytest.fixture
def tokenizer():
    return SentenceTokenizer()


def test_tokenize_simple_sentence(tokenizer):
    text = "زنده باد ایران!"
    expected = ["زنده باد ایران!"]
    assert list(tokenizer.tokenize(text)) == expected


def test_tokenize_multiple_sentences(tokenizer):
    text = "چه سیب‌های قشنگی! حیات نشئه تنهایی است."
    expected = ["چه سیب‌های قشنگی!", "حیات نشئه تنهایی است."]
    assert list(tokenizer(text)) == expected


def test_tokenize_multiple_sentences_with_space(tokenizer):
    text = "چه سیب‌های قشنگی!      حیات نشئه تنهایی است. "
    expected = ["چه سیب‌های قشنگی!", "حیات نشئه تنهایی است."]
    assert list(tokenizer.tokenize(text)) == expected


def test_tokenize_multiple_sentences_with_newline(tokenizer):
    text = "چه سیب‌های قشنگی!  \n\n  \n  \nحیات نشئه تنهایی است.  "
    expected = ["چه سیب‌های قشنگی!", "حیات نشئه تنهایی است."]
    assert list(tokenizer(text)) == expected


def test_tokenize_multiple_sentences_with_question_mark(tokenizer):
    text = "ما چه کردیم؟ و چه خواهیم کرد در این فرصت کم!؟"
    expected = ["ما چه کردیم؟", "و چه خواهیم کرد در این فرصت کم!؟"]
    assert list(tokenizer.tokenize(text)) == expected


def test_tokenize_sentences_with_quotation_marks(tokenizer):
    text = "او گفت: «من فردا به خانه می‌روم.»"
    expected = ["او گفت: «من فردا به خانه می‌روم.»"]
    assert list(tokenizer(text)) == expected
