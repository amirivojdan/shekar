from shekar.ner.albert_ner import AlbertNER


def test_albert_ner_model_loads_successfully():
    model = AlbertNER()
    assert model.session is not None
    assert hasattr(model, "transform")
    assert callable(model.transform)
    assert isinstance(model.id2tag, dict)
    assert "B-PER" in model.id2tag.values()


def test_albert_ner_transform_output_format():
    model = AlbertNER()
    text = "من علی‌رضا امیری هستم و در دانشگاه تهران تحصیل می‌کنم."

    output = model.transform(text)

    assert isinstance(output, list)
    assert all(isinstance(ent, tuple) and len(ent) == 2 for ent in output)

    for entity, label in output:
        assert isinstance(entity, str)
        assert isinstance(label, str)
        assert label in {"DAT", "EVE", "LOC", "ORG", "PER"}


def test_albert_ner_detects_known_entities():
    model = AlbertNER()
    text = "دکتر علی‌رضا امیری در دانشگاه تهران تحصیل می‌کند."
    output = model.transform(text)
    entities = {e[0]: e[1] for e in output}

    assert "دکتر علی‌رضا امیری" in entities
    assert entities["دکتر علی‌رضا امیری"] == "PER"

    assert "دانشگاه تهران" in entities
    assert entities["دانشگاه تهران"] == "LOC"


def test_albert_ner_fit_returns_self():
    model = AlbertNER()
    result = model.fit(["dummy text"])
    assert result is model
