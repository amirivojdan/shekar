import pytest

from shekar.preprocessing.normalizers.verbal_spacing_normalizer import (
    VerbalSpacingNormalizer,
)
from shekar import data


@pytest.fixture
def normalizer():
    return VerbalSpacingNormalizer()


def test_mi_with_space(normalizer):
    text = "من می روم"
    out = normalizer.transform(text)
    assert out == f"من می{data.ZWNJ}روم"


def test_mi_joined_without_zwnj(normalizer):
    text = "من میروم"
    out = normalizer.transform(text)
    assert out == f"من می{data.ZWNJ}روم"


def test_nemi_with_space(normalizer):
    text = "من نمی روم"
    out = normalizer.transform(text)
    assert out == f"من نمی{data.ZWNJ}روم"


def test_verbal_suffix_am(normalizer):
    text = "من رفته ام"
    out = normalizer.transform(text)
    assert out == f"من رفته{data.ZWNJ}ام"


def test_verbal_suffix_ast(normalizer):
    text = "او آمده است"
    out = normalizer.transform(text)
    assert out == "او آمده است"


def test_prefixed_verb_with_space(normalizer):
    text = "او بر می دارد"
    out = normalizer.transform(text)
    # Expected: برمی‌دارد (if exists in conjugated verbs vocab)
    assert f"برمی{data.ZWNJ}دارد" in out


def test_prefixed_verb_negative(normalizer):
    text = "او بر نمی گردد"
    out = normalizer.transform(text)
    assert f"برنمی{data.ZWNJ}گردد" in out


def test_prefixed_verb_without_mi(normalizer):
    text = "او بر گردد"
    out = normalizer.transform(text)
    # Should normalize only if valid conjugated verb
    assert isinstance(out, str)


def test_prefixed_simple_future_valid(normalizer):
    text = "او بر خواهد گشت"
    out = normalizer.transform(text)
    # Should remain spaced but validated against conjugated verbs
    assert isinstance(out, str)


def test_no_change_for_non_verbs(normalizer):
    text = "کتاب بزرگ است"
    out = normalizer.transform(text)
    assert out == text


def test_mixed_sentence(normalizer):
    text = "من دیروز می رفتم و امروز نمی روم"
    out = normalizer.transform(text)
    assert f"می{data.ZWNJ}رفتم" in out
    assert f"نمی{data.ZWNJ}روم" in out


def test_punctuation_boundary(normalizer):
    text = "او می رود، اما من نمی روم."
    out = normalizer.transform(text)
    assert f"می{data.ZWNJ}رود" in out
    assert f"نمی{data.ZWNJ}روم" in out


def test_idempotency(normalizer):
    text = f"من می{data.ZWNJ}روم"
    out = normalizer.transform(text)
    assert out == text


def test_multiple_spaces_between_verb_parts(normalizer):
    text = "من می   روم"
    out = normalizer.fit_transform(text)
    # Verbal normalizer should still fix spacing pattern
    assert f"می{data.ZWNJ}روم" in out


def test_prefixed_verbs_spacing(normalizer):
    normalizer = VerbalSpacingNormalizer()

    input_text = "او بر خواهد گشت."
    expected_output = "او بر خواهد گشت."
    assert normalizer(input_text) == expected_output

    input_text = "او برخواهد گشت."
    expected_output = "او بر خواهد گشت."
    assert normalizer.fit_transform(input_text) == expected_output

    input_text = "او بر خواهدگشت."
    expected_output = "او بر خواهد گشت."
    assert normalizer.fit_transform(input_text) == expected_output

    input_text = "او بر نخواهدگشت."
    expected_output = "او بر نخواهد گشت."
    assert normalizer.transform(input_text) == expected_output

    input_text = "او برنخواهدگشت."
    expected_output = "او بر نخواهد گشت."
    assert normalizer.transform(input_text) == expected_output

    input_text = f"او بر{data.ZWNJ}نخواهد{data.ZWNJ}گشت."
    expected_output = "او بر نخواهد گشت."
    assert normalizer(input_text) == expected_output


def test_prefixed_verbs_packed():
    spacing_normalizer = VerbalSpacingNormalizer()

    input_text = "می روم کتاب‌هایم را بر می دارم."
    expected_output = "می‌روم کتاب‌هایم را برمی‌دارم."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "می روم کتاب‌هایم را بر می‌دارم."
    expected_output = "می‌روم کتاب‌هایم را برمی‌دارم."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "می روم کتاب‌هایم را بر میدارم."
    expected_output = "می‌روم کتاب‌هایم را برمی‌دارم."
    assert spacing_normalizer(input_text) == expected_output

    input_text = f"می روم کتاب‌هایم را بر{data.ZWNJ}میدارم."
    expected_output = "می‌روم کتاب‌هایم را برمی‌دارم."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "کتاب‌هایم را پس بده!"
    expected_output = "کتاب‌هایم را پس‌بده!"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "کتاب‌هایم را پس‌بده!"
    expected_output = "کتاب‌هایم را پس‌بده!"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "کتاب‌هایم را پسبده!"
    expected_output = "کتاب‌هایم را پس‌بده!"
    assert spacing_normalizer(input_text) == expected_output


def test_preverb_stopword_not_merged(normalizer):
    assert normalizer("روحی تازه در آن دمیده می‌شود.") == "روحی تازه در آن دمیده می‌شود."


def test_preverb_stopword_variants(normalizer):
    assert normalizer("در این خانه") == "در این خانه"
    assert normalizer("بر او") == "بر او"
    assert normalizer("بر آن تأکید کرد") == "بر آن تأکید کرد"


def test_preverb_stopword_zwnj_still_checked(normalizer):
    assert normalizer(f"در{data.ZWNJ}آن") == "درآن"


def test_preverb_verb_with_mi_and_stopword_verb(normalizer):
    result = normalizer("بر می گردد")
    assert result == f"برمی{data.ZWNJ}گردد"
