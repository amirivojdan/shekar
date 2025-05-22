import arabic_reshaper
import matplotlib
from wordcloud import WordCloud as wc
from bidi import get_display
from PIL import Image
import numpy as np
from typing import Counter
from shekar import utils
import os


class WordCloud:
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
        masks_path = utils.data_root_path / "masks"
        if font == "parastoo" or font == "sahel":
            font_path = utils.data_root_path / "fonts" / f"{font}.ttf"
        elif os.path.exists(font):
            font_path = font
        else:
            raise FileNotFoundError(
                f"Font file {font} not found. Please provide a valid font path."
            )
        
        if isinstance(mask, str):
            if mask == "Iran":
                self.mask = np.array(Image.open(masks_path / "iran.png"))
            elif mask == "Head":
                self.mask = np.array(Image.open(masks_path / "head.png"))
            elif mask == "Heart":
                self.mask = np.array(Image.open(masks_path / "heart.png"))
            elif mask == "Bulb":
                self.mask = np.array(Image.open(masks_path / "bulb.png"))
            elif mask == "Cat":
                self.mask = np.array(Image.open(masks_path / "cat.png"))
            elif mask == "Cloud":
                self.mask = np.array(Image.open(masks_path / "cloud.png"))
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

    def generate(self, frequencies: Counter) -> Image:
        """
        Generate a word cloud from a dictionary of words and their frequencies.
        """
        if not isinstance(frequencies, Counter):
            raise ValueError(
                "Input must be a dictionary of words and their frequencies."
            )
        
        if not frequencies:
            raise ValueError("Frequencies dictionary is empty.")
        

        frequencies = {
            get_display(arabic_reshaper.reshape(k)): float(v)
            for k, v in frequencies.items()
            if v > 0
        }

        wordcloud = self.wc.generate_from_frequencies(frequencies)
        image = wordcloud.to_image()
        return image
