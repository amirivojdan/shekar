import pytest

from shekar.preprocessing import (
    PunctuationNormalizer,
    AlphabetNormalizer,
    DigitNormalizer,
    SpacingStandardizer,
    EmojiFilter,
    EmailMasker,
    URLMasker,
    DiacriticFilter,
    NonPersianLetterFilter,
    HTMLTagFilter,
    RepeatedLetterFilter,
    ArabicUnicodeNormalizer,
    StopWordFilter,
    PunctuationFilter,
    DigitFilter,
    MentionFilter,
    HashtagFilter,
    PunctuationSpacingStandardizer,
)

from shekar.transforms import (
    NGramExtractor,
    Flatten,
)


def test_correct_spacings():
    spacing_standardizer = SpacingStandardizer()

    input_text = "   این یک جمله   نمونه   است. "
    expected_output = "این یک جمله نمونه است."
    assert spacing_standardizer(input_text) == expected_output

    input_text = "اینجا کجاست؟تو میدونی؟نمیدونم!"
    expected_output = "اینجا کجاست؟تو میدونی؟نمیدونم!"
    assert spacing_standardizer.fit_transform(input_text) == expected_output

    input_text = "ناصر گفت:«من می‌روم.»"
    expected_output = "ناصر گفت:«من می‌روم.»"
    assert spacing_standardizer(input_text) == expected_output

    input_text = "با کی داری حرف می زنی؟"
    expected_output = "با کی داری حرف می زنی؟"
    assert spacing_standardizer(input_text) == expected_output

    input_text = "من می‌روم.تو نمی‌آیی؟"
    expected_output = "من می‌روم.تو نمی‌آیی؟"
    assert spacing_standardizer(input_text) == expected_output

    input_text = "به نکته ریزی اشاره کردی!"
    expected_output = "به نکته ریزی اشاره کردی!"
    assert spacing_standardizer.fit_transform(input_text) == expected_output

    sentences = ["   این یک جمله   نمونه   است. ", "با کی داری حرف می زنی؟"]
    expected_output = ["این یک جمله نمونه است.", "با کی داری حرف می زنی؟"]
    assert list(spacing_standardizer(sentences)) == expected_output
    assert list(spacing_standardizer.fit_transform(sentences)) == expected_output

    input_text = 13.4
    expected_output = "Input must be a string or a Iterable of strings."
    with pytest.raises(ValueError, match=expected_output):
        spacing_standardizer(input_text)


def test_remove_extra_spaces():
    spacing_standardizer = SpacingStandardizer()

    input_text = "این  یک  آزمون  است"
    expected_output = "این یک آزمون است"
    assert spacing_standardizer(input_text) == expected_output

    input_text = "این  یک\n\n\nآزمون  است"
    expected_output = "این یک\n\nآزمون است"
    assert spacing_standardizer(input_text) == expected_output

    input_text = "این\u200cیک\u200cآزمون\u200cاست"
    expected_output = "این\u200cیک\u200cآزمون\u200cاست"
    assert spacing_standardizer.fit_transform(input_text) == expected_output

    input_text = "این\u200c یک\u200c آزمون\u200c است"
    expected_output = "این یک آزمون است"
    assert spacing_standardizer(input_text) == expected_output

    input_text = "این  یک  آزمون  است  "
    expected_output = "این یک آزمون است"
    assert spacing_standardizer.fit_transform(input_text) == expected_output

    input_text = "این  یک  آزمون  است\n\n\n\n"
    expected_output = "این یک آزمون است"
    assert spacing_standardizer(input_text) == expected_output


def test_mask_email():
    email_masker = EmailMasker(mask="")

    input_text = "ایمیل من: she.kar@shekar.panir.io"
    expected_output = "ایمیل من:"
    assert email_masker(input_text) == expected_output

    input_text = "ایمیل من: she+kar@she-kar.io"
    expected_output = "ایمیل من:"
    assert email_masker.fit_transform(input_text) == expected_output


def test_mask_url():
    url_masker = URLMasker(mask="")

    input_text = "لینک: https://shekar.parsi-shekar.com"
    expected_output = "لینک:"
    assert url_masker(input_text) == expected_output

    input_text = "لینک: http://shekar2qand.com/id=2"
    expected_output = "لینک:"
    assert url_masker.fit_transform(input_text) == expected_output


def test_normalize_numbers():
    numeric_normalizer = DigitNormalizer()
    input_text = "٠١٢٣٤٥٦٧٨٩ ⒕34"
    expected_output = "۰۱۲۳۴۵۶۷۸۹ ۱۴۳۴"
    assert numeric_normalizer(input_text) == expected_output

    input_text = "۱۲۳۴۵۶۷۸۹۰"
    expected_output = "۱۲۳۴۵۶۷۸۹۰"
    assert numeric_normalizer.fit_transform(input_text) == expected_output


def test_unify_characters():
    alphabet_normalizer = AlphabetNormalizer()

    input_text = "نشان‌دهندة"
    expected_output = "نشان‌دهنده"
    assert alphabet_normalizer(input_text) == expected_output

    input_text = "دربارۀ ما"
    expected_output = "دربارۀ ما"
    assert alphabet_normalizer.fit_transform(input_text) == expected_output

    input_text = "نامۀ فرهنگستان"
    expected_output = "نامۀ فرهنگستان"
    assert alphabet_normalizer(input_text) == expected_output

    input_text = "رئالیسم رئیس لئیم"
    expected_output = "رئالیسم رئیس لئیم"
    assert alphabet_normalizer(input_text) == expected_output

    input_text = "رأس متلألئ مأخذ"
    expected_output = "رأس متلألئ مأخذ"
    assert alphabet_normalizer(input_text) == expected_output

    input_text = "مؤلف مؤمن مؤسسه"
    expected_output = "مؤلف مؤمن مؤسسه"
    assert alphabet_normalizer(input_text) == expected_output

    input_text = "جزء"
    expected_output = "جزء"
    assert alphabet_normalizer(input_text) == expected_output

    input_text = "سایة"
    expected_output = "سایه"
    assert alphabet_normalizer(input_text) == expected_output

    input_text = "ۿدف ما ػمګ بۃ ێڪډيڱڕ إښټ"
    expected_output = "هدف ما کمک به یکدیگر است"
    assert alphabet_normalizer.fit_transform(input_text) == expected_output

    input_text = "کارتون"
    expected_output = "کارتون"
    assert alphabet_normalizer(input_text) == expected_output

    input_text = "همه با هم در برابر پلیدی و ستم خواهیم ایستاد"
    expected_output = "همه با هم در برابر پلیدی و ستم خواهیم ایستاد"
    assert alphabet_normalizer(input_text) == expected_output


def test_unify_punctuations():
    punct_normalizer = PunctuationNormalizer()

    input_text = "؟?،٬!%:«»؛"
    expected_output = "؟؟،،!٪:«»؛"
    assert punct_normalizer(input_text) == expected_output

    input_text = "سلام!چطوری?"
    expected_output = "سلام!چطوری؟"
    assert punct_normalizer.fit_transform(input_text) == expected_output


def test_unify_arabic_unicode():
    arabic_unicode_normalizer = ArabicUnicodeNormalizer()

    input_text = "﷽"
    expected_output = "بسم الله الرحمن الرحیم"
    assert arabic_unicode_normalizer(input_text) == expected_output

    input_text = "پنجاه هزار ﷼"
    expected_output = "پنجاه هزار ریال"
    assert arabic_unicode_normalizer(input_text) == expected_output

    input_text = "ﷲ اعلم"
    expected_output = "الله اعلم"
    assert arabic_unicode_normalizer.fit_transform(input_text) == expected_output

    input_text = "ﷲ ﷳ"
    expected_output = "الله اکبر"
    assert arabic_unicode_normalizer(input_text) == expected_output

    input_text = "ﷴ"
    expected_output = "محمد"
    assert arabic_unicode_normalizer.fit_transform(input_text) == expected_output


def test_remove_punctuations():
    punc_Filter = PunctuationFilter()

    input_text = "اصفهان، نصف جهان!"
    expected_output = "اصفهان نصف جهان"
    assert punc_Filter(input_text) == expected_output

    input_text = "فردوسی، شاعر بزرگ ایرانی است."
    expected_output = "فردوسی شاعر بزرگ ایرانی است"
    assert punc_Filter.fit_transform(input_text) == expected_output


def test_remove_redundant_characters():
    redundant_character_Filter = RepeatedLetterFilter()
    input_text = "سلامم"
    expected_output = "سلامم"
    assert redundant_character_Filter(input_text) == expected_output

    input_text = "سلاممممممممممم"
    expected_output = "سلامم"
    assert redundant_character_Filter.fit_transform(input_text) == expected_output

    input_text = "روزی باغ ســـــــــــــــــــبــــــــــــــــــز بود"
    expected_output = "روزی باغ سبز بود"
    assert redundant_character_Filter(input_text) == expected_output


def test_remove_emojis():
    emoji_Filter = EmojiFilter()
    input_text = "😊🇮🇷سلام گلای تو خونه!🎉🎉🎊🎈"
    expected_output = "سلام گلای تو خونه!"
    assert emoji_Filter(input_text) == expected_output

    input_text = "🌹باز هم مرغ سحر🐔 بر سر منبر گل"
    expected_output = "باز هم مرغ سحر بر سر منبر گل"

    assert emoji_Filter.fit_transform(input_text) == expected_output


def test_remove_diacritics():
    diacritics_Filter = DiacriticFilter()
    input_text = "مَنْ"
    expected_output = "من"
    assert diacritics_Filter(input_text) == expected_output

    input_text = "کُجا نِشانِ قَدَم ناتَمام خواهَد ماند؟"
    expected_output = "کجا نشان قدم ناتمام خواهد ماند؟"
    assert diacritics_Filter.fit_transform(input_text) == expected_output


def test_remove_stopwords():
    stopword_Filter = StopWordFilter()
    input_text = "این یک جملهٔ نمونه است"
    expected_output = "جملهٔ نمونه"
    assert stopword_Filter(input_text) == expected_output

    input_text = "وی خاطرنشان کرد"
    expected_output = ""
    assert stopword_Filter(input_text) == expected_output

    input_text = "بهتر از ایران کجا می‌شود بود"
    expected_output = "ایران"
    assert stopword_Filter(input_text) == expected_output

    stopword_Filter = StopWordFilter(replace_with="|")
    input_text = "ایران ما زیباتر از تمام جهان"
    expected_output = "ایران | زیباتر | | جهان"
    assert stopword_Filter(input_text) == expected_output


def test_remove_non_persian():
    non_persian_Filter = NonPersianLetterFilter()
    input_text = "با یه گل بهار نمی‌شه"
    expected_output = "با یه گل بهار نمی‌شه"
    assert non_persian_Filter(input_text) == expected_output

    input_text = "What you seek is seeking you!"
    expected_output = "!"
    assert non_persian_Filter(input_text) == expected_output

    input_text = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسماً panic attack کردم!"
    expected_output = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسما   کردم!"
    assert non_persian_Filter(input_text) == expected_output

    non_persian_Filter = NonPersianLetterFilter(keep_english=True)

    input_text = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسماً panic attack کردم!"
    expected_output = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسما panic attack کردم!"
    assert non_persian_Filter(input_text) == expected_output

    input_text = "100 سال به این سال‌ها"
    expected_output = "100 سال به این سال‌ها"
    assert non_persian_Filter(input_text) == expected_output

    non_persian_Filter = NonPersianLetterFilter(keep_diacritics=True)
    input_text = "گُلِ مَنو اَذیَت نَکُنین!"
    expected_output = "گُلِ مَنو اَذیَت نَکُنین!"
    assert non_persian_Filter(input_text) == expected_output


def test_remove_html_tags():
    html_tag_Filter = HTMLTagFilter(replace_with="")
    input_text = "<p>گل صدبرگ به پیش تو فرو ریخت ز خجلت!</p>"
    expected_output = "گل صدبرگ به پیش تو فرو ریخت ز خجلت!"
    assert html_tag_Filter(input_text) == expected_output

    input_text = "<div>آنجا ببر مرا که شرابم نمی‌برد!</div>"
    expected_output = "آنجا ببر مرا که شرابم نمی‌برد!"
    assert html_tag_Filter.fit_transform(input_text) == expected_output

    input_text = "<a href='https://example.com'>Example</a>"
    expected_output = "Example"
    assert html_tag_Filter(input_text) == expected_output

    input_text = "خدایا! خدایا، <b>کویرم!</b>"
    result = html_tag_Filter(input_text)
    assert result == "خدایا! خدایا، کویرم!"


def test_punctuation_spacings():
    batch_input = []
    batch_expected_output = []
    punct_space_standardizer = PunctuationSpacingStandardizer()
    input_text = "سلام!چطوری؟"
    expected_output = "سلام! چطوری؟ "
    assert punct_space_standardizer(input_text) == expected_output

    batch_input.append(input_text)
    batch_expected_output.append(expected_output)

    input_text = "شرکت « گوگل »اعلام کرد ."
    expected_output = "شرکت «گوگل» اعلام کرد. "

    assert punct_space_standardizer.fit_transform(input_text) == expected_output

    batch_input.append(input_text)
    batch_expected_output.append(expected_output)

    assert list(punct_space_standardizer(batch_input)) == batch_expected_output
    assert (
        list(punct_space_standardizer.fit_transform(batch_input))
        == batch_expected_output
    )


def test_mention_Filter():
    mention_Filter = MentionFilter(replace_with="")
    input_text = "@user شما خبر دارید؟"
    expected_output = "شما خبر دارید؟"
    assert mention_Filter(input_text) == expected_output

    input_text = "@user سلام رفقا @user"
    expected_output = "سلام رفقا"
    assert mention_Filter.fit_transform(input_text) == expected_output


def test_hashtag_Filter():
    hashtag_Filter = HashtagFilter(replace_with="")
    input_text = "#پیشرفت_علمی در راستای توسعه"
    expected_output = "در راستای توسعه"
    assert hashtag_Filter(input_text) == expected_output

    input_text = "روز #کودک شاد باد."
    expected_output = "روز  شاد باد."
    assert hashtag_Filter.fit_transform(input_text) == expected_output


def test_ngram_extractor():
    ngram_extractor = NGramExtractor(range=(1, 2))
    input_text = "همان شهر ایرانش آمد به یاد"
    expected_output = [
        "همان",
        "شهر",
        "ایرانش",
        "آمد",
        "به",
        "یاد",
        "همان شهر",
        "شهر ایرانش",
        "ایرانش آمد",
        "آمد به",
        "به یاد",
    ]
    assert ngram_extractor(input_text) == expected_output
    assert ngram_extractor.fit_transform(input_text) == expected_output

    ngram_extractor = NGramExtractor(range=(1, 1))
    input_text = "هیچ جای دنیا تر و خشک را مثل ایران با هم نمی‌سوزانند."
    expected_output = [
        "هیچ",
        "جای",
        "دنیا",
        "تر",
        "و",
        "خشک",
        "را",
        "مثل",
        "ایران",
        "با",
        "هم",
        "نمی‌سوزانند",
        ".",
    ]
    assert ngram_extractor(input_text) == expected_output
    assert ngram_extractor.fit_transform(input_text) == expected_output

    ngram_extractor = NGramExtractor(range=(3, 3))
    input_text = ""
    assert ngram_extractor(input_text) == []

    input_text = "درود"
    assert ngram_extractor(input_text) == []

    input_text = "سلام دوست"
    assert ngram_extractor(input_text) == []

    ngram_extractor = NGramExtractor(range=(3, 3))
    input_text = "این یک متن نمونه است"
    expected_output = [
        "این یک متن",
        "یک متن نمونه",
        "متن نمونه است",
    ]
    assert ngram_extractor(input_text) == expected_output

    ngram_extractor = NGramExtractor(range=(2, 2))
    input_text = [
        "این یک متن",
        "یک متن نمونه",
        "متن نمونه است",
    ]
    expected_output = [
        ["این یک", "یک متن"],
        ["یک متن", "متن نمونه"],
        ["متن نمونه", "نمونه است"],
    ]
    assert list(ngram_extractor(input_text)) == expected_output
    assert list(ngram_extractor.fit_transform(input_text)) == expected_output


def test_ngram_extractor_invalid_inputs():
    with pytest.raises(
        TypeError, match="N-gram range must be a tuple tuple of integers."
    ):
        NGramExtractor(range="invalid")

    with pytest.raises(ValueError, match="N-gram range must be a tuple of length 2."):
        NGramExtractor(range=(1, 2, 3))

    with pytest.raises(ValueError, match="N-gram range must be greater than 0."):
        NGramExtractor(range=(0, 2))

    with pytest.raises(
        ValueError, match="N-gram range must be in the form of \\(min, max\\)."
    ):
        NGramExtractor(range=(3, 1))


def test_flatten():
    flatten = Flatten()
    input_text = [
        ["سلام", "دوست"],
        ["خوبی؟", "چطوری؟"],
    ]
    expected_output = ["سلام", "دوست", "خوبی؟", "چطوری؟"]
    assert list(flatten(input_text)) == expected_output

    input_text = [
        ["سلام", "دوست"],
        ["خوبی؟", "چطوری؟"],
        ["من خوبم", "شما چطورید؟"],
    ]
    expected_output = ["سلام", "دوست", "خوبی؟", "چطوری؟", "من خوبم", "شما چطورید؟"]
    assert list(flatten(input_text)) == expected_output


def test_digit_Filter():
    digit_Filter = DigitFilter()

    input_text = "قیمت این محصول ۱۲۳۴۵ تومان است"
    expected_output = "قیمت این محصول  تومان است"
    assert digit_Filter(input_text) == expected_output

    input_text = "سفارش شما با کد 98765 ثبت شد"
    expected_output = "سفارش شما با کد  ثبت شد"
    assert digit_Filter(input_text) == expected_output

    input_text = "کد پستی ۱۰۴۵۶-32901 را وارد کنید"
    expected_output = "کد پستی - را وارد کنید"
    assert digit_Filter.fit_transform(input_text) == expected_output

    input_text = "سلام، چطوری دوست من؟"
    expected_output = "سلام، چطوری دوست من؟"
    assert digit_Filter(input_text) == expected_output

    digit_Filter_custom = DigitFilter(replace_with="X")
    input_text = "سال ۱۴۰۲ با موفقیت به پایان رسید"
    expected_output = "سال XXXX با موفقیت به پایان رسید"
    assert digit_Filter_custom(input_text) == expected_output

    input_texts = ["شماره ۱۲۳۴", "کد 5678", "بدون عدد"]
    expected_outputs = ["شماره", "کد", "بدون عدد"]
    assert list(digit_Filter(input_texts)) == expected_outputs
    assert list(digit_Filter.fit_transform(input_texts)) == expected_outputs

    input_text = "نرخ تورم ۲۴.۵ درصد اعلام شد"
    expected_output = "نرخ تورم . درصد اعلام شد"
    assert digit_Filter(input_text) == expected_output

    input_text = 12345
    expected_output = "Input must be a string or a Iterable of strings."
    with pytest.raises(ValueError, match=expected_output):
        digit_Filter(input_text)
