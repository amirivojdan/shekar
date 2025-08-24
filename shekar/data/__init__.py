import csv
from importlib import resources
from . import files as data
from . import fonts
from . import masks
from shekar.morphology import Conjugator

resources_root = resources.files(data)
fonts_root = resources.files(fonts)
masks_root = resources.files(masks)

vocab_csv_path = resources_root.joinpath("vocab.csv")
compound_words_csv_path = resources_root.joinpath("compound_words.csv")
verbs_csv_path = resources_root.joinpath("verbs.csv")
stopwords_csv_path = resources_root.joinpath("stopwords.csv")


ZWNJ = "\u200c"
newline = "\n"
diacritics = "ًٌٍَُِّْ"
persian_letters = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
persian_full_set = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی" + "ءؤۀأئ" + ZWNJ
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

non_left_joiner_letters = "دۀذاأآورژز"

suffixes = [
    "ها",
    "های",
    "هایی",
    "ای",
    "تر",
    "تری",
    "ترین",
    "ات",
    "اش",
    "گر",
    "گری",
    "آسا",
    "فام",
    "جات",
    "وش",
    "آگین",
    "باره",
    "آسا",
    "وار",
    "نگر",
    "نگری",
    "زا",
    "زایی",
    "آمیز",
    "آمیزی",
    "زدایی",
    "فرسا",
    "سنج",
    "سنجی",
    "گشا",
    "گشایی",
    "سپاری",
    "شدگی",
    "زدگی",
    "طلبی",
    "یابی",
    "شمول",
    "پیما",
    "پیمایی",
    "شمول",
    "بندی",
    "نویسی",
    "نشین",
    "انگیز",
    "کش",
    "کشی",
    "آور",
    "آلود",
    "نشین",
    "گزین",
    "سازی",
    "کنان",
    "رو",
    "دار",
    "بندی",
    "ریز",
    "مایه",
    "پژوه",
    "گستر",
    "پژوهی",
    "گستری",
    "شناس",
    "شناسی",
    "پذیر",
    "پذیری",
    "ناپذیر",
    "ناپذیری",
    "پراکنی",
    "دهنده",
    "دهندگی",
]

prefixes = [
    "برون",
    "تک",
    "درون",
    "زیست",
    "میان",
    "نیم",
    "سوء",
    "ضد",
    "غیر",
    "بی",
    "هم",
    "نصفه",
    "پاره",
    "نیمه",
]


def load_verbs():
    # Read the verbs from the CSV file
    verbs = set()
    with open(verbs_csv_path, "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            parts = line.strip().split(",")
            past_stem = parts[1]
            present_stem = parts[0]
            verbs.add((past_stem, present_stem))
    return verbs


def read_words(path):
    """Read a list of words from a CSV file."""
    words = set()
    with open(path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # avoid empty rows
                words.add(row[0])
    return words


def read_vocab(path):
    """Read a vocabulary list from a CSV file."""
    vocab = {}
    with open(path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # avoid empty rows
                word = row[0]
                count = int(row[1]) if len(row) > 1 else 1
                vocab[word] = count
    return vocab


verbs = load_verbs()
stopwords = read_words(stopwords_csv_path)
vocab = read_vocab(vocab_csv_path)
compound_words = read_words(compound_words_csv_path)

min_count = min(vocab.values())
vocab = {word: count - min_count for word, count in vocab.items()}


conjugator = Conjugator()
conjugated_verbs = {}


for past_stem, present_stem in verbs:
    conjugations = conjugator.conjugate(past_stem, present_stem)
    for form in conjugations:
        conjugated_verbs[form] = (past_stem, present_stem)

compound_words = compound_words - set(conjugated_verbs.keys())

compound_words_space = {}
for word in compound_words:
    compound_words_space[word.replace(ZWNJ, " ")] = word
