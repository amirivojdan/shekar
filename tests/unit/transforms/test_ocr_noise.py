import pytest

from shekar.transforms.noise.ocr import OCRNoise


@pytest.fixture
def noise():
    return OCRNoise(seed=42)


def test_invalid_substitution_prob():
    with pytest.raises(ValueError):
        OCRNoise(substitution_prob=1.5)


def test_invalid_deletion_prob():
    with pytest.raises(ValueError):
        OCRNoise(deletion_prob=-0.1)


def test_invalid_repeat_prob():
    with pytest.raises(ValueError):
        OCRNoise(repeat_prob=2.0)


def test_zero_probabilities_is_identity():
    ocr = OCRNoise(substitution_prob=0, deletion_prob=0, repeat_prob=0, seed=0)
    text = "این یک متن آزمایشی است"
    assert ocr(text) == text


def test_deterministic_with_seed():
    text = "سلام دنیا"
    assert OCRNoise(seed=42)(text) == OCRNoise(seed=42)(text)


def test_output_is_string(noise):
    assert isinstance(noise("متن نمونه برای تست"), str)


def test_unmapped_chars_pass_through():
    # spaces, digits not in confusion map, punctuation — all unchanged
    ocr = OCRNoise(substitution_prob=1.0, deletion_prob=1.0, repeat_prob=1.0, seed=0)
    assert ocr("   ") == "   "
    assert ocr("abc") == "abc"


def test_deletion_removes_char():
    # deletion_prob=1 should delete every mapped character
    ocr = OCRNoise(substitution_prob=0, deletion_prob=1.0, repeat_prob=0, seed=0)
    # 'ب' is in the confusion map — must be deleted
    assert ocr("ب") == ""


def test_repeat_doubles_char():
    # deletion_prob=0, repeat_prob=1 should double every mapped character
    ocr = OCRNoise(substitution_prob=0, deletion_prob=0, repeat_prob=1.0, seed=0)
    assert ocr("ب") == "بب"


def test_substitution_replaces_with_confusion():
    # deletion_prob=0, repeat_prob=0, substitution_prob=1 — char must be replaced
    ocr = OCRNoise(substitution_prob=1.0, deletion_prob=0, repeat_prob=0, seed=0)
    result = ocr("ب")
    assert result in ocr._ocr_confusions["ب"]


def test_deletion_takes_priority_over_repeat():
    # Both deletion and repeat at prob=1 — deletion fires first, char disappears
    ocr = OCRNoise(substitution_prob=0, deletion_prob=1.0, repeat_prob=1.0, seed=0)
    assert ocr("ب") == ""


def test_repeat_takes_priority_over_substitution():
    # deletion=0, repeat=1, substitution=1 — repeat fires, char doubled not substituted
    ocr = OCRNoise(substitution_prob=1.0, deletion_prob=0, repeat_prob=1.0, seed=0)
    assert ocr("ب") == "بب"


def test_all_confusion_map_keys_are_mapped(noise):
    for key, candidates in noise._ocr_confusions.items():
        assert len(candidates) > 0, f"Empty confusion list for '{key}'"


def test_output_length_with_deletion():
    ocr = OCRNoise(substitution_prob=0, deletion_prob=1.0, repeat_prob=0, seed=0)
    text = "بپتث"  # all mapped chars
    assert len(ocr(text)) == 0


def test_output_length_with_repeat():
    ocr = OCRNoise(substitution_prob=0, deletion_prob=0, repeat_prob=1.0, seed=0)
    text = "بپ"  # 2 mapped chars
    assert len(ocr(text)) == 4


def test_mixed_mapped_and_unmapped():
    ocr = OCRNoise(substitution_prob=0, deletion_prob=1.0, repeat_prob=0, seed=0)
    # 'س' is mapped, spaces and 'a' are not
    result = ocr("a س b")
    assert "a" in result
    assert "b" in result
    assert " " in result
    assert "س" not in result


def test_numeral_confusion():
    # '۱' should be confused with 'ل'
    ocr = OCRNoise(substitution_prob=1.0, deletion_prob=0, repeat_prob=0, seed=0)
    result = ocr("۱")
    assert result in ocr._ocr_confusions["۱"]


def test_output_under_heavy_noise():
    ocr = OCRNoise(substitution_prob=0.5, deletion_prob=0.3, repeat_prob=0.3, seed=7)
    assert isinstance(ocr("متن نمونه برای تست سیستم"), str)
