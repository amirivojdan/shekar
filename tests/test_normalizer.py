import pytest
from shekar.normalizer import Normalizer


@pytest.fixture
def normalizer():
    return Normalizer()


def test_normalize(normalizer):
    input_text = "ناصر گفت:«من میروم.» \u200c 🎉🎉🎊🎈she+kar@she-kar.io"
    expected_output = "ناصر گفت: «من می‌روم.»"
    assert normalizer.normalize(input_text) == expected_output
