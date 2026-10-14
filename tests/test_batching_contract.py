from types import SimpleNamespace

import numpy as np
import pytest

from shekar.base import BaseTransform
from shekar.embeddings.albert_embedder import AlbertEmbedder
from shekar.pipeline import Pipeline
from shekar.preprocessing import PunctuationRemover
from shekar.tokenization import AlbertTokenizer


@pytest.mark.parametrize("size", [0, -1, True, False, 1.5, "2", None])
def test_invalid_batch_sizes(size):
    with pytest.raises(ValueError, match="positive integer"):
        BaseTransform._validate_batch_size(size)


@pytest.mark.parametrize(
    "texts", [None, 123, "text", b"text", {"text": "value"}, ["ok", None]]
)
def test_invalid_batch_input(texts):
    with pytest.raises(TypeError):
        list(BaseTransform._text_batches(texts, 2))


def test_batches_consume_generators_incrementally():
    consumed = []

    def source():
        for i in range(5):
            consumed.append(i)
            yield str(i)

    batches = BaseTransform._text_batches(source(), 2)
    assert next(batches) == ["0", "1"]
    assert consumed == [0, 1]
    assert list(batches) == [["2", "3"], ["4"]]


def test_encoded_batches_preserve_chunk_ownership_and_padding():
    documents = [
        {
            "input_ids": np.array([[1, 2], [3, 4]]),
            "attention_mask": np.ones((2, 2), dtype=np.int64),
        },
        {
            "input_ids": np.array([[5, 6, 7]]),
            "attention_mask": np.ones((1, 3), dtype=np.int64),
        },
    ]
    batches = list(AlbertTokenizer._encoded_batches(documents, 3, pad_token_id=99))
    feed, owners = batches[0]
    assert owners == [(0, 0, 2), (0, 1, 2), (1, 0, 3)]
    assert feed["input_ids"].tolist() == [[1, 2, 99], [3, 4, 99], [5, 6, 7]]
    assert feed["attention_mask"].tolist() == [[1, 1, 0], [1, 1, 0], [1, 1, 1]]
    assert [
        len(rows) for _, rows in AlbertTokenizer._encoded_batches(documents, 2)
    ] == [2, 1]


def test_fixed_batch_one_model_warns_and_limits_execution():
    session = SimpleNamespace(
        get_inputs=lambda: [SimpleNamespace(name="input_ids", shape=[1, "length"])]
    )
    with pytest.warns(RuntimeWarning, match="fixed batch size"):
        assert BaseTransform._session_batch_size(session, 32) == 1


class RecordingBatchTransform(BaseTransform):
    supports_batching = True

    def __init__(self, batch_size=2):
        self.batch_size = batch_size
        self.calls = []

    def transform(self, text):
        if not isinstance(text, str):
            return self.transform_batch(text)
        return text.upper()

    def _transform_batch(self, texts, batch_size):
        self.calls.append(list(texts))
        return [text.upper() for text in texts]


@pytest.mark.parametrize("method", ["__call__", "transform", "transform_batch"])
def test_pipeline_reaches_batch_model_and_preserves_order(method):
    model = RecordingBatchTransform()
    pipeline = PunctuationRemover() | model
    result = list(getattr(pipeline, method)(iter(["a!", "b!", "c!"])))
    assert result == ["A", "B", "C"]
    assert model.calls == [["a", "b"], ["c"]]
    assert pipeline("a!") == "A"


def test_batch_override_does_not_mutate_configuration():
    model = RecordingBatchTransform(2)
    assert model.transform_batch(["a", "b", "c"], batch_size=1) == ["A", "B", "C"]
    assert model.batch_size == 2
    assert model.calls == [["a"], ["b"], ["c"]]


def test_pipeline_preserves_custom_fit_transform_semantics():
    class Stateful(BaseTransform):
        def fit(self, X, y=None):
            self.seen = X
            self.target = y
            return self

        def transform(self, X):
            assert X == self.seen
            return X + "!"

    step = Stateful()
    result = list(Pipeline([step]).fit_transform(["a", "b"], y="target"))
    assert result == ["a!", "b!"]
    assert step.target == "target"


def test_embedding_pooling_never_merges_documents_and_bounds_chunks():
    model = AlbertEmbedder.__new__(AlbertEmbedder)
    model.batch_size = 2
    model.vector_size = 2

    def tokenize(text):
        # Three chunks for one document, with a masked token in the last chunk.
        ids = (
            np.array([[1, 3], [5, 7], [9, 0]])
            if text == "long"
            else np.array([[20, 30]])
        )
        return {"input_ids": ids, "attention_mask": (ids != 0).astype(np.int64)}

    class Tokenizer:
        pad_token_id = 0

        def __call__(self, text):
            return tokenize(text)

    model.tokenizer = Tokenizer()
    calls = []

    def run(names, inputs):
        assert names == ["last_hidden_state"]
        calls.append(len(inputs["input_ids"]))
        return [
            np.repeat(inputs["input_ids"][:, :, None], 2, axis=2).astype(np.float32)
        ]

    model.session = SimpleNamespace(
        get_inputs=lambda: [
            SimpleNamespace(name=n, shape=["batch", "length"])
            for n in ["input_ids", "attention_mask"]
        ],
        run=run,
    )
    np.testing.assert_array_equal(
        model.embed(iter(["long", "short"])), [[5, 5], [25, 25]]
    )
    assert calls == [2, 2]
    assert model.embed([]).shape == (0, 2)
    assert model.embed("short").shape == (2,)


def test_pipeline_composition_preserves_explicit_batch_size():
    model = RecordingBatchTransform(8)
    pipeline = Pipeline([model], batch_size=2) | PunctuationRemover()
    assert pipeline.batch_size == 2
    assert list(pipeline(["a!", "b!", "c!"])) == ["A", "B", "C"]
    assert model.calls == [["a!", "b!"], ["c!"]]
    assert (PunctuationRemover() | pipeline).batch_size == 2


def test_pipeline_adopts_model_batch_size():
    pipeline = PunctuationRemover() | RecordingBatchTransform(64)
    assert pipeline.batch_size == 64


@pytest.mark.parametrize(
    "name",
    [
        "NER",
        "POSTagger",
        "SentimentClassifier",
        "OffensiveLanguageClassifier",
        "ContextualEmbedder",
        "DependencyParser",
        "FarsiToTajik",
        "TajikToFarsi",
    ],
)
def test_public_constructors_reject_invalid_batch_size_before_loading(
    name, monkeypatch
):
    import shekar
    from shekar.hub import Hub

    def no_download(*args, **kwargs):
        pytest.fail("Invalid configuration must fail before fetching a model")

    monkeypatch.setattr(Hub, "get_resource", no_download)
    with pytest.raises(ValueError, match="batch_size"):
        getattr(shekar, name)(batch_size=0)


def test_dependency_parser_rejects_out_of_range_word_alignment():
    from shekar.dep_parsing.albert_dep_parser import AlbertDepParser

    parser = AlbertDepParser.__new__(AlbertDepParser)
    parser.tokenizer = SimpleNamespace(
        model_max_length=4,
        cls_token_id=0,
        sep_token_id=0,
        pad_token_id=0,
        sp=SimpleNamespace(encode=lambda word, out_type: [1]),
    )
    with pytest.raises(ValueError, match="shorter sentences"):
        parser._build_inputs(["a", "b", "c"])


def test_pos_splits_only_at_word_boundaries():
    from shekar.pos.albert_pos import AlbertPOS

    model = AlbertPOS.__new__(AlbertPOS)
    model.tokenizer = SimpleNamespace(
        model_max_length=4,
        unk_token_id=0,
        sp=SimpleNamespace(encode=lambda word, out_type: list(range(len(word)))),
    )
    assert model._encode_words(["ab", "cde", "f"]) == [
        ([0, 1], [(0, 0)]),
        ([0, 1, 2, 0], [(1, 0), (2, 3)]),
    ]
    with pytest.raises(ValueError, match="single word"):
        model._encode_words(["abcde"])


def test_pipeline_transform_preserves_custom_non_text_batch_contract():
    class Sum(BaseTransform):
        def transform(self, X):
            return sum(X)

    assert Pipeline([Sum()]).transform([1, 2, 3]) == 6


def test_pipeline_fit_transform_preserves_custom_subclass_override():
    class CustomPipeline(Pipeline):
        def fit_transform(self, X, y=None):
            return X + "!"

    pipeline = Pipeline([CustomPipeline([])])
    assert list(pipeline(["a", "b"])) == ["a!", "b!"]


def test_dynamic_padding_removes_only_trailing_masked_positions():
    documents = [
        {
            "input_ids": np.array([[1, 99, 2, 99, 99]]),
            "attention_mask": np.array([[1, 0, 1, 0, 0]]),
        }
    ]
    feed, _ = next(
        AlbertTokenizer._encoded_batches(
            documents, 2, pad_token_id=99, trim_padding=True
        )
    )
    assert feed["input_ids"].tolist() == [[1, 99, 2]]
    assert feed["attention_mask"].tolist() == [[1, 0, 1]]
    original, _ = next(AlbertTokenizer._encoded_batches(documents, 2))
    assert original["input_ids"].shape == (1, 5)


@pytest.mark.parametrize("tf32", [None, "0", "1"])
def test_cuda_session_uses_fp32_options_and_preserves_provider_order(monkeypatch, tf32):
    import importlib.metadata

    from shekar import utils

    monkeypatch.delenv("SHEKAR_USE_TF32", raising=False)
    if tf32 is not None:
        monkeypatch.setenv("SHEKAR_USE_TF32", tf32)
    monkeypatch.setattr(
        utils,
        "get_onnx_providers",
        lambda: ["CUDAExecutionProvider", "CPUExecutionProvider"],
    )
    monkeypatch.setattr(importlib.metadata, "version", lambda package: "9.0")
    preloads = []
    monkeypatch.setattr(utils.ort, "preload_dlls", lambda **kw: preloads.append(kw))
    calls = []
    monkeypatch.setattr(
        utils.ort, "InferenceSession", lambda *args, **kw: calls.append((args, kw))
    )
    utils.create_onnx_session("model.onnx")
    assert calls[0][1]["providers"] == ["CUDAExecutionProvider", "CPUExecutionProvider"]
    assert calls[0][1]["provider_options"] == [{"use_tf32": tf32 or "0"}, {}]
    assert preloads == [{"cuda": False, "cudnn": True}]


@pytest.mark.parametrize("batch_size", [1, 2, 3])
def test_ner_preserves_document_boundaries_and_removes_overlap(batch_size):
    from shekar.ner.albert_ner import AlbertNER

    model = AlbertNER.__new__(AlbertNER)
    model.batch_size = batch_size
    model.id2tag = {0: "O", 1: "B-PER", 2: "I-PER", 3: "B-LOC"}

    class Tokenizer:
        pad_token_id, cls_token_id, sep_token_id, stride = 0, 90, 91, 1
        unk_token_id = 99

        def __call__(self, text):
            ids = (
                np.array([[90, 1, 2, 91], [90, 2, 3, 91]])
                if text == "first"
                else np.array([[90, 4, 5, 91]])
            )
            return {"input_ids": ids, "attention_mask": np.ones_like(ids)}

        def id_to_token(self, token):
            return {1: "▁علی", 2: "▁رضا", 3: "▁امیری", 4: "▁نام", 5: "▁تهران"}[token]

    model.tokenizer = Tokenizer()
    calls = []

    def run(names, feed):
        ids = feed["input_ids"]
        calls.append(len(ids))
        logits = np.zeros((*ids.shape, 4))
        for row in range(len(ids)):
            for position, token in enumerate(ids[row]):
                tag = {1: 1, 2: 2, 3: 2, 4: 2, 5: 3}.get(token, 0)
                logits[row, position, tag] = 1
        return [logits]

    model.session = SimpleNamespace(
        get_inputs=lambda: [
            SimpleNamespace(name=n, shape=["batch", "length"])
            for n in ["input_ids", "attention_mask"]
        ],
        run=run,
    )
    assert model(["first", "second"]) == [
        [("علی رضا امیری", "PER")],
        [("تهران", "LOC")],
    ]
    assert max(calls) <= batch_size


def test_session_constraints_cached_but_batch_override_remains_dynamic():
    calls = []
    session = SimpleNamespace(
        get_inputs=lambda: (
            calls.append(1)
            or [
                SimpleNamespace(name="auxiliary", shape=[8]),
                SimpleNamespace(name="input_ids", shape=["batch", "length"]),
            ]
        )
    )
    assert BaseTransform._session_batch_size(session, 2) == 2
    assert BaseTransform._session_batch_size(session, 8) == 8
    assert calls == [1]


def test_fixed_batch_warning_emitted_once():
    import warnings

    session = SimpleNamespace(
        get_inputs=lambda: [SimpleNamespace(name="input_ids", shape=[1, "length"])]
    )
    assert BaseTransform._session_batch_size(session, 1) == 1
    with pytest.warns(RuntimeWarning):
        assert BaseTransform._session_batch_size(session, 8) == 1
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert BaseTransform._session_batch_size(session, 2) == 1
    assert not caught


def test_pos_rejects_unsupported_batch_dimension_at_construction(monkeypatch, tmp_path):
    from shekar.pos import albert_pos

    path = tmp_path / "model.onnx"
    path.touch()
    session = SimpleNamespace(
        get_inputs=lambda: [
            SimpleNamespace(name="input_ids", shape=[1, "length"]),
            SimpleNamespace(name="attention_mask", shape=[8, "length"]),
        ]
    )
    monkeypatch.setattr(albert_pos, "create_onnx_session", lambda path: session)
    with pytest.raises(ValueError, match="fixed batch of 1"):
        albert_pos.AlbertPOS(path)


def test_transliterator_private_empty_batch_needs_no_models():
    from shekar.transliteration.byt5_transliterator import ByT5Transliterator

    model = ByT5Transliterator.__new__(ByT5Transliterator)
    assert model._transform_batch([], 2) == []


def test_invalid_tf32_setting_fails_before_session_creation(monkeypatch):
    from shekar import utils

    monkeypatch.setenv("SHEKAR_USE_TF32", "yes")
    with pytest.raises(ValueError, match="SHEKAR_USE_TF32 must be 0 or 1"):
        utils.create_onnx_session("missing.onnx")
