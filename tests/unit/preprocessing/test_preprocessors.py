import pytest

from shekar.preprocessing import (
    PunctuationNormalizer,
    AlphabetNormalizer,
    DigitNormalizer,
    SpacingNormalizer,
    YaNormalizer,
    EmojiMasker,
    EmailMasker,
    URLMasker,
    DiacriticRemover,
    NonPersianLetterMasker,
    HTMLTagMasker,
    RepeatedLetterNormalizer,
    ArabicUnicodeNormalizer,
    StopWordRemover,
    PunctuationRemover,
    DigitRemover,
    MentionMasker,
    HashtagMasker,
    OffensiveWordMasker,
)

from shekar.transforms import (
    NGramExtractor,
    Flatten,
)

from shekar.data import ZWNJ


def test_correct_spacings():
    spacing_normalizer = SpacingNormalizer()

    input_text = (
        "میرویم به خانههای خاک آلود که گفته اند تا چند سال بعد تر ویران نمی شوند !"
    )
    expected_output = (
        "می‌رویم به خانه‌های خاک‌آلود که گفته‌اند تا چند سال بعدتر ویران نمی‌شوند!"
    )
    assert spacing_normalizer(input_text) == expected_output

    input_text = "خونه هاشون خیلی گرون تر شده"
    expected_output = "خونه‌هاشون خیلی گرون‌تر شده"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "دوقلو های هم خون"
    expected_output = "دوقلوهای هم‌خون"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "بنیان گذار خانه هایمان"
    expected_output = "بنیان‌گذار خانه‌هایمان"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "هم شاید"
    expected_output = "هم شاید"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "   این یک جمله   نمونه   است. "
    expected_output = "این یک جمله نمونه است."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "اینجا کجاست؟تو میدانی؟نمیدانم!"
    expected_output = "اینجا کجاست؟ تو می‌دانی؟ نمی‌دانم!"
    assert spacing_normalizer.fit_transform(input_text) == expected_output

    input_text = "ناصر گفت:«من می‌روم.»"
    expected_output = "ناصر گفت: «من می‌روم.»"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "با کی داری حرف می زنی؟"
    expected_output = "با کی داری حرف می‌زنی؟"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "من می‌روم.تو نمی‌آیی؟"
    expected_output = "من می‌روم. تو نمی‌آیی؟"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "به نکته ریزی اشاره کردی!"
    expected_output = "به نکته ریزی اشاره کردی!"
    assert spacing_normalizer.fit_transform(input_text) == expected_output

    sentences = ["   این یک جمله   نمونه   است. ", "با کی داری حرف می زنی؟"]
    expected_output = ["این یک جمله نمونه است.", "با کی داری حرف می‌زنی؟"]
    assert list(spacing_normalizer(sentences)) == expected_output
    assert list(spacing_normalizer.fit_transform(sentences)) == expected_output

    input_text = 13.4
    expected_output = "Input must be a string or a Iterable of strings."
    with pytest.raises(ValueError, match=expected_output):
        spacing_normalizer(input_text)


def test_prefixed_verbs_packed():
    spacing_normalizer = SpacingNormalizer()

    input_text = "می روم کتاب هایم را بر می دارم."
    expected_output = "می‌روم کتاب‌هایم را برمی‌دارم."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "می روم کتاب هایم را بر می‌دارم."
    expected_output = "می‌روم کتاب‌هایم را برمی‌دارم."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "می روم کتاب هایم را بر میدارم."
    expected_output = "می‌روم کتاب‌هایم را برمی‌دارم."
    assert spacing_normalizer(input_text) == expected_output

    input_text = f"می روم کتاب هایم را بر{ZWNJ}میدارم."
    expected_output = "می‌روم کتاب‌هایم را برمی‌دارم."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "کتاب هایم را پس بده!"
    expected_output = "کتاب‌هایم را پس‌بده!"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "کتاب هایم را پس‌بده!"
    expected_output = "کتاب‌هایم را پس‌بده!"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "کتاب هایم را پسبده!"
    expected_output = "کتاب‌هایم را پس‌بده!"
    assert spacing_normalizer(input_text) == expected_output


def test_prefixed_verbs_spacing():
    spacing_normalizer = SpacingNormalizer()

    input_text = "او بر خواهد گشت."
    expected_output = "او بر خواهد گشت."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "او برخواهد گشت."
    expected_output = "او بر خواهد گشت."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "او بر خواهدگشت."
    expected_output = "او بر خواهد گشت."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "او بر نخواهدگشت."
    expected_output = "او بر نخواهد گشت."
    assert spacing_normalizer(input_text) == expected_output

    input_text = "او برنخواهدگشت."
    expected_output = "او بر نخواهد گشت."
    assert spacing_normalizer(input_text) == expected_output

    input_text = f"او بر{ZWNJ}نخواهد{ZWNJ}گشت."
    expected_output = "او بر نخواهد گشت."
    assert spacing_normalizer(input_text) == expected_output


def test_remove_extra_spaces():
    spacing_normalizer = SpacingNormalizer()

    input_text = "این  یک  آزمون  است"
    expected_output = "این یک آزمون است"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "این\u200cیک\u200cآزمون\u200cاست"
    expected_output = "این\u200cیک\u200cآزمون\u200cاست"
    assert spacing_normalizer.fit_transform(input_text) == expected_output

    input_text = "این\u200c یک\u200c آزمون\u200c است"
    expected_output = "این یک آزمون است"
    assert spacing_normalizer(input_text) == expected_output

    # test ZWNJ after non-left joiner letters!
    input_text = "چهار‌لاچنگ"
    expected_output = "چهارلاچنگ"
    assert spacing_normalizer(input_text) == expected_output

    input_text = "این  یک  آزمون  است  "
    expected_output = "این یک آزمون است"
    assert spacing_normalizer.fit_transform(input_text) == expected_output

    input_text = "این  یک  آزمون  است\n\n\n\n"
    expected_output = "این یک آزمون است"
    assert spacing_normalizer(input_text) == expected_output


def test_ya_normalizer():
    ya_normalizer = YaNormalizer(style="standard")

    input_text = "خانه‌ی ما"
    expected_output = "خانۀ ما"
    assert ya_normalizer(input_text) == expected_output

    ya_normalizer = YaNormalizer()
    input_text = "خانۀ ما"
    expected_output = "خانه‌ی ما"
    assert ya_normalizer(input_text) == expected_output


def test_non_left_joiner_compound_words():
    space_normalizer = SpacingNormalizer()

    input_text = "دیدن آن صحنه منزجر کننده بود!"
    expected_output = "دیدن آن صحنه منزجرکننده بود!"
    assert space_normalizer(input_text) == expected_output

    input_text = "کار آفرینی بسیار ارزشمند است."
    expected_output = "کارآفرینی بسیار ارزشمند است."
    assert space_normalizer(input_text) == expected_output

    input_text = "یک کتابخانه خوب باید کاربر پسند باشد!"
    expected_output = "یک کتابخانه خوب باید کاربرپسند باشد!"
    assert space_normalizer(input_text) == expected_output


def test_mask_email():
    email_masker = EmailMasker(mask_token="")

    input_text = "ایمیل من: she.kar@shekar.panir.io"
    expected_output = "ایمیل من:"
    assert email_masker(input_text) == expected_output

    input_text = "ایمیل من: she+kar@she-kar.io"
    expected_output = "ایمیل من:"
    assert email_masker.fit_transform(input_text) == expected_output


def test_mask_url():
    url_masker = URLMasker(mask_token="")

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
    punc_Filter = PunctuationRemover()

    input_text = "اصفهان، نصف جهان!"
    expected_output = "اصفهان نصف جهان"
    assert punc_Filter(input_text) == expected_output

    input_text = "فردوسی، شاعر بزرگ ایرانی است."
    expected_output = "فردوسی شاعر بزرگ ایرانی است"
    assert punc_Filter.fit_transform(input_text) == expected_output


def test_remove_redundant_characters():
    redundant_character_Filter = RepeatedLetterNormalizer()
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
    emoji_Filter = EmojiMasker()
    input_text = "😊🇮🇷سلام گلای تو خونه!🎉🎉🎊🎈"
    expected_output = "سلام گلای تو خونه!"
    assert emoji_Filter(input_text) == expected_output

    input_text = "🌹باز هم مرغ سحر🐔 بر سر منبر گل"
    expected_output = "باز هم مرغ سحر بر سر منبر گل"

    assert emoji_Filter.fit_transform(input_text) == expected_output


def test_remove_diacritics():
    diacritics_Filter = DiacriticRemover()
    input_text = "مَنْ"
    expected_output = "من"
    assert diacritics_Filter(input_text) == expected_output

    input_text = "کُجا نِشانِ قَدَم ناتَمام خواهَد ماند؟"
    expected_output = "کجا نشان قدم ناتمام خواهد ماند؟"
    assert diacritics_Filter.fit_transform(input_text) == expected_output


def test_remove_stopwords():
    stopword_Filter = StopWordRemover()
    input_text = "سلام بر تو"
    expected_output = "سلام"
    assert stopword_Filter(input_text) == expected_output

    input_text = "وی خاطرنشان کرد"
    expected_output = "خاطرنشان کرد"
    assert stopword_Filter(input_text) == expected_output

    input_text = "درود بر ایران"
    expected_output = "درود  ایران"
    assert stopword_Filter(input_text) == expected_output

    stopword_Filter = StopWordRemover(mask_token="|")
    input_text = "درود بر ایران"
    expected_output = "درود | ایران"
    assert stopword_Filter(input_text) == expected_output


def test_remove_non_persian():
    non_persian_Filter = NonPersianLetterMasker()
    input_text = "با یه گل بهار نمی‌شه"
    expected_output = "با یه گل بهار نمی‌شه"
    assert non_persian_Filter(input_text) == expected_output

    input_text = "What you seek is seeking you!"
    expected_output = "!"
    assert non_persian_Filter(input_text) == expected_output

    input_text = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسماً panic attack کردم!"
    expected_output = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسما   کردم!"
    assert non_persian_Filter(input_text) == expected_output

    non_persian_Filter = NonPersianLetterMasker(keep_english=True)

    input_text = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسماً panic attack کردم!"
    expected_output = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسما panic attack کردم!"
    assert non_persian_Filter(input_text) == expected_output

    input_text = "100 سال به این سال‌ها"
    expected_output = "100 سال به این سال‌ها"
    assert non_persian_Filter(input_text) == expected_output

    non_persian_Filter = NonPersianLetterMasker(keep_diacritics=True)
    input_text = "گُلِ مَنو اَذیَت نَکُنین!"
    expected_output = "گُلِ مَنو اَذیَت نَکُنین!"
    assert non_persian_Filter(input_text) == expected_output


def test_remove_html_tags():
    html_tag_Filter = HTMLTagMasker(mask_token="")
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
    punct_space_normalizer = SpacingNormalizer()
    input_text = "سلام!چطوری؟"
    expected_output = "سلام! چطوری؟"
    assert punct_space_normalizer(input_text) == expected_output

    batch_input.append(input_text)
    batch_expected_output.append(expected_output)

    input_text = "شرکت « گوگل »اعلام کرد ."
    expected_output = "شرکت «گوگل» اعلام کرد."

    assert punct_space_normalizer.fit_transform(input_text) == expected_output

    batch_input.append(input_text)
    batch_expected_output.append(expected_output)

    assert list(punct_space_normalizer(batch_input)) == batch_expected_output
    assert (
        list(punct_space_normalizer.fit_transform(batch_input)) == batch_expected_output
    )


def test_mention_masker():
    mention_masker = MentionMasker(mask_token="")
    input_text = "@user شما خبر دارید؟"
    expected_output = "شما خبر دارید؟"
    assert mention_masker(input_text) == expected_output

    input_text = "@user سلام رفقا @user"
    expected_output = "سلام رفقا"
    assert mention_masker.fit_transform(input_text) == expected_output


def test_hashtag_masker():
    hashtag_masker = HashtagMasker(mask_token="")
    input_text = "#پیشرفت_علمی در راستای توسعه"
    expected_output = "در راستای توسعه"
    assert hashtag_masker(input_text) == expected_output

    input_text = "روز #کودک شاد باد."
    expected_output = "روز  شاد باد."
    assert hashtag_masker.fit_transform(input_text) == expected_output


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


def test_digit_remover():
    digit_remover = DigitRemover()

    input_text = "قیمت این محصول ۱۲۳۴۵ تومان است"
    expected_output = "قیمت این محصول  تومان است"
    assert digit_remover(input_text) == expected_output

    input_text = "سفارش شما با کد 98765 ثبت شد"
    expected_output = "سفارش شما با کد  ثبت شد"
    assert digit_remover(input_text) == expected_output

    input_text = "کد پستی ۱۰۴۵۶-32901 را وارد کنید"
    expected_output = "کد پستی - را وارد کنید"
    assert digit_remover.fit_transform(input_text) == expected_output

    input_text = "سلام، چطوری دوست من؟"
    expected_output = "سلام، چطوری دوست من؟"
    assert digit_remover(input_text) == expected_output

    digit_remover_custom = DigitRemover(mask_token="X")
    input_text = "سال ۱۴۰۲ با موفقیت به پایان رسید"
    expected_output = "سال XXXX با موفقیت به پایان رسید"
    assert digit_remover_custom(input_text) == expected_output

    input_texts = ["شماره ۱۲۳۴", "کد 5678", "بدون عدد"]
    expected_outputs = ["شماره", "کد", "بدون عدد"]
    assert list(digit_remover(input_texts)) == expected_outputs
    assert list(digit_remover.fit_transform(input_texts)) == expected_outputs

    input_text = "نرخ تورم ۲۴.۵ درصد اعلام شد"
    expected_output = "نرخ تورم . درصد اعلام شد"
    assert digit_remover(input_text) == expected_output

    input_text = 12345
    expected_output = "Input must be a string or a Iterable of strings."
    with pytest.raises(ValueError, match=expected_output):
        digit_remover(input_text)


def test_offensive_word_masker():
    offensive_word_masker = OffensiveWordMasker(
        words=["تاپاله", "فحش", "بد", "زشت"], mask_token="[بوق]"
    )

    input_text = "عجب آدم تاپاله ای هستی!"
    expected_output = "عجب آدم [بوق] ای هستی!"
    assert offensive_word_masker(input_text) == expected_output

    input_text = "این فحش بد و زشت است"
    expected_output = "این [بوق] [بوق] و [بوق] است"
    assert offensive_word_masker.fit_transform(input_text) == expected_output


def test_offensive_word_masker_default_words():
    offensive_word_masker = OffensiveWordMasker()

    # Test with default offensive words from data.offensive_words
    input_text = "این متن عادی است"
    expected_output = "این متن عادی است"
    assert offensive_word_masker(input_text) == expected_output

    # Test empty mask token behavior
    offensive_word_masker = OffensiveWordMasker(words=["بد", "زشت"], mask_token="")
    input_text = "کلمه بد و زشت را حذف کن"
    expected_output = "کلمه  و  را حذف کن"
    assert offensive_word_masker(input_text) == expected_output

    # Test with iterable input
    input_texts = ["فحش نگو", "کلام زیبا بگو"]
    offensive_word_masker = OffensiveWordMasker(words=["فحش"], mask_token="***")
    expected_outputs = ["*** نگو", "کلام زیبا بگو"]
    assert list(offensive_word_masker(input_texts)) == expected_outputs
