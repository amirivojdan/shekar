from shekar.preprocessing.normalizers import YaNormalizer


def test_ya_normalizer_standard():
    ya_normalizer = YaNormalizer(style="standard")
    assert ya_normalizer("خانه‌ی ما") == "خانۀ ما"
    # "ه ی" where ی is a standalone ezafe particle
    assert ya_normalizer("خانه ی ما") == "خانۀ ما"


def test_ya_normalizer_standard_no_cross_word_boundary():
    ya_normalizer = YaNormalizer(style="standard")
    assert ya_normalizer("که یه") == "که یه"
    assert ya_normalizer("خانه یک") == "خانه یک"


def test_ya_normalizer_joda():
    ya_normalizer = YaNormalizer(style="joda")
    assert ya_normalizer("خانۀ ما") == "خانه‌ی ما"
    # "ه ی" where ی is a standalone ezafe particle
    assert ya_normalizer("خانه ی ما") == "خانه‌ی ما"


def test_ya_normalizer_no_cross_word_boundary():
    ya_normalizer = YaNormalizer(style="joda")
    # ی at start of next word should not be joined to preceding ه
    assert ya_normalizer("که یه") == "که یه"
    assert ya_normalizer("خانه یک") == "خانه یک"
