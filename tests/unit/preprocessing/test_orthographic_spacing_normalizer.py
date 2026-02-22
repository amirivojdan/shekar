from shekar.preprocessing.normalizers.orthographic_spacing_normalizer import (
    OrthographicSpacingNormalizer,
)


def test_remove_extra_spaces():
    spacing_normalizer = OrthographicSpacingNormalizer()

    input_text = "این  یک  آزمون  است"
    expected_output = "این یک آزمون است"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "این\u200cیک\u200cآزمون\u200cاست"
    expected_output = "این\u200cیک\u200cآزمون\u200cاست"
    assert spacing_normalizer.fit_transform(input_text) == expected_output

    input_text = "این\u200c یک\u200c آزمون\u200c است"
    expected_output = "این یک آزمون است"
    assert spacing_normalizer(input_text) == expected_output

    # test ZWNJ after non-left joiner letters!
    input_text = "چهار‌لاچنگ"
    expected_output = "چهارلاچنگ"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "این  یک  آزمون  است  "
    expected_output = "این یک آزمون است"
    assert spacing_normalizer.fit_transform(input_text) == expected_output

    input_text = "این  یک  آزمون  است\n\n\n\n"
    expected_output = "این یک آزمون است"
    assert spacing_normalizer(input_text) == expected_output
