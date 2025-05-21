import arabic_reshaper
from wordcloud import WordCloud as wc
from bidi import get_display
from PIL import Image
import numpy as np
from typing import Counter
from shekar import utils


class WordCloud:
    def __init__(
        self,
        mask: str | None = None,
        width=1000,
        height=500,
        bg_color="black",
        contour_width=5,
        contour_color="white",
        font="sahel",
        min_font_size=12,
        max_font_size=84,
        horizontal_ratio=0.75,
    ):
        masks_path = utils.data_root_path / "masks"
        if font != "parastoo" and font != "sahel":
            font = "sahel"
        font_path = utils.data_root_path / "fonts" / f"{font}.ttf"
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
            else:
                self.mask = None
        else:
            self.mask = mask

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
        )

    def generate(self, frequencies: Counter) -> Image:
        """
        Generate a word cloud from a dictionary of words and their frequencies.
        """
        if not isinstance(frequencies, Counter):
            raise ValueError(
                "Input must be a dictionary of words and their frequencies."
            )

        # Filter out words with zero frequency
        frequencies = {
            get_display(arabic_reshaper.reshape(k)): float(v)
            for k, v in frequencies.items()
            if v > 0
        }

        # Generate the word cloud
        wordcloud = self.wc.generate_from_frequencies(frequencies)
        image = wordcloud.to_image()
        return image


if __name__ == "__main__":
    # Example usage
    text = """هیچ جای دنیا تر و خشک را مثل ایران با هم نمی‌سوزانند. پس از پنج سال در به دری و خون جگری هنوز چشمم از بالای صفحهٔ کشتی به خاک پاک ایران نیفتاده بود که آواز گیلکی کرجی‌بان‌های انزلی به گوشم رسید که «بالام جان، بالام جان» خوانان مثل مورچه‌هایی که دور ملخ مرده‌ای را بگیرند دور کشتی را گرفته و بلای جان مسافرین شدند و ریش هر مسافری به چنگ چند پاروزن و کرجی بان و حمال افتاد. ولی میان مسافرین کار من دیگر از همه زارتر بود چون سایرین عموما کاسب‌کارهای لباده دراز و کلاه کوتاه باکو و رشت بودند که به زور چماق و واحد یموت هم بند کیسه‌شان باز نمی‌شود و جان به عزرائیل می‌دهند و رنگ پولشان را کسی نمی‌بیند. ولی من بخت برگشتهٔ مادر مرده مجال نشده بود کلاه لگنی فرنگیم را که از همان فرنگستان سرم مانده بود عوض کنم و یاروها ما را پسر حاجی و لقمهٔ چربی فرض کرده و «صاحب، صاحب» گویان دورمان کردند و هر تکه از اسباب‌هایمان مایه‌النزاع ده راس حمال و پانزده نفر کرجی‌بان بی‌انصاف شد و جیغ و داد و فریادی بلند و قشقره‌ای برپا گردید که آن سرش پیدا نبود. ما مات و متحیر و انگشت به دهن سرگردان مانده بودیم که به چه بامبولی یخه‌مان را از چنگ این ایلغاریان خلاص کنیم و به چه حقه و لمی از گیرشان بجهیم که صف شکافته شد و عنق منکسر و منحوس دو نفر از ماموران تذکره که انگاری خود انکر و منکر بودند با چند نفر فراش سرخ پوش و شیر و خورشید به کلاه با صورت‌هایی اخمو و عبوس و سبیل‌های چخماقی از بناگوش دررفته‌ای که مانند بیرق جوع و گرسنگی، نسیم دریا به حرکتشان آورده بود در مقابل ما مانند آینهٔ دق حاضر گردیدند و همین که چشمشان به تذکرهٔ ما افتاد مثل این‌که خبر تیر خوردن شاه یا فرمان مطاع عزرائیل را به دستشان داده باشند یکه‌ای خورده و لب و لوچه‌ای جنبانده سر و گوشی تکان دادند و بعد نگاهشان را به ما دوخته و چندین بار قد و قامت ما را از بالا به پایین و از پایین به بالا مثل اینکه به قول بچه‌های تهران برایم قبایی دوخته باشند برانداز کرده بالاخره یکیشان گفت «چه طور! آیا شما ایرانی هستید؟»"""
    text = text + text + text + text + text + text + text + text + text + text + text

    counwords = Counter()
    for word in text.split():
        if word not in utils.stopwords:
            counwords[word] += 1

    counwords["شقایق"] = 120

    counwords["عشق"] = 80
    counwords["آسمان"] = 12
    counwords["زمین"] = 3
    counwords["دریاچه"] = 4
    counwords["دریا"] = 13
    counwords["کوه"] = 1
    counwords["خورشید"] = 10
    counwords["زندگی"] = 5
    counwords["ماه"] = 5
    counwords["ستاره"] = 2
    counwords["ابر"] = 1

    worCloud = WordCloud(
        mask="Iran",
        width=1000,
        height=500,
        max_font_size=220,
        min_font_size=5,
        bg_color="white",
        contour_color="black",
    )

    image = worCloud.generate(counwords)
    image.show()
