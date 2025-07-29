import pytest
from shekar.tokenization import (
    Tokenizer,
    WordTokenizer,
    SentenceTokenizer,
    AlbertTokenizer,
)
import collections.abc


def test_tokenizer_default_model_is_word():
    tokenizer = Tokenizer()
    assert isinstance(tokenizer.model, WordTokenizer)


def test_tokenizer_initializes_correct_model():
    assert isinstance(Tokenizer("word").model, WordTokenizer)
    assert isinstance(Tokenizer("sentence").model, SentenceTokenizer)
    assert isinstance(Tokenizer("albert").model, AlbertTokenizer)


def test_tokenizer_invalid_model_raises():
    with pytest.raises(ValueError, match="Unknown tokenizer model 'foobar'"):
        Tokenizer("foobar")


@pytest.mark.parametrize("model_name", ["word", "sentence", "albert"])
def test_tokenizer_transform_returns_expected_type(model_name):
    tokenizer = Tokenizer(model_name)
    text = "سلام دنیا. من علی هستم."

    output = tokenizer.transform(text)

    if model_name == "albert":
        assert isinstance(output, dict)
        assert {"input_ids", "attention_mask", "token_type_ids"} <= output.keys()
    else:
        assert isinstance(output, collections.abc.Iterable)
        output_list = list(output)
        assert all(isinstance(t, str) for t in output_list)


@pytest.mark.parametrize("model_name", ["word", "sentence", "albert"])
def test_tokenizer_fit_delegation(model_name):
    tokenizer = Tokenizer(model_name)
    assert tokenizer.fit(["test sentence"]) is tokenizer.model
