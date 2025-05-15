from typing import Iterable
from shekar.base import BaseTextTransformer
from shekar.tokenizers import WordTokenizer
import shekar.utils as utils
import re
import html
import string
import emoji


class PunctuationNormalizer(BaseTextTransformer):
    """
    A text transformation class for normalizing punctuation marks in text.

    This class inherits from `BaseTextTransformer` and provides functionality to replace
    various punctuation symbols with their normalized equivalents. It uses predefined
    mappings to substitute characters such as dashes, underscores, question marks,
    exclamation marks, and others with consistent representations.

    The `PunctuationNormalizer` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by normalizing punctuation marks.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> punc_normalizer = PunctuationNormalizer()
        >>> normalized_text = punc_normalizer("فارسی شکر است❕نوشته کیست?")
        >>> print(normalized_text)
        "فارسی شکر است! نوشته کیست؟"
    """

    def __init__(self):
        super().__init__()
        self.punctuation_mappings = [
            (r"[▕❘❙❚▏│]", "|"),
            (r"[ㅡ一—–ー̶]", "-"),
            (r"[▁_̲]", "_"),
            (r"[❔?�؟ʕʔ🏻\x08\x97\x9d]", "؟"),
            (r"[❕！]", "!"),
            (r"[⁉]", "!؟"),
            (r"[‼]", "!!"),
            (r"[℅%]", "٪"),
            (r"[÷]", "/"),
            (r"[×]", "*"),
            (r"[：]", ":"),
            (r"[›]", ">"),
            (r"[‹＜]", "<"),
            (r"[《]", "«"),
            (r"[》]", "»"),
            (r"[•]", "."),
            (r"[٬,]", "،"),
            (r"[;；]", "؛"),
        ]

        self._patterns = self._compile_patterns(self.punctuation_mappings)

    def _function(self, X, y=None):
        return self._map_patterns(X, self._patterns)


class AlphabetNormalizer(BaseTextTransformer):
    """
    A text transformation class for normalizing Arabic/Urdu characters to Persian characters.

    This class inherits from `BaseTextTransformer` and provides functionality to replace
    various Arabic/Urdu characters with their Persian equivalents. It uses predefined mappings
    to substitute characters such as different forms of "ی", "ک", and other Arabic letters
    with their standard Persian representations.

    The `AlphabetNormalizer` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by normalizing Arabic/Urdu characters to Persian.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> alphabet_normalizer = AlphabetNormalizer()
        >>> normalized_text = alphabet_normalizer("ۿدف ما ػمګ بۃ ێڪډيڱڕ إښټ")
        >>> print(normalized_text)
        "هدف ما کمک به یکدیگر است"
    """

    def __init__(self):
        super().__init__()
        self.character_mappings = [
            (r"[ﺁﺂ]", "آ"),
            (r"[أٲٵ]", "أ"),
            (r"[ﭐﭑٳﺇﺈإٱ]", "ا"),
            (r"[ؠٮٻڀݐݒݔݕݖﭒﭕﺏﺒ]", "ب"),
            (r"[ﭖﭗﭘﭙﭚﭛﭜﭝ]", "پ"),
            (r"[ٹٺټٿݓﭞﭟﭠﭡﭦﭨﺕﺘ]", "ت"),
            (r"[ٽݑﺙﺚﺛﺜﭢﭤ]", "ث"),
            (r"[ڃڄﭲﭴﭵﭷﺝﺟﺠ]", "ج"),
            (r"[ڇڿﭺݘﭼﮀﮁݯ]", "چ"),
            (r"[ځڂڅݗݮﺡﺤ]", "ح"),
            (r"[ﺥﺦﺧ]", "خ"),
            (r"[ڈډڊڋڍۮݙݚﮂﮈﺩ]", "د"),
            (r"[ڌﱛﺫﺬڎڏڐﮅﮇ]", "ذ"),
            (r"[ڑڒړڔڕږۯݛﮌﺭ]", "ر"),
            (r"[ڗݫﺯﺰ]", "ز"),
            (r"[ڙﮊﮋ]", "ژ"),
            (r"[ښڛﺱﺴ]", "س"),
            (r"[ڜۺﺵﺸݜݭ]", "ش"),
            (r"[ڝڞﺹﺼ]", "ص"),
            (r"[ۻﺽﻀ]", "ض"),
            (r"[ﻁﻃﻄ]", "ط"),
            (r"[ﻅﻆﻈڟ]", "ظ"),
            (r"[ڠݝݞݟﻉﻊﻋ]", "ع"),
            (r"[ۼﻍﻎﻐ]", "غ"),
            (r"[ڡڢڣڤڥڦݠݡﭪﭫﭬﻑﻒﻓ]", "ف"),
            (r"[ٯڧڨﻕﻗ]", "ق"),
            (r"[كػؼڪګڬڭڮݢݣﮎﮐﯓﻙﻛ]", "ک"),
            (r"[ڰڱڲڳڴﮒﮔﮖ]", "گ"),
            (r"[ڵڶڷڸݪﻝﻠ]", "ل"),
            (r"[۾ݥݦﻡﻢﻣ]", "م"),
            (r"[ڹںڻڼڽݧݨݩﮞﻥﻧ]", "ن"),
            (r"[ﯝٷﯗﯘﺅٶ]", "ؤ"),
            (r"[ﯙﯚﯜﯞﯟۄۅۉۊۋۏﯠﻭפ]", "و"),
            (r"[ﮤۂ]", "ۀ"),
            (r"[ھۿہۃەﮦﮧﮨﮩﻩﻫة]", "ه"),
            (r"[ﮰﮱٸۓ]", "ئ"),
            (r"[ﯷﯹ]", "ئی"),
            (r"[ﯻ]", "ئد"),
            (r"[ﯫ]", "ئا"),
            (r"[ﯭ]", "ئه"),
            (r"[ﯰﯵﯳ]", "ئو"),
            (
                r"[ؽؾؿىيۍێېۑےﮮﮯﯤﯥﯦﯧﯼﯽﯾﯿﻯﻱﻳﯨﯩﱝ]",
                "ی",
            ),
        ]

        self._patterns = self._compile_patterns(self.character_mappings)

    def _function(self, X, y=None):
        return self._map_patterns(X, self._patterns)


class ArabicUnicodeNormalizer(BaseTextTransformer):
    """
    A text transformation class for normalizing special Arabic Unicode characters to their Persian equivalents.

    This class inherits from `BaseTextTransformer` and provides functionality to replace
    various special Arabic Unicode characters with their Persian equivalents. It uses predefined mappings
    to substitute characters such as "﷽", "﷼", and other Arabic ligatures with their standard Persian representations.

    The `ArabicUnicodeNormalizer` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by normalizing special Arabic Unicode characters.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> unicode_normalizer = ArabicUnicodeNormalizer()
        >>> normalized_text = unicode_normalizer("﷽ ﷼ ﷴ")
        >>> print(normalized_text)
        "بسم الله الرحمن الرحیم ریال محمد"
    """

    def __init__(self):
        super().__init__()
        self.unicode_mappings = [
            ("﷽", "بسم الله الرحمن الرحیم"),
            ("﷼", "ریال"),
            ("(ﷰ|ﷹ)", "صلی"),
            ("ﷲ", "الله"),
            ("ﷳ", "اکبر"),
            ("ﷴ", "محمد"),
            ("ﷵ", "صلعم"),
            ("ﷶ", "رسول"),
            ("ﷷ", "علیه"),
            ("ﷸ", "وسلم"),
            ("ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ", "لا"),
        ]

        self._patterns = self._compile_patterns(self.unicode_mappings)

    def _function(self, X, y=None):
        return self._map_patterns(X, self._patterns)


class NumericNormalizer(BaseTextTransformer):
    """
    A text transformation class for normalizing Arabic, English, and other Unicode number signs to Persian numbers.

    This class inherits from `BaseTextTransformer` and provides functionality to replace
    various numeric characters from Arabic, English, and other Unicode representations with their Persian equivalents.
    It uses predefined mappings to substitute characters such as "1", "٢", and other numeric signs with their standard Persian representations.

    The `NumericNormalizer` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by normalizing numbers.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> numeric_normalizer = NumericNormalizer()
        >>> normalized_text = numeric_normalizer("1𝟮3٤٥⓺")
        >>> print(normalized_text)
        "۱۲۳۴۵۶"
    """

    def __init__(self):
        super().__init__()
        self._number_mappings = [
            (r"[0٠𝟢𝟬]", "۰"),
            (r"[1١𝟣𝟭⑴⒈⓵①❶𝟙𝟷ı]", "۱"),
            (r"[2٢𝟤𝟮⑵⒉⓶②❷²𝟐𝟸𝟚ᒿշ]", "۲"),
            (r"[3٣𝟥𝟯⑶⒊⓷③❸³ვ]", "۳"),
            (r"[4٤𝟦𝟰⑷⒋⓸④❹⁴]", "۴"),
            (r"[5٥𝟧𝟱⑸⒌⓹⑤❺⁵]", "۵"),
            (r"[6٦𝟨𝟲⑹⒍⓺⑥❻⁶]", "۶"),
            (r"[7٧𝟩𝟳⑺⒎⓻⑦❼⁷]", "۷"),
            (r"[8٨𝟪𝟴⑻⒏⓼⑧❽⁸۸]", "۸"),
            (r"[9٩𝟫𝟵⑼⒐⓽⑨❾⁹]", "۹"),
            (r"[⑽⒑⓾⑩]", "۱۰"),
            (r"[⑾⒒⑪]", "۱۱"),
            (r"[⑿⒓⑫]", "۱۲"),
            (r"[⒀⒔⑬]", "۱۳"),
            (r"[⒁⒕⑭]", "۱۴"),
            (r"[⒂⒖⑮]", "۱۵"),
            (r"[⒃⒗⑯]", "۱۶"),
            (r"[⒄⒘⑰]", "۱۷"),
            (r"[⒅⒙⑱]", "۱۸"),
            (r"[⒆⒚⑲]", "۱۹"),
            (r"[⒇⒛⑳]", "۲۰"),
        ]
        self._patterns = self._compile_patterns(self._number_mappings)

    def _function(self, X, y=None):
        return self._map_patterns(X, self._patterns)


class PunctuationRemover(BaseTextTransformer):
    """
    A text transformation class for removing punctuations from text.

    This class inherits from `BaseTextTransformer` and provides functionality to remove
    all punctuation marks from the text. Optionally, it can retain Persian punctuations
    while removing non-Persian ones.

    The `PunctuationRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing punctuations.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> punctuation_remover = PunctuationRemover(keep_persian=True)
        >>> cleaned_text = punctuation_remover(دریغ است ایران که ویران شود!)
        >>> print(cleaned_text)
        "دریغ است ایران که ویران شود"
    """

    def __init__(self):
        super().__init__()

        self._punctuation_mappings = [
            (rf"[{re.escape(utils.punctuations)}]", ""),
            (rf"[{re.escape(string.punctuation)}]", ""),
        ]

        self._patterns = self._compile_patterns(self._punctuation_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns)


class DiacriticsRemover(BaseTextTransformer):
    """
    A text transformation class for removing Arabic diacritics from the text.

    This class inherits from `BaseTextTransformer` and provides functionality to remove
    Arabic diacritics from the text. It uses predefined mappings to eliminate diacritics
    such as "َ", "ً", "ُ", and others, ensuring a clean and normalized text representation.

    The `DiacriticsRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing diacritics.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> diacritics_remover = DiacriticsRemover()
        >>> cleaned_text = diacritics_remover("کُجا نِشانِ قَدَم ناتَمام خواهَد ماند؟")
        >>> print(cleaned_text)
        "کجا نشان قدم ناتمام خواهد ماند؟"
    """

    def __init__(self):
        super().__init__()
        self._diacritic_mappings = [
            (rf"[{utils.diacritics}]", ""),
        ]

        self._patterns = self._compile_patterns(self._diacritic_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns)


class EmojiRemover(BaseTextTransformer):
    """
    A text transformation class for removing emojis from the text.
    This class inherits from `BaseTextTransformer` and provides functionality to remove
    emojis from the text. It identifies and eliminates a wide range of emojis, ensuring a clean and emoji-free text representation.
    The `EmojiRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing emojis.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> emoji_remover = EmojiRemover()
        >>> cleaned_text = emoji_remover("درود بر شما😊!🌟")
        >>> print(cleaned_text)
        "درود بر شما!"
    """

    def __init__(self):
        super().__init__()

    def _function(self, text: str) -> str:
        return emoji.replace_emoji(text, replace="")


class EmailMasker(BaseTextTransformer):
    """
    A text transformation class for masking email addresses in the text.

    This class inherits from `BaseTextTransformer` and provides functionality to identify
    and mask email addresses in the text. It replaces email addresses with a specified
    mask, ensuring privacy and anonymization of sensitive information.

    The `EmailMasker` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Args:
        mask (str): The mask to replace the email addresses with. Default is "<EMAIL>".

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by masking email addresses.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> email_masker = EmailMasker(mask="<EMAIL>")
        >>> masked_text = email_masker("برای تماس با ما به info@shekar.io ایمیل بزنید.")
        >>> print(masked_text)
        "برای تماس با ما به <EMAIL> ایمیل بزنید."
    """

    def __init__(self, mask: str = "<EMAIL>"):
        super().__init__()
        self.mask = mask
        self._email_mappings = [
            (r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", self.mask),
        ]
        self._patterns = self._compile_patterns(self._email_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns)


class URLMasker(BaseTextTransformer):
    """
    A text transformation class for masking URLs in the text.

    This class inherits from `BaseTextTransformer` and provides functionality to identify
    and mask URLs in the text. It replaces URLs with a specified mask, ensuring privacy
    and anonymization of sensitive information.

    The `URLMasker` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Args:
        mask (str): The mask to replace the URLs with. Default is "<URL>".

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by masking URLs.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.
    Example:
        >>> url_masker = URLMasker(mask="<URL>")
        >>> masked_text = url_masker("برای اطلاعات بیشتر به https://shekar.io مراجعه کنید.")
        >>> print(masked_text)
        "برای اطلاعات بیشتر به <URL> مراجعه کنید."
    """

    def __init__(self, mask: str = "<URL>"):
        super().__init__()
        self.mask = mask
        self._url_mappings = [
            (r"(https?://[^\s]+)", self.mask),
        ]
        self._patterns = self._compile_patterns(self._url_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns)


class SpacingStandardizer(BaseTextTransformer):
    """
    Standardizes spacing in the text regarding the offical Persian script standard published by the Iranian Academy of Language and Literature.
    reference: https://apll.ir/
    This class is also used to remove extra spaces, newlines, zero width nonjoiners, and other unicode space characters.
    """

    def __init__(self):
        super().__init__()
        self._spacing_mappings = [
            (r" {2,}", " "),  # remove extra spaces
            (r"\n{3,}", "\n\n"),  # remove extra newlines
            (r"\u200c{2,}", "\u200c"),  # remove extra ZWNJs
            (r"\u200c{1,} ", " "),  # remove ZWNJs before space
            (r" \u200c{1,}", " "),  # remove ZWNJs after space
            (r"\b\u200c*\B", ""),  # remove ZWNJs at the beginning of words
            (r"\B\u200c*\b", ""),  # remove ZWNJs at the end of words
            (
                r"[\u200b\u200d\u200e\u200f\u2066\u2067\u202a\u202b\u202d]",
                "",
            ),  # remove other unicode space characters
        ]

        self._patterns = self._compile_patterns(self._spacing_mappings)

    def _function(self, text: str) -> str:
        # A POS tagger is needed to identify part of speech tags in the text.

        text = re.sub(r"^(بی|می|نمی)( )", r"\1‌", text)  # verb_prefix
        text = re.sub(r"( )(می|نمی)( )", r"\1\2‌ ", text)  # verb_prefix
        text = re.sub(r"([^ ]ه) ی ", r"\1‌ی ", text)

        return self._map_patterns(text, self._patterns).strip()


class StopwordRemover(BaseTextTransformer):
    """
    A text transformation class for removing Persian stopwords from the text.

    This class inherits from `BaseTextTransformer` and provides functionality to identify
    and remove Persian stopwords from the text. It uses a predefined list of stopwords
    to filter out common words that do not contribute significant meaning to the text.

    The `StopwordRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Args:
        stopwords (Iterable[str], optional): A list of stopwords to be removed from the text.
            If not provided, a default list of Persian stopwords will be used.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing stopwords.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.
    Example:
        >>> stopword_remover = StopwordRemover(stopwords=["و", "به", "از"])
        >>> cleaned_text = stopword_remover("این یک متن نمونه است و به شما کمک می‌کند.")
        >>> print(cleaned_text)
        "این یک متن نمونه است شما کمک می‌کند."
    """

    def __init__(self, stopwords: Iterable[str] = None):
        super().__init__()
        self.stopwords = stopwords or utils.stopwords
        self._word_tokenzer = WordTokenizer()

    def _function(self, text: str) -> str:
        words = self._word_tokenzer(text)
        return " ".join([word for word in words if word not in self.stopwords])


class HTMLTagRemover(BaseTextTransformer):
    """
    A text transformation class for removing HTML tags and entities from the text.

    This class inherits from `BaseTextTransformer` and provides functionality to identify
    and remove HTML tags and entities from the text. It ensures a clean and tag-free
    representation of the text by unescaping HTML entities and removing all HTML tags.

    The `HTMLTagRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing HTML tags and entities.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> html_tag_remover = HTMLTagRemover()
        >>> cleaned_text = html_tag_remover("<p>این یک <strong>متن</strong> نمونه است.</p>")
        >>> print(cleaned_text)
        "این یک متن نمونه است."
    """

    def __init__(self):
        super().__init__()
        self._html_tag_mappings = [
            (r"<[^>]+>", ""),
        ]

        self._patterns = self._compile_patterns(self._html_tag_mappings)

    def _function(self, text: str) -> str:
        text = html.unescape(text)
        return self._map_patterns(text, self._patterns)


class RedundantCharacterRemover(BaseTextTransformer):
    """
    A text transformation class for removing redundant characters from the text.

    This class inherits from `BaseTextTransformer` and provides functionality to identify
    and remove redundant characters from the text. It removes more than two repeated letters
    and eliminates every keshida (ـ) from the text, ensuring a clean and normalized representation.

    The `RedundantCharacterRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing redundant characters.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.

    Example:
        >>> redundant_char_remover = RedundantCharacterRemover()
        >>> cleaned_text = redundant_char_remover("اینــــجاااا یکــــــ متنــــــ نمونه است.")
        >>> print(cleaned_text)
        "اینجاا یک متن نمونه است."
    """

    def __init__(self):
        super().__init__()
        self._redundant_mappings = [
            (r"[ـ]", ""),  # remove keshida
            (r"([^\s])\1{2,}", r"\1\1"),  # remove more than two repeated letters
        ]

        self._patterns = self._compile_patterns(self._redundant_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns)


class NonPersianRemover(BaseTextTransformer):
    """
    A text transformation class for removing non-Persian characters from the text.

    This class inherits from `BaseTextTransformer` and provides functionality to identify
    and remove non-Persian characters from the text. It uses predefined character sets
    to filter out unwanted characters while optionally retaining English characters and diacritics.

    The `NonPersianRemover` class includes `fit` and `fit_transform` methods, and it
    is callable, allowing direct application to text data.

    Args:
        keep_english (bool): If True, retains English characters. Default is False.
        keep_diacritics (bool): If True, retains diacritics. Default is False.

    Methods:

        fit(X, y=None):
            Fits the transformer to the input data.
        transform(X, y=None):
            Transforms the input data by removing non-Persian characters.
        fit_transform(X, y=None):
            Fits the transformer to the input data and applies the transformation.

        __call__(text: str) -> str:
            Allows the class to be called as a function, applying the transformation
            to the input text.
    Example:
        >>> non_persian_remover = NonPersianRemover(keep_english=True, keep_diacritics=False)
        >>> cleaned_text = non_persian_remover("این یک متن نمونه است! Hello!")
        >>> print(cleaned_text)
        "این یک متن نمونه است! Hello!"
    """

    def __init__(self, keep_english=False, keep_diacritics=False):
        super().__init__()

        self.characters_to_keep = (
            utils.persian_letters
            + utils.spaces
            + utils.persian_digits
            + utils.punctuations
        )

        if keep_diacritics:
            self.characters_to_keep += utils.diacritics

        if keep_english:
            self.characters_to_keep += (
                string.ascii_letters + string.digits + string.punctuation
            )

        allowed_chars = re.escape(self.characters_to_keep)
        self._filter_mappings = [(r"[^" + allowed_chars + r"]+", "")]

        self._patterns = self._compile_patterns(self._filter_mappings)

    def _function(self, text: str) -> str:
        return self._map_patterns(text, self._patterns)
