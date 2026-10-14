from types import SimpleNamespace
from unittest.mock import MagicMock

import numpy as np
import pytest

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


# --- chunk stitching (runs on a private instance; the shared fixture is untouched) ---


def _stitching_model(input_ids, attention_mask, stride):
    """AlbertNER with a fake tokenizer/session; returns (model, captured tokens)."""
    model = AlbertNER.__new__(AlbertNER)
    model.batch_size = 8
    model.id2tag = {10: "O"}
    model.tokenizer = MagicMock(
        return_value={"input_ids": input_ids, "attention_mask": attention_mask},
        pad_token_id=0,
        cls_token_id=0,
        sep_token_id=0,
        unk_token_id=0,
        stride=stride,
        id_to_token=lambda i: f"▁t{i}",
    )
    model.session = MagicMock()
    model.session.get_inputs.return_value = [
        SimpleNamespace(name="input_ids", shape=["batch", "seq"]),
        SimpleNamespace(name="attention_mask", shape=["batch", "seq"]),
    ]

    def run(_, feed):
        logits = np.zeros((*feed["input_ids"].shape, 11))
        logits[..., 10] = 1.0  # every position tagged "O"
        return [logits]

    model.session.run.side_effect = run
    captured = []
    model._aggregate_entities = lambda tokens, tags: captured.append(tokens) or []
    return model, captured


def test_transform_stride_trims_overlap():
    # Two overlapping chunks: the first `stride` real tokens of chunk 2 repeat
    # the end of chunk 1 and must be dropped. Id 0 marks CLS/SEP/padding.
    input_ids = np.array([[0, 1, 2, 3, 4, 0], [0, 3, 4, 5, 6, 0]])
    model, captured = _stitching_model(input_ids, np.ones_like(input_ids), stride=2)
    assert model.transform("some text") == []
    assert captured == [["▁t1", "▁t2", "▁t3", "▁t4", "▁t5", "▁t6"]]


def test_transform_fully_masked_chunk_contributes_nothing():
    input_ids = np.array([[0, 1, 2, 0], [0, 7, 8, 0]])
    attention_mask = np.array([[1, 1, 1, 1], [0, 0, 0, 0]])
    model, captured = _stitching_model(input_ids, attention_mask, stride=0)
    assert model.transform("some text") == []
    assert captured == [["▁t1", "▁t2"]]


def test_inputs_are_padded_to_batch_maximum_not_model_limit(ner_model, monkeypatch):
    widths = []
    run = ner_model.session.run

    def recording_run(names, feed):
        widths.append(feed["input_ids"].shape[1])
        return run(names, feed)

    monkeypatch.setattr(ner_model.session, "run", recording_run)
    ner_model.transform_batch(["علی به تهران رفت.", "سلام"], batch_size=2)
    assert widths and max(widths) < ner_model.tokenizer.model_max_length
