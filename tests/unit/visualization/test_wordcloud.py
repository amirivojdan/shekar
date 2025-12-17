import pytest

pytest.importorskip("wordcloud")
pytest.importorskip("matplotlib")
pytest.importorskip("arabic_reshaper")
pytest.importorskip("bidi")
pytest.importorskip("PIL")

from shekar.visualization import WordCloud
from PIL import Image
from collections import Counter
import numpy as np
import os
from importlib import resources
from shekar import data


@pytest.fixture
def wordcloud_instance():
    return WordCloud()


def test_wordcloud_default_initialization(wordcloud_instance):
    assert wordcloud_instance.wc is not None
    assert wordcloud_instance.mask is None


def test_wordcloud_custom_mask():
    mask_path = resources.files(data).joinpath("masks") / "iran.png"
    if not os.path.exists(mask_path):
        pytest.skip("Custom mask file does not exist.")
    wc_instance = WordCloud(mask=str(mask_path))
    assert wc_instance.mask is not None
    assert isinstance(wc_instance.mask, np.ndarray)


def test_wordcloud_invalid_mask():
    with pytest.raises(FileNotFoundError):
        WordCloud(mask="invalid_path.png")


def test_wordcloud_generate_valid_frequencies(wordcloud_instance):
    frequencies = Counter({"ایران": 10, "خاک": 5, "دلیران": 15})
    image = wordcloud_instance.generate(frequencies)
    assert isinstance(image, Image.Image)


def test_wordcloud_generate_invalid_frequencies(wordcloud_instance):
    with pytest.raises(ValueError):
        wordcloud_instance.generate({"word1": "invalid_frequency"})


def test_wordcloud_generate_empty_frequencies(wordcloud_instance):
    frequencies = Counter()
    with pytest.raises(ValueError):
        wordcloud_instance.generate(frequencies)


def test_wordcloud_font_path():
    wc_instance = WordCloud(font="parastoo")
    assert "parastoo.ttf" in str(wc_instance.wc.font_path)


def test_wordcloud_invalid_font_path():
    with pytest.raises(FileNotFoundError):
        WordCloud(font="invalid_font.ttf")


def test_wordcloud_invalid_color_map():
    wc_instance = WordCloud(color_map="invalid_colormap")
    assert wc_instance.wc.colormap == "Set3"
