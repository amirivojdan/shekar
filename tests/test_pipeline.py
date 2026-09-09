import pytest

from shekar.base import BaseTransform
from shekar.pipeline import Pipeline
from shekar.preprocessing import (
    EmojiRemover,
    HTMLTagRemover,
    NonPersianRemover,
    PunctuationRemover,
)


@pytest.fixture
def mock_pipeline():
    steps = [
        EmojiRemover(),
        PunctuationRemover(),
    ]
    return Pipeline(steps=steps)


def test_pipeline_fit(mock_pipeline):
    result = mock_pipeline.fit("خدایا!خدایا،کویرم!")
    assert result == mock_pipeline


@pytest.mark.parametrize("named", [False, True])
def test_pipeline_generator_steps_are_reusable(named):
    steps = [EmojiRemover(), PunctuationRemover()]
    if named:
        steps = [("emoji", steps[0]), ("punctuation", steps[1])]
    pipeline = Pipeline(step for step in steps)

    assert len(pipeline.steps) == 2
    for _ in range(2):
        assert pipeline("سلام!🌹") == "سلام"
    assert (HTMLTagRemover() | pipeline)("<b>سلام!🌹</b>") == "سلام"
    assert (pipeline | NonPersianRemover())("سلام!🌹abc") == "سلام"


@pytest.mark.parametrize("steps", [123, [object()], [("invalid", object())]])
def test_pipeline_rejects_invalid_steps(steps):
    with pytest.raises(TypeError, match="steps must be"):
        Pipeline(steps)


def test_pipeline_fit_passes_transformed_data_to_later_steps():
    class RecordingTransform(BaseTransform):
        def fit(self, X, y=None):
            self.fit_input = X
            self.fit_target = y
            self.transform_calls = 0
            return self

        def transform(self, X):
            self.transform_calls += 1
            return [value + 1 for value in X]

    first, middle, last = (RecordingTransform() for _ in range(3))
    pipeline = Pipeline([first, middle, last])
    target = [0, 1]

    assert pipeline.fit([1, 2], target) is pipeline
    assert first.fit_input == [1, 2]
    assert middle.fit_input == [2, 3]
    assert last.fit_input == [3, 4]
    assert all(step.fit_target is target for step in (first, middle, last))
    assert [step.transform_calls for step in (first, middle, last)] == [1, 1, 0]


def test_empty_pipeline_is_identity():
    pipeline = Pipeline(iter([]))
    assert pipeline.fit("سلام") is pipeline
    assert pipeline.transform("سلام") == "سلام"


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
    with pytest.raises(TypeError, match="Input must be a string or a list of strings."):
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
    other_pipeline = Pipeline([("htmlTagRemover", HTMLTagRemover())])
    combined = mock_pipeline | other_pipeline
    assert isinstance(combined, Pipeline)

    assert len(combined.steps) == len(mock_pipeline.steps) + len(other_pipeline.steps)

    assert combined.steps[-1][0] == "htmlTagRemover"
    assert isinstance(combined.steps[-1][1], HTMLTagRemover)
    assert combined.steps[-2][0] == mock_pipeline.steps[-1][0]
    assert isinstance(combined.steps[-2][1], type(mock_pipeline.steps[-1][1]))


def test_pipeline_or_with_transformer(mock_pipeline):
    # Pipline | Transformer
    htmlTagRemover = HTMLTagRemover()
    nonPersianRemover = NonPersianRemover()
    combined = mock_pipeline | htmlTagRemover | nonPersianRemover
    assert isinstance(combined, Pipeline)
    assert len(combined.steps) == len(mock_pipeline.steps) + 2
    assert combined.steps[-1][0] == nonPersianRemover.__class__.__name__
    assert combined.steps[-1][1] is nonPersianRemover
    assert combined.steps[-2][0] == htmlTagRemover.__class__.__name__
    assert combined.steps[-2][1] is htmlTagRemover

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
        == "Pipeline(steps=[('EmojiMasker', EmojiMasker()), ('PunctuationMasker', PunctuationMasker())])"
    )


def test_pipeline_repr(mock_pipeline):
    print(repr(mock_pipeline))
    assert (
        repr(mock_pipeline)
        == "Pipeline(steps=[('EmojiMasker', EmojiMasker()), ('PunctuationMasker', PunctuationMasker())])"
    )
