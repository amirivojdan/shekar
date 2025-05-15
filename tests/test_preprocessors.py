import pytest
from shekar.preprocessing import (
    PunctuationNormalizer,
    AlphabetNormalizer,
    NumericNormalizer,
    SpacingStandardizer,
    EmojiRemover,
    EmailMasker,
    URLMasker,
    DiacriticsRemover,
    NonPersianRemover,
    HTMLTagRemover,
    RedundantCharacterRemover,
    ArabicUnicodeNormalizer,
    StopwordRemover,
    PunctuationRemover,
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
    expected_output = "ایمیل من: "
    assert email_masker(input_text) == expected_output

    input_text = "ایمیل من: she+kar@she-kar.io"
    expected_output = "ایمیل من: "
    assert email_masker.fit_transform(input_text) == expected_output


def test_mask_url():
    url_masker = URLMasker(mask="")

    input_text = "لینک: https://shekar.parsi-shekar.com"
    expected_output = "لینک: "
    assert url_masker(input_text) == expected_output

    input_text = "لینک: http://shekar2qand.com/id=2"
    expected_output = "لینک: "
    assert url_masker.fit_transform(input_text) == expected_output


def test_normalize_numbers():
    numeric_normalizer = NumericNormalizer()
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
    punc_remover = PunctuationRemover()

    input_text = "اصفهان، نصف جهان!"
    expected_output = "اصفهان نصف جهان"
    assert punc_remover(input_text) == expected_output

    input_text = "فردوسی، شاعر بزرگ ایرانی است."
    expected_output = "فردوسی شاعر بزرگ ایرانی است"
    assert punc_remover.fit_transform(input_text) == expected_output


def test_remove_redundant_characters():
    redundant_character_remover = RedundantCharacterRemover()
    input_text = "سلامم"
    expected_output = "سلامم"
    assert redundant_character_remover(input_text) == expected_output

    input_text = "سلاممممممممممم"
    expected_output = "سلامم"
    assert redundant_character_remover.fit_transform(input_text) == expected_output

    input_text = "روزی باغ ســـــــــــــــــــبــــــــــــــــــز بود"
    expected_output = "روزی باغ سبز بود"
    assert redundant_character_remover(input_text) == expected_output


def test_remove_emojis():
    emoji_remover = EmojiRemover()
    input_text = "😊🇮🇷سلام گلای تو خونه!🎉🎉🎊🎈"
    expected_output = "سلام گلای تو خونه!"
    assert emoji_remover(input_text) == expected_output

    input_text = "🌹باز هم مرغ سحر🐔 بر سر منبر گل"
    expected_output = "باز هم مرغ سحر بر سر منبر گل"

    assert emoji_remover.fit_transform(input_text) == expected_output


def test_remove_diacritics():
    diacritics_remover = DiacriticsRemover()
    input_text = "مَنْ"
    expected_output = "من"
    assert diacritics_remover(input_text) == expected_output

    input_text = "کُجا نِشانِ قَدَم ناتَمام خواهَد ماند؟"
    expected_output = "کجا نشان قدم ناتمام خواهد ماند؟"
    assert diacritics_remover.fit_transform(input_text) == expected_output


def test_remove_stopwords():
    stopword_remover = StopwordRemover()
    input_text = "این یک جملهٔ نمونه است"
    expected_output = "جملهٔ نمونه"
    assert stopword_remover(input_text) == expected_output

    input_text = "وی خاطرنشان کرد"
    expected_output = ""
    assert stopword_remover(input_text) == expected_output

    input_text = "بهتر از ایران کجا می‌شود بود"
    expected_output = "ایران"
    assert stopword_remover(input_text) == expected_output


def test_remove_non_persian():
    non_persian_remover = NonPersianRemover()
    input_text = "با یه گل بهار نمی‌شه"
    expected_output = "با یه گل بهار نمی‌شه"
    assert non_persian_remover(input_text) == expected_output

    input_text = "What you seek is seeking you!"
    expected_output = "     !"
    assert non_persian_remover(input_text) == expected_output

    input_text = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسماً panic attack کردم!"
    expected_output = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسما   کردم!"
    assert non_persian_remover(input_text) == expected_output

    non_persian_remover = NonPersianRemover(keep_english=True)

    input_text = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسماً panic attack کردم!"
    expected_output = "صبح از خواب پاشدم دیدم اینترنت ندارم، رسما panic attack کردم!"
    assert non_persian_remover(input_text) == expected_output

    input_text = "100 سال به این سال‌ها"
    expected_output = "100 سال به این سال‌ها"
    assert non_persian_remover(input_text) == expected_output

    non_persian_remover = NonPersianRemover(keep_diacritics=True)
    input_text = "گُلِ مَنو اَذیَت نَکُنین!"
    expected_output = "گُلِ مَنو اَذیَت نَکُنین!"
    assert non_persian_remover(input_text) == expected_output


def test_remove_html_tags():
    html_tag_remover = HTMLTagRemover()
    input_text = "<p>گل صدبرگ به پیش تو فرو ریخت ز خجلت!</p>"
    expected_output = "گل صدبرگ به پیش تو فرو ریخت ز خجلت!"
    assert html_tag_remover(input_text) == expected_output

    input_text = "<div>آنجا ببر مرا که شرابم نمی‌برد!</div>"
    expected_output = "آنجا ببر مرا که شرابم نمی‌برد!"
    assert html_tag_remover.fit_transform(input_text) == expected_output

    input_text = "<a href='https://example.com'>Example</a>"
    expected_output = "Example"
    assert html_tag_remover(input_text) == expected_output
