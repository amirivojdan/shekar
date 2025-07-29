from importlib import resources
from . import files as data
from . import fonts
from . import masks

resources_root = resources.files(data)
fonts_root = resources.files(fonts)
masks_root = resources.files(masks)

vocab_csv_path = resources_root.joinpath("vocab.csv")
verbs_csv_path = resources_root.joinpath("verbs.csv")
stopwords_csv_path = resources_root.joinpath("stopwords.csv")

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
