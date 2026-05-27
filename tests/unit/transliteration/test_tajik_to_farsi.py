import pytest

from shekar.transliteration import TajikToFarsi


@pytest.fixture(scope="module")
def model():
    return TajikToFarsi()


def test_loads_successfully(model):
    assert model.encoder is not None
    assert model.decoder is not None


def test_direction(model):
    assert model._direction == "tg2fa"


def test_transliterates_kitob(model):
    assert model("китоб") == "کتاب"


def test_transliterates_donishgoh(model):
    assert model("донишгоҳ") == "دانشگاه"


def test_returns_string(model):
    result = model("салом")
    assert isinstance(result, str)
    assert len(result) > 0


def test_batch_transform(model):
    results = list(model(["китоб", "донишгоҳ"]))
    assert results[0] == "کتاب"
    assert results[1] == "دانشگاه"
