import pytest

from shekar.transliteration import FarsiToTajik


@pytest.fixture(scope="module")
def model():
    return FarsiToTajik()


def test_loads_successfully(model):
    assert model.encoder is not None
    assert model.decoder is not None


def test_direction(model):
    assert model._direction == "fa2tg"


def test_transliterates_kitab(model):
    assert model("کتاب") == "китоб"


def test_transliterates_daneshgah(model):
    assert model("دانشگاه") == "донишгоҳ"


def test_returns_string(model):
    result = model("سلام")
    assert isinstance(result, str)
    assert len(result) > 0


def test_batch_transform(model):
    results = list(model(["کتاب", "دانشگاه"]))
    assert results[0] == "китоб"
    assert results[1] == "донишгоҳ"
