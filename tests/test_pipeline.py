import pytest
from shekar.pipeline import Pipeline

from shekar.preprocessing import (
    EmojiFilter,
    PunctuationFilter,
    HTMLTagFilter,
    NonPersianLetterFilter,
)


@pytest.fixture
def mock_pipeline():
    steps = [
        EmojiFilter(),
        PunctuationFilter(),
    ]
    return Pipeline(steps=steps)


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

        process_text("ایران سرای من است")


def test_pipeline_or_with_pipeline(mock_pipeline):
    # Pipline | Pipeline
    other_pipeline = Pipeline([("htmlFilter", HTMLTagFilter())])
    combined = mock_pipeline | other_pipeline
    assert isinstance(combined, Pipeline)

    assert len(combined.steps) == len(mock_pipeline.steps) + len(other_pipeline.steps)

    assert combined.steps[-1][0] == "htmlFilter"
    assert isinstance(combined.steps[-1][1], HTMLTagFilter)
    assert combined.steps[-2][0] == mock_pipeline.steps[-1][0]
    assert isinstance(combined.steps[-2][1], type(mock_pipeline.steps[-1][1]))


def test_pipeline_or_with_transformer(mock_pipeline):
    # Pipline | Transformer
    htmlRemover = HTMLTagFilter()
    nonPersianRemover = NonPersianLetterFilter()
    combined = mock_pipeline | htmlRemover | nonPersianRemover
    assert isinstance(combined, Pipeline)
    assert len(combined.steps) == len(mock_pipeline.steps) + 2
    assert combined.steps[-1][0] == nonPersianRemover.__class__.__name__
    assert combined.steps[-1][1] is nonPersianRemover
    assert combined.steps[-2][0] == htmlRemover.__class__.__name__
    assert combined.steps[-2][1] is htmlRemover

    input_text = "خدایا! خدایا، <b>کویرم!</b>"
    result = combined(input_text)
    assert result == "خدایا خدایا کویرم"


def test_pipeline_or_invalid_type(mock_pipeline):
    with pytest.raises(
        TypeError,
        match="Unsupported type for pipeline concatenation: <class 'int'>",
    ):
        _ = mock_pipeline | 123


def test_pipeline_str(mock_pipeline):
    assert (
        str(mock_pipeline)
        == "Pipeline(steps=[('EmojiFilter', EmojiFilter()), ('PunctuationFilter', PunctuationFilter())])"
    )


def test_pipeline_repr(mock_pipeline):
    print(repr(mock_pipeline))
    assert (
        repr(mock_pipeline)
        == "Pipeline(steps=[('EmojiFilter', EmojiFilter()), ('PunctuationFilter', PunctuationFilter())])"
    )
