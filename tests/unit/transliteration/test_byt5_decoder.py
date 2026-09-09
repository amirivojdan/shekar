from types import SimpleNamespace

import numpy as np
import pytest

from shekar.transliteration.byt5_decoder import ByT5Decoder
from shekar.transliteration.byt5_transliterator import ByT5Transliterator


class BeamSearchSession:
    def __init__(self):
        self.input_history = []

    def run(self, _, feed):
        input_ids = feed["input_ids"][:, 0]
        self.input_history.append(input_ids.copy())
        logits = np.full((len(input_ids), 1, 5), -20.0, dtype=np.float32)

        if len(self.input_history) == 1:
            logits[0, 0, 2] = 5.0
            logits[0, 0, 3] = 4.0
            logits[0, 0, 1] = -10.0
            return [logits]

        for row, token_id in enumerate(input_ids):
            if token_id == 2:
                logits[row, 0, 1] = 0.0
                logits[row, 0, 4] = -0.2
            elif token_id == 3:
                logits[row, 0, 4] = 0.0
                logits[row, 0, 2] = -0.1
                logits[row, 0, 1] = -10.0
            elif token_id == 4:
                logits[row, 0, 1] = 10.0

        return [logits]


def make_decoder() -> ByT5Decoder:
    decoder = ByT5Decoder.__new__(ByT5Decoder)
    decoder._session = BeamSearchSession()
    decoder._tokenizer = SimpleNamespace(_pad_id=0, _eos_id=1)
    decoder._past_self_k = []
    decoder._past_self_v = []
    decoder._past_cross_k = []
    decoder._past_cross_v = []
    decoder._present_self_k = []
    decoder._present_self_v = []
    decoder._present_cross_k = []
    decoder._present_cross_v = []
    decoder._output_names = ["logits"]
    decoder._has_use_cache_branch = False
    decoder._num_layers = 0
    decoder._num_heads = 1
    decoder._d_kv = 1
    return decoder


@pytest.mark.parametrize(
    ("num_beams", "max_new_tokens"),
    [(0, 1), (-1, 1), (True, 1), (1.5, 1), (1, 0), (1, False), (1, 2.5)],
)
def test_decode_validates_generation_parameters(num_beams, max_new_tokens):
    decoder = make_decoder()
    with pytest.raises(ValueError):
        decoder.decode(
            np.zeros((1, 1, 1), dtype=np.float32),
            np.ones((1, 1), dtype=np.int64),
            num_beams=num_beams,
            max_new_tokens=max_new_tokens,
        )


def test_transliterator_validates_before_loading_models():
    with pytest.raises(ValueError, match="num_beams"):
        ByT5Transliterator(num_beams=0)


def test_beam_search_keeps_finished_and_active_scores_separate():
    decoder = make_decoder()

    result = decoder.decode(
        np.zeros((1, 1, 1), dtype=np.float32),
        np.ones((1, 1), dtype=np.int64),
        num_beams=2,
        max_new_tokens=3,
    )

    assert result == [2, 4]
    assert all(
        decoder._tokenizer._eos_id not in input_ids
        for input_ids in decoder._session.input_history[1:]
    )


class MultiDocumentSession:
    """Expose cache/beam mixups through distinct per-document cache values."""

    def __init__(self):
        self.batch_sizes = []

    def run(self, _, feed):
        ids = feed["input_ids"][:, 0]
        documents = feed["encoder_hidden_states"][:, 0, 0]
        self.batch_sizes.append(len(ids))
        past = feed["past_key_values.0.decoder.key"]
        if past.shape[2]:
            np.testing.assert_array_equal(past[:, 0, 0, 0], documents)
            np.testing.assert_array_equal(
                feed["past_key_values.0.encoder.key"][:, 0, 0, 0], documents
            )
        logits = np.full((len(ids), 1, 5), -30.0, dtype=np.float32)
        for row, (token, document) in enumerate(zip(ids, documents)):
            next_token = (
                (2 if document == 10 else 3) if token == 0 else (4 if token == 3 else 1)
            )
            logits[row, 0, next_token] = 10.0
        self_cache = np.broadcast_to(
            documents[:, None, None, None], (len(ids), 1, past.shape[2] + 1, 1)
        ).copy()
        cross_cache = documents[:, None, None, None].copy()
        return [logits, self_cache, cross_cache]


def make_multi_document_decoder():
    decoder = make_decoder()
    decoder._session = MultiDocumentSession()
    decoder._past_self_k = ["past_key_values.0.decoder.key"]
    decoder._past_cross_k = ["past_key_values.0.encoder.key"]
    decoder._present_self_k = ["present.0.decoder.key"]
    decoder._present_cross_k = ["present.0.encoder.key"]
    decoder._output_names = ["logits", "present.0.decoder.key", "present.0.encoder.key"]
    # Reuse the same named cache for values; this fake model only needs one per kind.
    decoder._past_self_v = decoder._past_self_k
    decoder._past_cross_v = decoder._past_cross_k
    decoder._present_self_v = decoder._present_self_k
    decoder._present_cross_v = decoder._present_cross_k
    decoder._num_layers = 1
    return decoder


@pytest.mark.parametrize("num_beams", [1, 2])
def test_decode_batch_keeps_beams_caches_and_early_stopping_per_document(num_beams):
    states = np.array([[[10.0]], [[20.0]]], dtype=np.float32)
    masks = np.ones((2, 1), dtype=np.int64)
    expected = [
        make_multi_document_decoder().decode(
            states[i : i + 1], masks[i : i + 1], num_beams, 4
        )
        for i in range(2)
    ]
    decoder = make_multi_document_decoder()
    actual = decoder.decode_batch(states, masks, num_beams, 4)
    assert actual == expected == [[2], [3, 4]]
    assert max(decoder._session.batch_sizes) == 2 * num_beams
    assert decoder._session.batch_sizes[-1] == num_beams
