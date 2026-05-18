import pytest

from shekar.transforms.noise.keyboard import KeyboardNoise


@pytest.fixture
def noise():
    return KeyboardNoise(seed=42)


def test_keyboard_layout_row_count_matches_shifted(noise):
    assert len(noise.keyboard_layout) == len(noise.shifted_keyboard_layout)


def test_keyboard_layout_row_lengths_match_shifted(noise):
    for i, (row, shifted_row) in enumerate(
        zip(noise.keyboard_layout, noise.shifted_keyboard_layout)
    ):
        assert len(row) == len(shifted_row), (
            f"Row {i} length mismatch: keyboard={len(row)}, shifted={len(shifted_row)}"
        )


def test_shifted_only_does_not_crash():
    noise = KeyboardNoise(
        seed=42,
        substitution_prob=0,
        insertion_prob=0,
        deletion_prob=0,
        repeat_prob=0,
        shifted_prob=1.0,
    )
    out = noise("سلام")
    assert isinstance(out, str)


def test_shift_letters_false_never_shifts_letters():
    # With shift_letters=False (default), letters must pass through unchanged
    # even when shifted_prob=1.0.
    noise = KeyboardNoise(
        seed=0,
        substitution_prob=0,
        insertion_prob=0,
        deletion_prob=0,
        repeat_prob=0,
        shifted_prob=1.0,
        shift_letters=False,
    )
    text = "سلام"
    assert noise(text) == text


def test_shift_letters_false_does_shift_digits_and_punctuation():
    # Digits and punctuation must be shifted when shifted_prob=1.0.
    noise = KeyboardNoise(
        seed=0,
        substitution_prob=0,
        insertion_prob=0,
        deletion_prob=0,
        repeat_prob=0,
        shifted_prob=1.0,
        shift_letters=False,
    )
    # '1' -> '!', '/' -> '؟'
    assert noise("1") == "!"
    assert noise("/") == "؟"


def test_shift_letters_true_can_shift_letters():
    # With shift_letters=True, a Persian letter must be shiftable.
    noise = KeyboardNoise(
        seed=0,
        substitution_prob=0,
        insertion_prob=0,
        deletion_prob=0,
        repeat_prob=0,
        shifted_prob=1.0,
        shift_letters=True,
    )
    # 'س' is on the keyboard; its shifted form must differ from the original.
    result = noise("س")
    assert result != "س"


def test_shiftable_set_default_contains_only_non_alpha(noise):
    assert all(not ch.isalpha() for ch in noise._shiftable)


def test_shiftable_set_shift_letters_true_contains_letters():
    noise = KeyboardNoise(shift_letters=True, seed=0)
    letters = {ch for ch in noise._shiftable if ch.isalpha()}
    assert len(letters) > 0


def test_zero_probabilities_is_identity():
    noise = KeyboardNoise(
        seed=1,
        substitution_prob=0,
        insertion_prob=0,
        deletion_prob=0,
        repeat_prob=0,
        shifted_prob=0,
    )
    text = "این یک متن آزمایشی است"
    assert noise(text) == text


def test_deterministic_with_seed():
    text = "سلام دنیا"
    assert KeyboardNoise(seed=42)(text) == KeyboardNoise(seed=42)(text)


def test_non_keyboard_chars_pass_through():
    # spaces, ZWNJ, newlines untouched at any setting
    noise = KeyboardNoise(seed=0, substitution_prob=1.0)
    assert " " in noise("a b")  # space survives


def test_output_is_string_under_heavy_noise():
    noise = KeyboardNoise(
        seed=7,
        substitution_prob=0.5,
        insertion_prob=0.5,
        deletion_prob=0.5,
        repeat_prob=0.5,
        shifted_prob=0.5,
    )
    assert isinstance(noise("متن نمونه برای تست"), str)
