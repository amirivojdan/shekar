"""Real model parity tests. Set SHEKAR_BATCH_INTEGRATION=cpu or cuda to run.

Uses only existing ~/.shekar resources. CUDA runs assert the CUDA EP initialized;
unit tests in test_batching_contract.py cover boundaries without model downloads.
"""

import os
from pathlib import Path

import numpy as np
import onnxruntime as ort
import pytest

from shekar import (
    NER,
    ContextualEmbedder,
    DependencyParser,
    FarsiToTajik,
    OffensiveLanguageClassifier,
    POSTagger,
    SentimentClassifier,
    TajikToFarsi,
)

MODE = os.environ.get("SHEKAR_BATCH_INTEGRATION")
pytestmark = pytest.mark.skipif(
    MODE not in ("cpu", "cuda"), reason="Opt-in real-model batch tests"
)
CLASSES = [
    ContextualEmbedder,
    DependencyParser,
    NER,
    POSTagger,
    SentimentClassifier,
    OffensiveLanguageClassifier,
    FarsiToTajik,
    TajikToFarsi,
]


class CountingSession:
    def __init__(self, session):
        self.session = session
        self.rows = []

    def __getattr__(self, name):
        return getattr(self.session, name)

    def run(self, names, feed):
        name = "input_ids" if "input_ids" in feed else "input_text"
        self.rows.append(len(feed[name]))
        return self.session.run(names, feed)


@pytest.fixture(scope="module", params=CLASSES, ids=lambda cls: cls.__name__)
def model(request):
    from shekar.hub import Hub

    patcher = pytest.MonkeyPatch()
    original_session = ort.InferenceSession

    def make_session(*args, **kwargs):
        opts = kwargs.get("sess_options") or ort.SessionOptions()
        opts.intra_op_num_threads = 1
        kwargs["sess_options"] = opts
        kwargs["provider_options"] = [{"use_tf32": "0"}, {}] if MODE == "cuda" else [{}]
        kwargs["providers"] = (
            ["CUDAExecutionProvider", "CPUExecutionProvider"]
            if MODE == "cuda"
            else ["CPUExecutionProvider"]
        )
        session = original_session(*args, **kwargs)
        if MODE == "cuda":
            assert "CUDAExecutionProvider" in session.get_providers()
        return session

    def resource(file_name):
        path = Path.home() / ".shekar" / file_name
        if not path.is_file():
            pytest.skip(f"Missing cached model: {file_name}")
        return path

    patcher.setattr(ort, "InferenceSession", make_session)
    patcher.setattr(Hub, "get_resource", staticmethod(resource))
    instance = request.param(batch_size=2)
    if isinstance(instance, (FarsiToTajik, TajikToFarsi)):
        instance.max_new_tokens = 24
        instance.encoder._session = CountingSession(instance.encoder._session)
        instance.decoder._session = CountingSession(instance.decoder._session)
        counter = instance.decoder._session
    else:
        core = (
            instance.embedder
            if isinstance(instance, ContextualEmbedder)
            else instance.model
        )
        core.session = CountingSession(core.session)
        counter = core.session
    yield instance, counter
    patcher.undo()


def compare(model, actual, expected):
    if isinstance(model, ContextualEmbedder):
        np.testing.assert_allclose(actual, expected, atol=1e-4, rtol=1e-4)
    elif isinstance(model, (SentimentClassifier, OffensiveLanguageClassifier)):
        assert [r[0] for r in actual] == [r[0] for r in expected]
        np.testing.assert_allclose(
            [r[1] for r in actual], [r[1] for r in expected], atol=0.03, rtol=0.03
        )
    else:
        assert actual == expected


@pytest.mark.parametrize("batch_size", [1, 2, 3])
def test_batch_matches_single_documents(model, batch_size):
    instance, counter = model
    texts = ["سلام تهران", "من به خانه رفتم.", "", "کتاب کتاب کتاب", "سلام تهران"]
    if isinstance(instance, TajikToFarsi):
        texts = ["Салом", "Эрон модар аст!", "", "китоб", "Салом"]
    expected = [instance(text) for text in texts]
    counter.rows.clear()
    actual = instance.transform_batch(iter(texts), batch_size=batch_size)
    compare(instance, actual, expected)
    assert max(counter.rows) <= batch_size
    if batch_size > 1:
        assert max(counter.rows) > 1
    assert instance.batch_size == 2


def test_automatic_batch_and_empty_input(model):
    instance, _ = model
    texts = ["سلام", "کتاب"]
    compare(instance, list(instance(iter(texts))), [instance(text) for text in texts])
    empty = instance([])
    if isinstance(instance, ContextualEmbedder):
        assert empty.shape == (0, 768)
    else:
        assert list(empty) == []


def test_long_chunked_documents(model):
    instance, counter = model
    if not isinstance(instance, (ContextualEmbedder, NER, POSTagger)):
        pytest.skip("Model does not use overflow chunks")
    texts = ["کتاب " * 600, "تهران"]
    expected = [instance(text) for text in texts]
    counter.rows.clear()
    actual = instance(texts)
    compare(instance, actual, expected)
    assert max(counter.rows) <= instance.batch_size
    if isinstance(instance, POSTagger):
        assert len(actual[0]) == 600


def test_real_beam_search_batch(model):
    instance, counter = model
    if not isinstance(instance, (FarsiToTajik, TajikToFarsi)):
        pytest.skip("Beam search applies only to transliteration")
    original = instance.num_beams
    instance.num_beams = 2
    try:
        texts = (
            ["ایران", "سلام"]
            if isinstance(instance, FarsiToTajik)
            else ["Эрон", "Салом"]
        )
        expected = [instance(text) for text in texts]
        counter.rows.clear()
        assert instance.transform_batch(texts) == expected
        assert max(counter.rows) == 4
    finally:
        instance.num_beams = original
