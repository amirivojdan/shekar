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


def test_empty_text_returns_empty(model):
    assert model("") == ""
    assert model("   ") == ""


def test_multi_sentence_text_is_not_truncated(model):
    sentence = "من در دانشگاه تهران درس می‌خوانم و هر روز به کتابخانه می‌روم."
    text = " ".join([sentence] * 4) + "\nخداحافظ!"
    result = model(text)
    single = model(sentence)
    assert "�" not in result
    assert result.split("\n")[0] == " ".join([single] * 4)
    assert result.count("\n") == 1


def test_long_unpunctuated_text_is_complete(model):
    text = (
        "من در دانشگاه تهران درس می‌خوانم و هر روز به کتابخانه می‌روم و "
        "کتاب‌های زیادی درباره تاریخ ایران و فرهنگ مردم این سرزمین می‌خوانم "
        "دوستانم نیز گاهی همراه من می‌آیند و با هم درباره شعر حافظ و سعدی "
        "و مولانا گفتگو می‌کنیم بعد از ظهر به خانه برمی‌گردم"
    )
    result = model(text)
    assert "�" not in result
    words = result.split()
    # Output length tracks the input (no truncation, no runaway repetition).
    assert 0.8 * len(text.split()) <= len(words) <= 1.2 * len(text.split())


def test_batch_matches_single_for_long_documents(model):
    texts = ["سلام. خداحافظ!", "", "کتاب\nدانشگاه"]
    assert model.transform_batch(texts, batch_size=2) == [model(t) for t in texts]


def test_small_max_new_tokens_warns():
    tiny = FarsiToTajik(max_new_tokens=4)
    with pytest.warns(RuntimeWarning, match="max_new_tokens"):
        tiny("دانشگاه تهران")
