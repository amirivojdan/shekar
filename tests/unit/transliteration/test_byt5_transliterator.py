import pytest

from shekar.transliteration.byt5_transliterator import (
    _MAX_CHUNK_BYTES,
    ByT5Transliterator,
)

split = ByT5Transliterator._split_sentences

LONG_SENTENCE = " ".join(["کتاب‌های زیادی درباره تاریخ ایران می‌خوانم"] * 12)


@pytest.mark.parametrize(
    "text",
    [
        "سلام",
        "سلام. خوبی؟ خداحافظ!",
        "خط اول\nخط دوم\n\n\nخط سوم",
        "  سلام.   خوبی؟\t\n خداحافظ  ",
        "Салом! Эрон модар аст.",
        "۳.۵ درصد",
        LONG_SENTENCE,
        LONG_SENTENCE + ". " + LONG_SENTENCE,
    ],
)
def test_split_round_trips_stripped_text(text):
    parts, indices = split(text)
    assert "".join(parts) == text.strip()
    assert all(i % 2 == 0 and parts[i].strip() for i in indices)


def test_split_on_sentence_punctuation_and_newlines():
    parts, indices = split("سلام. خوبی؟\nخداحافظ")
    assert [parts[i] for i in indices] == ["سلام.", "خوبی؟", "خداحافظ"]


def test_split_keeps_decimal_points_inside_a_sentence():
    parts, indices = split("قیمت ۳.۵ دلار است.")
    assert [parts[i] for i in indices] == ["قیمت ۳.۵ دلار است."]


def test_long_sentence_is_chunked_at_word_boundaries():
    parts, indices = split(LONG_SENTENCE)
    chunks = [parts[i] for i in indices]
    assert len(chunks) > 1
    assert all(len(chunk.encode("utf-8")) <= _MAX_CHUNK_BYTES for chunk in chunks)
    assert " ".join(chunks).split() == LONG_SENTENCE.split()


def test_single_overlong_word_is_kept_whole():
    word = "ب" * _MAX_CHUNK_BYTES
    parts, indices = split(f"سلام {word} سلام")
    assert word in [parts[i] for i in indices]


@pytest.mark.parametrize("text", ["", "   ", "\n\n"])
def test_blank_text_has_no_segments(text):
    assert split(text)[1] == []


def test_blank_documents_need_no_model():
    model = ByT5Transliterator.__new__(ByT5Transliterator)
    assert model._transform_batch(["", "  "], 2) == ["", ""]


def test_auto_max_new_tokens_scales_with_input():
    model = ByT5Transliterator.__new__(ByT5Transliterator)
    model.max_new_tokens = None
    short = model._max_new_tokens(["fa2tg: کتاب"])
    long = model._max_new_tokens(["fa2tg: " + "کتاب " * 40])
    assert short < long
    assert long > len(("fa2tg: " + "کتاب " * 40).encode("utf-8"))
    model.max_new_tokens = 24
    assert model._max_new_tokens(["fa2tg: " + "کتاب " * 40]) == 24
