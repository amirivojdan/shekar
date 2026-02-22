from shekar.preprocessing.normalizers import YaNormalizer


def test_ya_normalizer():
    ya_normalizer = YaNormalizer(style="standard")

    input_text = "خانه‌ی ما"
    expected_output = "خانۀ ما"
    assert ya_normalizer(input_text) == expected_output

    ya_normalizer = YaNormalizer()
    input_text = "خانۀ ما"
    expected_output = "خانه‌ی ما"
    assert ya_normalizer(input_text) == expected_output
