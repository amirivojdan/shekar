import numpy as np
import pytest

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


@pytest.mark.parametrize("model_max_length", [2, 1, 0, -1, 2.5, True])
def test_rejects_invalid_model_max_length(model_max_length):
    with pytest.raises(
        ValueError, match="model_max_length must be an integer greater than 2"
    ):
        AlbertTokenizer(model_max_length=model_max_length)


@pytest.mark.parametrize("stride", [-1, 6, 7, 1.5, True])
def test_rejects_stride_that_cannot_advance(stride):
    with pytest.raises(ValueError, match="stride must be an integer"):
        AlbertTokenizer(
            enable_truncation=True,
            return_overflowing_tokens=True,
            model_max_length=8,
            stride=stride,
        )


def test_stride_requires_overflow_windows():
    with pytest.raises(ValueError, match="stride is only used"):
        AlbertTokenizer(enable_truncation=True, stride=1)


def test_overflow_windows_require_truncation():
    with pytest.raises(ValueError, match="requires enable_truncation=True"):
        AlbertTokenizer(return_overflowing_tokens=True)


def test_truncation_disabled_preserves_the_full_sequence():
    tokenizer = AlbertTokenizer(enable_truncation=False, model_max_length=8)
    text = " ".join(["سلام"] * 20)
    expected_body_length = len(tokenizer.sp.encode(text, out_type=int))

    output = tokenizer(text)

    assert output["input_ids"].shape == (1, expected_body_length + 2)
    assert output["input_ids"].shape[1] > tokenizer.model_max_length
    assert np.all(output["attention_mask"] == 1)


def test_truncation_returns_only_the_first_window_by_default():
    tokenizer = AlbertTokenizer(enable_truncation=True, model_max_length=8)
    text = " ".join(["سلام"] * 20)

    output = tokenizer(text)

    assert output["input_ids"].shape == (1, tokenizer.model_max_length)
    assert output["input_ids"][0, 0] == tokenizer.cls_token_id
    assert output["input_ids"][0, -1] == tokenizer.sep_token_id


def test_overflow_windows_are_dense_without_explicit_padding():
    tokenizer = AlbertTokenizer(
        enable_padding=False,
        enable_truncation=True,
        return_overflowing_tokens=True,
        model_max_length=8,
    )
    text = " ".join(["سلام"] * 20)

    output = tokenizer(text)

    assert output["input_ids"].ndim == 2
    assert output["input_ids"].shape[0] > 1
    assert output["input_ids"].shape[1] == tokenizer.model_max_length
    assert output["attention_mask"].shape == output["input_ids"].shape
    assert output["token_type_ids"].shape == output["input_ids"].shape
    assert np.any(output["attention_mask"][-1] == 0)


def test_padding_does_not_implicitly_truncate():
    tokenizer = AlbertTokenizer(
        enable_padding=True,
        enable_truncation=False,
        model_max_length=8,
    )
    text = " ".join(["سلام"] * 20)
    expected_body_length = len(tokenizer.sp.encode(text, out_type=int))

    output = tokenizer(text)

    assert output["input_ids"].shape == (1, expected_body_length + 2)
    assert np.all(output["attention_mask"] == 1)


def test_special_token_ids_match_training_vocabulary():
    # The shipped models were trained with these tokens appended after the
    # 32k SentencePiece vocabulary; id 0 is <unk>, not a special token.
    tokenizer = AlbertTokenizer()
    assert tokenizer.unk_token_id == 0
    assert tokenizer.cls_token_id == 32000
    assert tokenizer.sep_token_id == 32001
    assert tokenizer.pad_token_id == 32002
    assert tokenizer.mask_token_id == 32003


def test_encoding_wraps_text_with_cls_and_sep():
    tokenizer = AlbertTokenizer()
    ids = tokenizer("سلام")["input_ids"][0].tolist()
    assert ids == [32000, *tokenizer.sp.encode("سلام", out_type=int), 32001]
    assert tokenizer.encode("سلام").ids == ids


def test_padding_uses_pad_token_with_zero_mask():
    tokenizer = AlbertTokenizer(enable_padding=True, model_max_length=8)
    output = tokenizer("سلام")
    assert output["input_ids"][0, -1] == tokenizer.pad_token_id
    assert output["attention_mask"][0, -1] == 0


def test_token_id_lookups_round_trip_special_tokens():
    tokenizer = AlbertTokenizer()
    for token in ("[CLS]", "[SEP]", "<pad>", "[MASK]", "<unk>"):
        assert tokenizer.id_to_token(tokenizer.token_to_id(token)) == token


def test_unknown_token_name_is_not_mapped_to_unk():
    tokenizer = AlbertTokenizer()
    assert tokenizer.token_to_id("<cls>") is None
    assert tokenizer.token_to_id("not-a-piece-xyz") is None
