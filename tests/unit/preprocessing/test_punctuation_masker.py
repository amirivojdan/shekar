from shekar.preprocessing.maskers import PunctuationMasker


def test_default_removes_persian_and_ascii_punctuation():
    masker = PunctuationMasker()
    assert masker("دریغ است ایران که ویران شود!") == "دریغ است ایران که ویران شود"


def test_custom_punctuations_removes_only_specified_chars():
    masker = PunctuationMasker(punctuations="!?")
    assert masker("سلام!") == "سلام"
    assert masker("چطوری؟") == "چطوری؟"


def test_custom_mask_token_replaces_instead_of_removing():
    masker = PunctuationMasker(mask_token=" ")
    result = masker("سلام!")
    assert "!" not in result


def test_empty_string_returns_empty():
    masker = PunctuationMasker()
    assert masker("") == ""
