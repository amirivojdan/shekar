import numpy as np
import pytest

from shekar.transliteration.byt5_tokenizer import ByT5Tokenizer


@pytest.fixture
def tokenizer():
    return ByT5Tokenizer()


def test_constants(tokenizer):
    assert tokenizer._pad_id == 0
    assert tokenizer._eos_id == 1
    assert tokenizer._byte_offset == 3


def test_tokenize_appends_eos(tokenizer):
    ids = tokenizer.tokenize("a")
    assert int(ids[-1]) == tokenizer._eos_id


def test_tokenize_ascii(tokenizer):
    ids = tokenizer.tokenize("a")
    assert int(ids[0]) == ord("a") + tokenizer._byte_offset


def test_tokenize_persian(tokenizer):
    ids = tokenizer.tokenize("ک")
    expected = [b + tokenizer._byte_offset for b in "ک".encode("utf-8")]
    assert ids[: len(expected)].tolist() == expected


def test_tokenize_returns_int64(tokenizer):
    ids = tokenizer.tokenize("test")
    assert ids.dtype == np.int64


def test_detokenize_ignores_special_ids(tokenizer):
    assert tokenizer.detokenize([0, 1, 2]) == ""


def test_roundtrip(tokenizer):
    for text in ["کتاب", "hello", "донишгоҳ"]:
        ids = tokenizer.tokenize(text)
        assert tokenizer.detokenize(ids) == text


def test_batch_tokenize_shape(tokenizer):
    texts = ["ک", "کتاب"]
    input_ids, attn = tokenizer.batch_tokenize(texts)
    assert input_ids.shape[0] == 2
    assert input_ids.shape == attn.shape


def test_batch_tokenize_pads_shorter_sequence(tokenizer):
    texts = ["ک", "کتاب"]
    input_ids, attn = tokenizer.batch_tokenize(texts)
    short_len = len(tokenizer.tokenize("ک"))
    assert int(attn[0, short_len]) == 0
    assert int(input_ids[0, short_len]) == tokenizer._pad_id


def test_batch_tokenize_attention_mask(tokenizer):
    input_ids, attn = tokenizer.batch_tokenize(["a", "abc"])
    assert int(attn[1, -1]) == 1
