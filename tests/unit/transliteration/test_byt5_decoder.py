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
