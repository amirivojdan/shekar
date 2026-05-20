import pytest

from shekar.data import ZWNJ
from shekar.transforms.noise.whitespace import WhitespaceNoise


@pytest.fixture
def noise():
    return WhitespaceNoise(seed=42)


def test_invalid_zwnj_deletion_prob():
    with pytest.raises(ValueError):
        WhitespaceNoise(zwnj_deletion_prob=1.5)


def test_invalid_zwnj_to_space_prob():
    with pytest.raises(ValueError):
        WhitespaceNoise(zwnj_to_space_prob=2.0)


def test_invalid_space_deletion_prob():
    with pytest.raises(ValueError):
        WhitespaceNoise(space_deletion_prob=-0.1)


def test_invalid_space_to_zwnj_prob():
    with pytest.raises(ValueError):
        WhitespaceNoise(space_to_zwnj_prob=1.5)


def test_zero_probabilities_is_identity():
    n = WhitespaceNoise(
        zwnj_deletion_prob=0,
        zwnj_to_space_prob=0,
        space_deletion_prob=0,
        space_to_zwnj_prob=0,
        seed=0,
    )
    text = "می‌رود و می‌آید"
    assert n(text) == text


def test_deterministic_with_seed():
    text = "می‌رود و نمی‌آید"
    assert WhitespaceNoise(seed=42)(text) == WhitespaceNoise(seed=42)(text)


def test_output_is_string(noise):
    assert isinstance(noise("می‌رود"), str)


# --- ZWNJ perturbations ---


def test_zwnj_deletion_removes_zwnj():
    n = WhitespaceNoise(zwnj_deletion_prob=1.0, zwnj_to_space_prob=0, seed=0)
    assert n(f"می{ZWNJ}رود") == "میرود"


def test_zwnj_deletion_removes_all_zwnjS():
    n = WhitespaceNoise(zwnj_deletion_prob=1.0, zwnj_to_space_prob=0, seed=0)
    text = f"می{ZWNJ}رود و نمی{ZWNJ}آید"
    assert ZWNJ not in n(text)


def test_zwnj_to_space_replaces_zwnj():
    n = WhitespaceNoise(zwnj_deletion_prob=0, zwnj_to_space_prob=1.0, seed=0)
    result = n(f"می{ZWNJ}رود")
    assert ZWNJ not in result
    assert result == "می رود"


def test_zwnj_deletion_takes_priority_over_space_sub():
    n = WhitespaceNoise(zwnj_deletion_prob=1.0, zwnj_to_space_prob=1.0, seed=0)
    assert n(f"می{ZWNJ}رود") == "میرود"


# --- Space perturbations ---


def test_space_deletion_removes_spaces():
    n = WhitespaceNoise(space_deletion_prob=1.0, space_to_zwnj_prob=0, seed=0)
    assert n("می رود") == "میرود"


def test_space_deletion_removes_all_spaces():
    n = WhitespaceNoise(space_deletion_prob=1.0, space_to_zwnj_prob=0, seed=0)
    text = "می رود و نمی آید"
    assert " " not in n(text)


def test_space_to_zwnj_replaces_space():
    n = WhitespaceNoise(space_deletion_prob=0, space_to_zwnj_prob=1.0, seed=0)
    result = n("می رود")
    assert " " not in result
    assert ZWNJ in result


def test_space_deletion_takes_priority_over_zwnj_sub():
    n = WhitespaceNoise(space_deletion_prob=1.0, space_to_zwnj_prob=1.0, seed=0)
    assert n("می رود") == "میرود"


# --- Pass-through ---


def test_non_whitespace_chars_pass_through_unchanged():
    n = WhitespaceNoise(
        zwnj_deletion_prob=1.0,
        zwnj_to_space_prob=1.0,
        space_deletion_prob=1.0,
        space_to_zwnj_prob=1.0,
        seed=0,
    )
    result = n("سلاماbc123")
    assert result == "سلاماbc123"


def test_output_under_heavy_noise():
    n = WhitespaceNoise(
        zwnj_deletion_prob=0.5,
        zwnj_to_space_prob=0.3,
        space_deletion_prob=0.2,
        space_to_zwnj_prob=0.2,
        seed=7,
    )
    assert isinstance(n("می‌رود و نمی‌آید"), str)
