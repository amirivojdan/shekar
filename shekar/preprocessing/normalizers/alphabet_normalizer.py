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
