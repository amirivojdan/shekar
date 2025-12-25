from shekar.base import BaseTextTransform


class AlphabetNormalizer(BaseTextTransform):
    """
    A text transformation class for normalizing Arabic/Urdu characters to Persian characters.

    This class inherits from `BaseTextTransform` and provides functionality to replace
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
            ("ﺁﺂ", "آ"),
            ("أٲٵ", "أ"),
            ("ﭐﭑٳﺇﺈإٱ", "ا"),
            ("ؠٮٻڀݐݒݔݕݖﭒﭕﺏﺒ", "ب"),
            ("ﭖﭗﭘﭙﭚﭛﭜﭝ", "پ"),
            ("ٹٺټٿݓﭞﭟﭠﭡﭦﭨﺕﺘ", "ت"),
            ("ٽݑﺙﺚﺛﺜﭢﭤ", "ث"),
            ("ڃڄﭲﭴﭵﭷﺝﺟﺠ", "ج"),
            ("ڇڿﭺݘﭼﮀﮁݯ", "چ"),
            ("ځڂڅݗݮﺡﺤ", "ح"),
            ("ﺥﺦﺧ", "خ"),
            ("ڈډڊڋڍۮݙݚﮂﮈﺩ", "د"),
            ("ڌﱛﺫﺬڎڏڐﮅﮇ", "ذ"),
            ("ڑڒړڔڕږۯݛﮌﺭ", "ر"),
            ("ڗݫﺯﺰ", "ز"),
            ("ڙﮊﮋ", "ژ"),
            ("ښڛﺱﺴ", "س"),
            ("ڜۺﺵﺸݜݭ", "ش"),
            ("ڝڞﺹﺼ", "ص"),
            ("ۻﺽﻀ", "ض"),
            ("ﻁﻃﻄ", "ط"),
            ("ﻅﻆﻈڟ", "ظ"),
            ("ڠݝݞݟﻉﻊﻋ", "ع"),
            ("ۼﻍﻎﻐ", "غ"),
            ("ڡڢڣڤڥڦݠݡﭪﭫﭬﻑﻒﻓ", "ف"),
            ("ٯڧڨﻕﻗ", "ق"),
            ("كػؼڪګڬڭڮݢݣﮎﮐﯓﻙﻛ", "ک"),
            ("ڰڱڲڳڴﮒﮔﮖ", "گ"),
            ("ڵڶڷڸݪﻝﻠ", "ل"),
            ("۾ݥݦﻡﻢﻣ", "م"),
            ("ڹںڻڼڽݧݨݩﮞﻥﻧ", "ن"),
            ("ﯝٷﯗﯘﺅٶ", "ؤ"),
            ("ﯙﯚﯜﯞﯟۄۅۉۊۋۏﯠﻭפ", "و"),
            ("ﮤۂ", "ۀ"),
            ("ھۿہۃەﮦﮧﮨﮩﻩﻫة", "ه"),
            ("ﮰﮱٸۓ", "ئ"),
            ("ﯷﯹ", "ئی"),
            ("ﯻ", "ئد"),
            ("ﯫ", "ئا"),
            ("ﯭ", "ئه"),
            ("ﯰﯵﯳ", "ئو"),
            (
                "ؽؾؿىيۍێېۑےﮮﮯﯤﯥﯦﯧﯼﯽﯾﯿﻯﻱﻳﯨﯩﱝ",
                "ی",
            ),
        ]

        self._translation_table = self._create_translation_table(
            self.character_mappings
        )

    def _function(self, X, y=None):
        return X.translate(self._translation_table)
