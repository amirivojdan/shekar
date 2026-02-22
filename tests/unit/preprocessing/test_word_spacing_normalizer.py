from shekar.preprocessing.normalizers.word_spacing_normalizer import (
    WordSpacingNormalizer,
)

# Create a single instance for testing
normalizer = WordSpacingNormalizer()


def test_compound_words():
    input_text = "او یک کار آفرین نمونه است."
    expected = "او یک کارآفرین نمونه است."
    output = normalizer(input_text)
    assert output == expected, f"Expected: {expected}, Got: {output}"


def test_prefix_spacing():
    input_text = "اظهار نامه مالیاتی را پر کنید"
    expected = "اظهارنامه مالیاتی را پر کنید"
    output = normalizer(input_text)
    assert output == expected, f"Expected: {expected}, Got: {output}"


def test_suffix_spacing():
    input_text = "کتاب ها روی میز است"
    expected = "کتاب‌ها روی میز است"
    output = normalizer(input_text)
    assert output == expected, f"Expected: {expected}, Got: {output}"

    input_text = "بزرگ تر از من است"
    expected = "بزرگ‌تر از من است"
    output = normalizer(input_text)
    assert output == expected, f"Expected: {expected}, Got: {output}"


def test_morph_suffix_spacing():
    """
    Test morphological suffixes that only correct if stem exists in vocab.
    """
    input_text = "کتاب هایش را برد"
    expected = "کتاب‌هایش را برد"
    output = normalizer(input_text)
    assert output == expected, f"Expected: {expected}, Got: {output}"

    input_text = "خانه ام بزرگ است"
    expected = "خانه‌ام بزرگ است"
    output = normalizer(input_text)
    assert output == expected, f"Expected: {expected}, Got: {output}"


def test_non_left_joiner_compound_words():
    input_text = "دیدن آن صحنه منزجر کننده بود!"
    expected_output = "دیدن آن صحنه منزجرکننده بود!"
    assert normalizer(input_text) == expected_output

    input_text = "کار آفرینی بسیار ارزشمند است."
    expected_output = "کارآفرینی بسیار ارزشمند است."
    assert normalizer(input_text) == expected_output

    input_text = "یک کتابخانه خوب باید کاربر پسند باشد!"
    expected_output = "یک کتابخانه خوب باید کاربرپسند باشد!"
    assert normalizer(input_text) == expected_output
