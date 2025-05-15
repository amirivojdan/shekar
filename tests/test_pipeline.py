import pytest
from shekar.pipeline import Pipeline
from shekar.preprocessing import EmojiRemover, PunctuationRemover


@pytest.fixture
def mock_pipeline():
    steps = [
        ("removeEmoji", EmojiRemover()),
        ("removePunct", PunctuationRemover()),
    ]
    return Pipeline(steps)


def test_pipeline_fit(mock_pipeline):
    result = mock_pipeline.fit("خدایا!خدایا،کویرم!")
    assert result == mock_pipeline


def test_pipeline_transform(mock_pipeline):
    result = mock_pipeline.transform("پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!")
    assert result == "پرنده‌های  قفسی عادت دارن به بی‌کسی"


def test_pipeline_fit_transform_string(mock_pipeline):
    result = mock_pipeline.fit_transform("پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!")
    assert result == "پرنده‌های  قفسی عادت دارن به بی‌کسی"


def test_pipeline_fit_transform_list(mock_pipeline):
    input_data = ["یادته گل رز قرمز 🌹 به تو دادم؟", "بگو یهویی از کجا پیدات شد؟"]
    result = list(mock_pipeline.fit_transform(input_data))
    assert result == [
        "یادته گل رز قرمز  به تو دادم",
        "بگو یهویی از کجا پیدات شد",
    ]


def test_pipeline_fit_transform_invalid_input(mock_pipeline):
    with pytest.raises(
        ValueError, match="Input must be a string or a list of strings."
    ):
        mock_pipeline.fit_transform(123)


def test_pipeline_call(mock_pipeline):
    result = mock_pipeline("تو را من چشم👀 در راهم!")
    assert result == "تو را من چشم در راهم"


def test_pipeline_on_args_decorator(mock_pipeline):
    @mock_pipeline.on_args("text")
    def process_text(text):
        return text

    result = process_text("عمری دگر بباید بعد از وفات ما را!🌞")
    assert result == "عمری دگر بباید بعد از وفات ما را"


def test_pipeline_on_args_multiple_params(mock_pipeline):
    @mock_pipeline.on_args(["text", "description"])
    def process_text_and_description(text, description):
        return text, description

    result = process_text_and_description("ناز داره چو وای!", "مهرهٔ مار داره تو دلبری❤️")
    assert result == ("ناز داره چو وای", "مهرهٔ مار داره تو دلبری")


def test_pipeline_on_args_invalid_param(mock_pipeline):
    @mock_pipeline.on_args("invalid_param")
    def process_text(text):
        return text

    with pytest.raises(
        ValueError, match="Parameter 'invalid_param' not found in function arguments."
    ):
        process_text("input_data")


def test_pipeline_on_args_invalid_type(mock_pipeline):
    with pytest.raises(
        TypeError, match="param_names must be a string or an iterable of strings"
    ):

        @mock_pipeline.on_args([123])  # invalid param name: int instead of str
        def process_text(text):
            return text
