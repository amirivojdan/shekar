import numpy as np
from shekar.tokenization import AlbertTokenizer


def test_albert_tokenizer_real_loads_successfully():
    tokenizer = AlbertTokenizer()
    assert tokenizer.tokenizer is not None
    assert hasattr(tokenizer, "transform")


def test_albert_tokenizer_transform_output():
    tokenizer = AlbertTokenizer()

    text = "من عاشق برنامه‌نویسی هستم."
    output = tokenizer.transform(text)

    # Check keys
    assert isinstance(output, dict)
    assert set(output.keys()) == {"input_ids", "attention_mask", "token_type_ids"}

    # Check shapes and types
    input_ids = output["input_ids"]
    attention_mask = output["attention_mask"]
    token_type_ids = output["token_type_ids"]

    assert isinstance(input_ids, np.ndarray)
    assert input_ids.dtype == np.int64
    assert input_ids.shape[0] == 1

    assert isinstance(attention_mask, np.ndarray)
    assert attention_mask.shape == input_ids.shape

    assert isinstance(token_type_ids, np.ndarray)
    assert token_type_ids.shape == input_ids.shape
    assert np.all(token_type_ids == 0)


def test_albert_tokenizer_multiple_sentences():
    tokenizer = AlbertTokenizer()

    texts = ["سلام دنیا", "او به دانشگاه تهران رفت.", "کتاب‌ها روی میز هستند."]

    for text in texts:
        output = tokenizer.transform(text)
        assert isinstance(output, dict)
        assert output["input_ids"].shape[1] > 0  # Non-empty sequence
