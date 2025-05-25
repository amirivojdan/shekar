import re
from importlib import resources
from shekar import data

data_root = resources.files(data)

vocab_csv_path = data_root.joinpath("vocab.csv") 
verbs_csv_path = data_root.joinpath("verbs.csv")
stopwords_csv_path = data_root.joinpath("stopwords.csv")

ZWNJ = "\u200c"
newline = "\n"
diacritics = "ًٌٍَُِّْ"
persian_letters = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی" + "ءؤۀأئ" + ZWNJ
persian_digits = "۰۱۲۳۴۵۶۷۸۹"
english_digits = "0123456789"
special_signs = "-٪@/#"
end_sentence_punctuations = ".؟!؛" + newline
single_punctuations = "…،:" + end_sentence_punctuations
opener_punctuations = r">{[\(«"
closer_punctuations = r"<}]\)»"
punctuations = (
    single_punctuations + opener_punctuations + closer_punctuations + special_signs
)

spaces = "\u200c" + " "
right_to_left_mark = "\u200f"
arabic_digits = "٠١٢٣٤٥٦٧٨٩"
numbers = persian_digits + english_digits + arabic_digits

no_joiner_letters = "دۀذاأآورژز"


def is_informal(text, threshold=1) -> bool:
    """
    Classifies Persian text into formal or informal based on predefined regex patterns and counts the number of informal matches.
    This function is an implementation of:
    https://fa.wikipedia.org/wiki/%D9%88%DB%8C%DA%A9%DB%8C%E2%80%8C%D9%BE%D8%AF%DB%8C%D8%A7:%D8%A7%D8%B4%D8%AA%D8%A8%D8%A7%D9%87%E2%80%8C%DB%8C%D8%A7%D8%A8/%D9%81%D9%87%D8%B1%D8%B3%D8%AA/%D8%BA%DB%8C%D8%B1%D8%B1%D8%B3%D9%85%DB%8C

    Args:
        text (str): The input Persian text.

    Returns:
        tuple: True or False
    """
    informal_patterns = [
        r"(?:ن?می‌? ?|ب|ن)(?:[یا]فشون|پاشون|پرورون|پرون|پوسون|پوشون|پیچون|تابون|تازون|ترسون|ترکون|تکون|تونست|جنبون|جوشون|چپون|چربون|چرخون|چرون|چسبون|چشون|چکون|چلون|خارون|خراشون|خشکون|خندون|خوابون|خورون|خون|خیسون|درخشون|رسون|رقصون|رنجون|رون|دون|سابون|ستون|سوزون|ش|شورون|غلتون|فهمون|کوبون|گذرون|گردون|گریون|گزین|گسترون|گنجون|لرزون|لغزون|لمبون|مالون|ا?نداز|نشون|هراسون|وزون)(?:م|ی|ه|یم|ید|ن)",
        r"(?:ن?می‌? ?|ب|ن)(?:چا|خا|خوا)(?:م|ی|د|یم|ید|ن)",
        r"(?:ن?می‌? ?|ب)(?:مون|شین|گ)(?:م|ی|ه|یم|ید|ن)",
        r"(?:ن?می‌? ?|ن)(?:دون|د|تون)(?:م|ی|ه|یم|ید|ن)",
        r"(?:نمی‌? ?|ن)(?:یا)(?:م|ه|یم|ید|ن)",
        r"(?:می‌? ?)(?:ر)(?:م|ی|ه|یم|ید|ن)",
        r"(?:ن?می‌? ?|ب|ن)(?:در|پا|کاه|گا|ایست)ن",
        r"(?:ن?می‌? ?|ب|ن)دون(?:م|ی|ه|یم|ید|ن)",
        r"(?:ازش|اونه?ا|ایشون|اینجوری?|این[وه]|بازم|باهاش|براتون|برام|بهش|بی‌خیال|تموم|چ?جوری|چیه|دیگه|کدوم|مونده|زبون|همینه)",
        r"(?:آروم|آشیونه|آشیون|اومدم|برم|اونه|اون‌|ایرونی|اینا|بادمجون|بدونیم|بذار|بریم|بشیم|بشین|بنداز|بچگونه|بیابون|بیگیر|تهرون|تونستم|خمیردندون|خودتون|خودشون|خودمونی|خودمون)",
        r"(?:خوروندن|خونه|خیابون|داره|داروخونه|داغون|دخترونه|دندون|رودخونه|زمونه|زنونه|سوزوندن|قلیون|مردونه|مهمون|موندم|میام|میونه|میون|می‌دونیم|نتونستم|ندونیم)",
        r"(?:نذار|نریم|نسوزوندن|نشونه|نشون|نموندم|نمیاد|نمیام|نمیان|نمیایم|نمیاین|نمیای|نمیدونید|نمی‌دونیم|نمی‌دونین|نیستن|نیومدم|هستن|همزبون|همشون|پسرونه|پشت بوم|کوچیک|تمومه)",
    ]

    match_count = 0

    for pattern in informal_patterns:
        matches = re.findall(pattern, text)
        match_count += len(matches)

    classification = True if match_count >= threshold else False
    return classification


def load_verbs():
    # Read the verbs from the CSV file
    with open(verbs_csv_path, "r", encoding="utf-8") as file:
        verbs = [line.strip().split(",") for line in file.read().splitlines()]
    return verbs


def loadstopwords():
    # Read the stopwords from the text file
    with open(stopwords_csv_path, "r", encoding="utf-8") as file:
        stopwords = [line.strip() for line in file.read().splitlines()]
    return stopwords



verbs = load_verbs()
stopwords = loadstopwords()
