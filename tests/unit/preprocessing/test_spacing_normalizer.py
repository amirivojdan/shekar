import pytest

from shekar.preprocessing.normalizers.spacing_normalizer import SpacingNormalizer


def test_correct_spacings():
    spacing_normalizer = SpacingNormalizer()

    input_text = (
        "میرویم به خانههای خاک آلود که گفته اند تا چند سال بعد تر ویران نمی شوند !"
    )
    expected_output = (
        "می‌رویم به خانه‌های خاک‌آلود که گفته‌اند تا چند سال بعدتر ویران نمی‌شوند!"
    )
    assert spacing_normalizer(input_text) == expected_output

    input_text = "خونه هاشون خیلی گرون تر شده"
    expected_output = "خونه‌هاشون خیلی گرون‌تر شده"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "دوقلو های هم خون"
    expected_output = "دوقلوهای هم‌خون"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "بنیان گذار خانه هایمان"
    expected_output = "بنیان‌گذار خانه‌هایمان"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "هم شاید"
    expected_output = "هم شاید"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "   این یک جمله   نمونه   است. "
    expected_output = "این یک جمله نمونه است."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "اینجا کجاست؟تو میدانی؟نمیدانم!"
    expected_output = "اینجا کجاست؟ تو می‌دانی؟ نمی‌دانم!"
    assert spacing_normalizer.fit_transform(input_text) == expected_output

    input_text = "ناصر گفت:«من می‌روم.»"
    expected_output = "ناصر گفت: «من می‌روم.»"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "با کی داری حرف می زنی؟"
    expected_output = "با کی داری حرف می‌زنی؟"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "من می‌روم.تو نمی‌آیی؟"
    expected_output = "من می‌روم. تو نمی‌آیی؟"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "به نکته ریزی اشاره کردی!"
    expected_output = "به نکته ریزی اشاره کردی!"
    assert spacing_normalizer.fit_transform(input_text) == expected_output

    sentences = ["   این یک جمله   نمونه   است. ", "با کی داری حرف می زنی؟"]
    expected_output = ["این یک جمله نمونه است.", "با کی داری حرف می‌زنی؟"]
    assert list(spacing_normalizer(sentences)) == expected_output
    assert list(spacing_normalizer.fit_transform(sentences)) == expected_output

    input_text = 13.4
    expected_output = "Input must be a string or a list of strings."
    with pytest.raises(ValueError, match=expected_output):
        spacing_normalizer(input_text)
