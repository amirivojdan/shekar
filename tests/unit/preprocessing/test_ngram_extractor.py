from shekar.transforms import (
    NGramExtractor,
)
import pytest


def test_ngram_extractor():
    ngram_extractor = NGramExtractor(range=(1, 2))
    input_text = "همان شهر ایرانش آمد به یاد"
    expected_output = [
        "همان",
        "شهر",
        "ایرانش",
        "آمد",
        "به",
        "یاد",
        "همان شهر",
        "شهر ایرانش",
        "ایرانش آمد",
        "آمد به",
        "به یاد",
    ]
    assert ngram_extractor(input_text) == expected_output
    assert ngram_extractor.fit_transform(input_text) == expected_output

    ngram_extractor = NGramExtractor(range=(1, 1))
    input_text = "هیچ جای دنیا تر و خشک را مثل ایران با هم نمی‌سوزانند."
    expected_output = [
        "هیچ",
        "جای",
        "دنیا",
        "تر",
        "و",
        "خشک",
        "را",
        "مثل",
        "ایران",
        "با",
        "هم",
        "نمی‌سوزانند",
        ".",
    ]
    assert ngram_extractor(input_text) == expected_output
    assert ngram_extractor.fit_transform(input_text) == expected_output

    ngram_extractor = NGramExtractor(range=(3, 3))
    input_text = ""
    assert ngram_extractor(input_text) == []

    input_text = "درود"
    assert ngram_extractor(input_text) == []

    input_text = "سلام دوست"
    assert ngram_extractor(input_text) == []

    ngram_extractor = NGramExtractor(range=(3, 3))
    input_text = "این یک متن نمونه است"
    expected_output = [
        "این یک متن",
        "یک متن نمونه",
        "متن نمونه است",
    ]
    assert ngram_extractor(input_text) == expected_output

    ngram_extractor = NGramExtractor(range=(2, 2))
    input_text = [
        "این یک متن",
        "یک متن نمونه",
        "متن نمونه است",
    ]
    expected_output = [
        ["این یک", "یک متن"],
        ["یک متن", "متن نمونه"],
        ["متن نمونه", "نمونه است"],
    ]
    assert list(ngram_extractor(input_text)) == expected_output
    assert list(ngram_extractor.fit_transform(input_text)) == expected_output


def test_ngram_extractor_invalid_inputs():
    with pytest.raises(
        TypeError, match="N-gram range must be a tuple tuple of integers."
    ):
        NGramExtractor(range="invalid")

    with pytest.raises(ValueError, match="N-gram range must be a tuple of length 2."):
        NGramExtractor(range=(1, 2, 3))

    with pytest.raises(ValueError, match="N-gram range must be greater than 0."):
        NGramExtractor(range=(0, 2))

    with pytest.raises(
        ValueError, match="N-gram range must be in the form of \\(min, max\\)."
    ):
        NGramExtractor(range=(3, 1))
