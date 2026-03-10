import numpy as np
import pytest
from unittest.mock import MagicMock
from shekar.ner.albert_ner import AlbertNER


@pytest.fixture(scope="module")
def ner_model():
    return AlbertNER()


def test_albert_ner_model_loads_successfully(ner_model):
    assert ner_model.session is not None
    assert hasattr(ner_model, "transform")
    assert callable(ner_model.transform)
    assert isinstance(ner_model.id2tag, dict)
    assert "B-PER" in ner_model.id2tag.values()


def test_albert_ner_transform_output_format(ner_model):
    text = "من علی‌رضا امیری هستم و در دانشگاه تهران تحصیل می‌کنم."
    output = ner_model.transform(text)

    assert isinstance(output, list)
    assert all(isinstance(ent, tuple) and len(ent) == 2 for ent in output)

    for entity, label in output:
        assert isinstance(entity, str)
        assert isinstance(label, str)
        assert label in {"DAT", "EVE", "LOC", "ORG", "PER"}


def test_albert_ner_detects_known_entities(ner_model):
    text = "دکتر علی‌رضا امیری در دانشگاه تهران تحصیل می‌کند."
    output = ner_model.transform(text)
    entities = {e[0]: e[1] for e in output}

    assert "دکتر علی‌رضا امیری" in entities
    assert entities["دکتر علی‌رضا امیری"] == "PER"

    assert "دانشگاه تهران" in entities
    assert entities["دانشگاه تهران"] == "LOC"


def test_albert_ner_fit_returns_self(ner_model):
    result = ner_model.fit(["dummy text"])
    assert result is ner_model


# --- _aggregate_entities branch coverage ---


def test_aggregate_entities_skips_cls_sep_tokens(ner_model):
    # line 45: [CLS]/[SEP] tokens hit `continue`
    tokens = ["[CLS]", "▁علی", "[SEP]"]
    tag_ids = np.array([10, 4, 10])  # O, B-PER, O
    result = ner_model._aggregate_entities(tokens, tag_ids)
    assert result == [("علی", "PER")]


def test_aggregate_entities_consecutive_b_labels(ner_model):
    # line 57: new B- seen while current_entity is non-empty → flush previous entity
    tokens = ["▁علی", "▁تهران"]
    tag_ids = np.array([4, 2])  # B-PER, B-LOC
    result = ner_model._aggregate_entities(tokens, tag_ids)
    assert ("علی", "PER") in result
    assert ("تهران", "LOC") in result


def test_aggregate_entities_subword_continuation(ner_model):
    # line 66: I- token without ▁ prefix and current entity has no ZWNJ
    tokens = ["▁علی", "رضا"]
    tag_ids = np.array([4, 9])  # B-PER, I-PER
    result = ner_model._aggregate_entities(tokens, tag_ids)
    assert result == [("علیرضا", "PER")]


def test_aggregate_entities_trailing_entity(ner_model):
    # line 74: entity still open when loop ends → appended after loop
    tokens = ["▁تهران"]
    tag_ids = np.array([2])  # B-LOC
    result = ner_model._aggregate_entities(tokens, tag_ids)
    assert result == [("تهران", "LOC")]


# --- transform multi-batch branch coverage ---


def _make_transform_mocks(ner_model, B, L, stride, mask_rows=None):
    """Helper: patch tokenizer/session on ner_model for transform tests."""
    input_ids = np.arange(B * L, dtype=np.int64).reshape(B, L)
    attention_mask = np.ones((B, L), dtype=np.int64)
    if mask_rows:
        for r in mask_rows:
            attention_mask[r] = 0

    mock_tok = MagicMock()
    mock_tok.return_value = {"input_ids": input_ids, "attention_mask": attention_mask}
    mock_tok.tokenizer.token_to_id.return_value = None  # no special ids
    mock_tok.tokenizer.id_to_token.return_value = "▁و"  # non-entity word
    mock_tok.stride = stride

    logits = np.zeros((B, L, 11))
    logits[:, :, 10] = 1.0  # all O tags

    mock_sess = MagicMock()
    mock_sess.get_inputs.return_value = [
        MagicMock(name="input_ids"),
        MagicMock(name="attention_mask"),
    ]
    mock_sess.run.return_value = [logits]

    ner_model.tokenizer = mock_tok
    ner_model.session = mock_sess


def test_transform_stride_trims_overlap(ner_model):
    # line 117: b > 0 and stride > 0 → valid_pos = valid_pos[stride:]
    _make_transform_mocks(ner_model, B=2, L=6, stride=2)
    result = ner_model.transform("some text")
    assert isinstance(result, list)


def test_transform_empty_valid_pos_continues(ner_model):
    # line 120: batch with all-zero mask → valid_pos empty → continue
    _make_transform_mocks(ner_model, B=2, L=4, stride=0, mask_rows=[1])
    result = ner_model.transform("some text")
    assert isinstance(result, list)
