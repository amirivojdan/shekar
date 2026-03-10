from shekar.preprocessing.normalizers.punctuation_spacing_normalizer import (
    PunctuationSpacingNormalizer,
)


def test_punctuation_spacings():
    punct_space_normalizer = PunctuationSpacingNormalizer()

    batch_input = []
    batch_expected_output = []
    input_text = "سلام!چطوری؟"
    expected_output = "سلام! چطوری؟"
    assert punct_space_normalizer(input_text) == expected_output

    batch_input.append(input_text)
    batch_expected_output.append(expected_output)

    input_text = "شرکت « گوگل »اعلام کرد ."
    expected_output = "شرکت «گوگل» اعلام کرد."

    assert punct_space_normalizer.fit_transform(input_text) == expected_output

    batch_input.append(input_text)
    batch_expected_output.append(expected_output)

    assert list(punct_space_normalizer(batch_input)) == batch_expected_output
    assert (
        list(punct_space_normalizer.fit_transform(batch_input)) == batch_expected_output
    )


def test_punctuation_spacing_edge_cases():
    punct_space_normalizer = PunctuationSpacingNormalizer()

    input_text = "کار ما بوده ؟! حالا که چی؟!"
    expected_output = "کار ما بوده؟! حالا که چی؟!"
    assert punct_space_normalizer(input_text) == expected_output
