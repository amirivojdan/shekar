import arabic_reshaper
import matplotlib
from wordcloud import WordCloud as wc
from bidi import get_display
from PIL import Image
import numpy as np
from typing import Counter
import os
from shekar import data
from importlib import resources


class WordCloud:
    """
    A class to generate word clouds from Persian text using the WordCloud library.
    This class provides functionality to create visually appealing word clouds
    with various customization options such as font, color map, and mask.
    """

    def __init__(
        self,
        mask: str | None = None,
        width: int = 1000,
        height: int = 500,
        color_map: str | None = "viridis",
        bg_color: str = "black",
        contour_width: int = 5,
        contour_color: str = "white",
        font: str = "sahel",
        min_font_size: int = 6,
        max_font_size: int = 80,
        horizontal_ratio: float = 0.75,
    ):
        self.predefined_masks = {
            "Iran": "iran.png",
            "Head": "head.png",
            "Heart": "heart.png",
            "Bulb": "bulb.png",
            "Cat": "cat.png",
            "Cloud": "cloud.png",
        }

        if font == "parastoo" or font == "sahel":
            font_path = resources.files(data).joinpath("fonts") / f"{font}.ttf"
        elif os.path.exists(font):
            font_path = font
        else:
            raise FileNotFoundError(
                f"Font file {font} not found. Please provide a valid font path."
            )

        if isinstance(mask, str):
            if mask in self.predefined_masks:
                mask_path = (
                    resources.files(data).joinpath("masks")
                    / self.predefined_masks[mask]
                )
                self.mask = np.array(Image.open(mask_path))
            elif os.path.exists(mask):
                self.mask = np.array(Image.open(mask))
            else:
                raise FileNotFoundError(
                    f"Mask file {mask} not found. Please provide a valid mask path."
                )
        else:
            self.mask = None

        if not color_map or color_map not in list(matplotlib.colormaps):
            color_map = "Set3"

        self.wc = wc(
            width=width,
            height=height,
            background_color=bg_color,
            contour_width=contour_width,
            contour_color=contour_color,
            min_font_size=min_font_size,
            max_font_size=max_font_size,
            mask=self.mask,
            font_path=font_path,
            prefer_horizontal=horizontal_ratio,
            colormap=color_map,
        )

    def generate(self, frequencies: Counter, bidi_reshape: bool = True) -> Image:
        """
        Generates a word cloud image from the given frequencies.
        Args:
            frequencies (Counter): A dictionary of words and their frequencies.
            bidi_reshape (bool): Whether to apply bidirectional reshaping for Persian text.
        Returns:
            Image: The generated word cloud PIL image.
        """
        if not isinstance(frequencies, Counter):
            raise ValueError(
                "Input must be a dictionary of words and their frequencies."
            )

        if not frequencies:
            raise ValueError("Frequencies dictionary is empty.")

        reshaped_frequencies = {
            (get_display(arabic_reshaper.reshape(k)) if bidi_reshape else k): float(v)
            for k, v in frequencies.items()
            if v > 0
        }

        wordcloud = self.wc.generate_from_frequencies(reshaped_frequencies)
        image = wordcloud.to_image()
        return image
