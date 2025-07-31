import pytest
from shekar.ner import NER
from shekar.ner.albert_ner import AlbertNER


def test_ner_default_model_is_albert():
    ner = NER()
    assert isinstance(ner.model, AlbertNER)


def test_ner_invalid_model_raises():
    with pytest.raises(ValueError, match="Unknown NER model 'foobar'"):
        NER("foobar")


def test_ner_transform_outputs_entities():
    ner = NER()
    text = "من علی‌رضا امیری هستم و در دانشگاه تهران تحصیل می‌کنم."

    entities = ner.transform(text)

    # Should be a list of tuples or dicts
    assert isinstance(entities, list)
    assert all(isinstance(ent, tuple) for ent in entities)

    # Check format: (text, label)
    for ent in entities:
        assert isinstance(ent[0], str)  # entity text
        assert isinstance(ent[1], str)  # entity label


def test_ner_fit_returns_model():
    ner = NER()
    result = ner.fit(["متن تست"], [["O", "B-PER", "I-PER"]])
    assert result is ner


def test_ner_detects_known_entities():
    ner = NER()
    text = "دکتر علی‌رضا امیری در دانشگاه تهران تدریس می‌کند."
    entities = ner.transform(text)
    print(entities)
    entity_texts = [e[0] for e in entities]
    assert "دکتر علی‌رضا امیری" in entity_texts
    assert "دانشگاه تهران" in entity_texts
