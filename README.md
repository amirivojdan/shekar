
![Shekar](https://amirivojdan.io/wp-content/uploads/2025/01/shekar-lib.png)

<p align="center">
<a href="https://pypi.python.org/pypi/shekar" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/shekar?color=00A693"></a>
<a href="https://pypi.python.org/pypi/shekar" target="_blank"><img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/amirivojdan/shekar/test.yml?color=00A693"></a>
<a href="https://pypi.python.org/pypi/shekar" target="_blank"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/amirivojdan/shekar?color=00A693"></a>
<a href="https://pypi.python.org/pypi/shekar" target="_blank"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/shekar?color=00A693"></a>
<a href="https://pypi.python.org/pypi/shekar" target="_blank"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/shekar?color=00A693"></a>
</p>


<p align="center">
    <em>Simplifying Persian NLP for Modern Applications</em>
</p>

**Shekar** (meaning 'sugar' in Persian) is a Python library for Persian natural language processing, named after the influential satirical story *"فارسی شکر است"* (Persian is Sugar) published in 1921 by Mohammad Ali Jamalzadeh.
The story became a cornerstone of Iran's literary renaissance, advocating for accessible yet eloquent expression. Shekar embodies this philosophy in its design and development.


### Table of Contents

- [Installation](#installation)
- [Preprocessing](#preprocessing)
  - [Normalizer](#normalizer)
  - [Batch Processing](#batch-processing)
  - [Decorator Support](#decorator-support)
  - [Customization](#customization)
    - [Component Overview](#component-overview)
  - [Using Pipelines](#using-pipelines)
- [Tokenization](#tokenization)
  - [WordTokenizer](#wordtokenizer)
  - [SentenceTokenizer](#sentencetokenizer)
- [Embeddings](#embeddings)
  - [Word Embeddings](#word-embeddings)
  - [Contextual Embeddings](#contextual-embeddings)
- [Stemming](#stemming)
- [Lemmatization](#lemmatization)
- [Part-of-Speech Tagging](#part-of-speech-tagging)
- [Named Entity Recognition (NER)](#named-entity-recognition-ner)
  - [Chaining with Pipelines](#chaining-with-pipelines)
- [Keyword Extraction](#keyword-extraction)
- [Spell Checking](#spell-checking)
- [WordCloud](#wordcloud)
- [Download Models](#download-models)


## Installation

To install the package, you can use **`pip`**. Run the following command:

<!-- termynal -->
```bash
$ pip install shekar
```

## Preprocessing

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/preprocessing.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/preprocessing.ipynb)


### Normalizer

The built-in `Normalizer` class provides a ready-to-use pipeline that combines the most common filters and normalization steps, offering a default configuration that covers the majority of use cases.

```python
from shekar import Normalizer

normalizer = Normalizer()
text = "«فارسی شِکَر است» نام داستان ڪوتاه طنز    آمێزی از محمد علی جمالــــــــزاده  می   باشد که در سال 1921 منتشر  شده است و آغاز   ڱر تحول بزرگی در ادَبێات معاصر ایران 🇮🇷 بۃ شمار میرود."

print(normalizer(text))
```

```shell
«فارسی شکر است» نام داستان کوتاه طنزآمیزی از محمد‌علی جمالزاده می‌باشد که در سال ۱۹۲۱ منتشر شده‌است و آغازگر تحول بزرگی در ادبیات معاصر ایران به شمار می‌رود.
```

### Batch Processing

Both `Normalizer` and `Pipeline` support memory-efficient batch processing:

```python
texts = [
    "پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!",
    "تو را من چشم👀 در راهم!"
]
outputs = normalizer.fit_transform(texts)
print(list(outputs))
```

```shell
["پرنده‌های  قفسی عادت دارن به بی‌کسی", "تو را من چشم در راهم"]
```

### Decorator Support

Use `.on_args(...)` to apply the pipeline to specific function arguments:

```python
@normalizer.on_args(["text"])
def process_text(text):
    return text

print(process_text("تو را من چشم👀 در راهم!"))
```

```shell
تو را من چشم در راهم
```

### Customization

For advanced customization, Shekar offers a modular and composable framework for text preprocessing. It includes components such as `filters`, `normalizers`, and `maskers`, which can be applied individually or flexibly combined using the `Pipeline` class with the `|` operator.

#### Component Overview

<details>
<summary>Filters / Removers</summary>

| Component | Aliases | Description |
|----------|---------|-------------|
| `DiacriticFilter` | `DiacriticRemover`, `RemoveDiacritics` | Removes Persian/Arabic diacritics |
| `EmojiFilter` | `EmojiRemover`, `RemoveEmojis` | Removes emojis |
| `NonPersianLetterFilter` | `NonPersianRemover`, `RemoveNonPersianLetters` | Removes all non-Persian content (optionally keeps English) |
| `PunctuationFilter` | `PunctuationRemover`, `RemovePunctuations` | Removes all punctuation characters |
| `StopWordFilter` | `StopWordRemover`, `RemoveStopWords` | Removes frequent Persian stopwords |
| `DigitFilter` | `DigitRemover`, `RemoveDigits` | Removes all digit characters |
| `RepeatedLetterFilter` | `RepeatedLetterRemover`, `RemoveRepeatedLetters` | Shrinks repeated letters (e.g. "سسسلام") |
| `HTMLTagFilter` | `HTMLRemover`, `RemoveHTMLTags` | Removes HTML tags but retains content |
| `HashtagFilter` | `HashtagRemover`, `RemoveHashtags` | Removes hashtags |
| `MentionFilter` | `MentionRemover`, `RemoveMentions` | Removes @mentions |

</details>

<details>
<summary>Normalizers</summary>

| Component | Aliases | Description |
|----------|---------|-------------|
| `DigitNormalizer` | `NormalizeDigits` | Converts English/Arabic digits to Persian |
| `PunctuationNormalizer` | `NormalizePunctuations` | Standardizes punctuation symbols |
| `AlphabetNormalizer` | `NormalizeAlphabets` | Converts Arabic characters to Persian equivalents |
| `ArabicUnicodeNormalizer` | `NormalizeArabicUnicodes` | Replaces Arabic presentation forms (e.g. ﷽) with Persian equivalents |
| `SpacingNormalizer` | `NormalizeSpacings` | Corrects spacings in Persian text by fixing issues like misplaced spaces, missing zero-width non-joiners (ZWNJ), and incorrect spacing around punctuation and affixes. |
</details>


<details>
<summary>Maskers</summary>

| Component | Aliases | Description |
|----------|---------|-------------|
| `EmailMasker` | `MaskEmails` | Masks or removes email addresses |
| `URLMasker` | `MaskURLs` | Masks or removes URLs |

</details>

### Using Pipelines

You can combine any of the preprocessing components using the `|` operator:

```python
from shekar.preprocessing import EmojiRemover, PunctuationRemover

text = "ز ایران دلش یاد کرد و بسوخت! 🌍🇮🇷"
pipeline = EmojiRemover() | PunctuationRemover()
output = pipeline(text)
print(output)
```

```shell
ز ایران دلش یاد کرد و بسوخت
```

## Tokenization

### WordTokenizer
The WordTokenizer class in Shekar is a simple, rule-based tokenizer for Persian that splits text based on punctuation and whitespace using Unicode-aware regular expressions.

```python
from shekar import WordTokenizer

tokenizer = WordTokenizer()

text = "چه سیب‌های قشنگی! حیات نشئهٔ تنهایی است."
tokens = list(tokenizer(text))
print(tokens)
```

```shell
["چه", "سیب‌های", "قشنگی", "!", "حیات", "نشئهٔ", "تنهایی", "است", "."]
```

### SentenceTokenizer

The `SentenceTokenizer` class is designed to split a given text into individual sentences. This class is particularly useful in natural language processing tasks where understanding the structure and meaning of sentences is important. The `SentenceTokenizer` class can handle various punctuation marks and language-specific rules to accurately identify sentence boundaries.

Below is an example of how to use the `SentenceTokenizer`:

```python
from shekar.tokenizers import SentenceTokenizer

text = "هدف ما کمک به یکدیگر است! ما می‌توانیم با هم کار کنیم."
tokenizer = SentenceTokenizer()
sentences = tokenizer(text)

for sentence in sentences:
    print(sentence)
```

```output
هدف ما کمک به یکدیگر است!
ما می‌توانیم با هم کار کنیم.
```

## Embeddings

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/embeddings.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/embeddings.ipynb)

**Shekar** offers two main embedding classes:

- **`WordEmbedder`**: Provides static word embeddings using pre-trained FastText models.
- **`ContextualEmbedder`**: Provides contextual embeddings using a fine-tuned ALBERT model.

Both classes share a consistent interface:

- `embed(text)` returns a NumPy vector.
- `transform(text)` is an alias for `embed(text)` to integrate with pipelines.

### Word Embeddings

`WordEmbedder` supports two static FastText models:

- **`fasttext-d100`**: A 100-dimensional CBOW model trained on [Persian Wikipedia](https://huggingface.co/datasets/codersan/Persian-Wikipedia-Corpus).
- **`fasttext-d300`**: A 300-dimensional CBOW model trained on the large-scale [Naab dataset](https://huggingface.co/datasets/SLPL/naab).

> **Note:** The word embeddings are static due to Gensim’s outdated dependencies, which can lead to compatibility issues. To ensure stability, the embeddings are stored as pre-computed vectors.

```python
from shekar.embeddings import WordEmbedder

embedder = WordEmbedder(model="fasttext-d100")

embedding = embedder("کتاب")
print(embedding.shape)

similar_words = embedder.most_similar("کتاب", top_n=5)
print(similar_words)
```

### Contextual Embeddings

`ContextualEmbedder` uses an ALBERT model trained with Masked Language Modeling (MLM) on the Naab dataset to generate high-quality contextual embeddings.
The resulting embeddings are 768-dimensional vectors representing the semantic meaning of entire phrases or sentences.

```python
from shekar.embeddings import ContextualEmbedder

embedder = ContextualEmbedder(model="albert")

sentence = "کتاب‌ها دریچه‌ای به جهان دانش هستند."
embedding = embedder(sentence)
print(embedding.shape)  # (768,)
```

## Stemming

The `Stemmer` is a lightweight, rule-based reducer for Persian word forms. It trims common suffixes while respecting Persian orthography and Zero Width Non-Joiner usage. The goal is to produce stable stems for search, indexing, and simple text analysis without requiring a full morphological analyzer.

```python
from shekar import Stemmer

stemmer = Stemmer()

print(stemmer("نوه‌ام"))
print(stemmer("کتاب‌ها"))
print(stemmer("خانه‌هایی"))
```

```output
نوه
کتاب
خانه
```

## Lemmatization

The `Lemmatizer` maps Persian words to their base dictionary form. Unlike stemming, which only trims affixes, lemmatization uses explicit verb conjugation rules, vocabulary lookups, and a stemmer fallback to ensure valid lemmas. This makes it more accurate for tasks like part-of-speech tagging, text normalization, and linguistic analysis where the canonical form of a word is required.

```python
from shekar import Lemmatizer

lemmatizer = Lemmatizer()

print(lemmatizer("رفتند"))
print(lemmatizer("کتاب‌ها"))
print(lemmatizer("خانه‌هایی"))
print(lemmatizer("گفته بوده‌ایم"))
```

```output
رفت/رو
کتاب
خانه
گفت/گو
```

## Part-of-Speech Tagging

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/pos_tagging.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/pos_tagging.ipynb)

The POSTagger class provides part-of-speech tagging for Persian text using a transformer-based model (default: ALBERT). It returns one tag per word based on Universal POS tags (following the Universal Dependencies standard).

Example usage:

```python
from shekar import POSTagger

pos_tagger = POSTagger()
text = "نوروز، جشن سال نو ایرانی، بیش از سه هزار سال قدمت دارد و در کشورهای مختلف جشن گرفته می‌شود."

result = pos_tagger(text)
for word, tag in result:
    print(f"{word}: {tag}")
```

```output
نوروز: PROPN
،: PUNCT
جشن: NOUN
سال: NOUN
نو: ADJ
ایرانی: ADJ
،: PUNCT
بیش: ADJ
از: ADP
سه: NUM
هزار: NUM
سال: NOUN
قدمت: NOUN
دارد: VERB
و: CCONJ
در: ADP
کشورهای: NOUN
مختلف: ADJ
جشن: NOUN
گرفته: VERB
می‌شود: VERB
.: PUNCT
```

## Named Entity Recognition (NER)

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/ner.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/ner.ipynb)

The `NER` module in **Shekar** offers a fast, quantized Named Entity Recognition pipeline using a fine-tuned ALBERT model in ONNX format. It detects common Persian entities such as persons, locations, organizations, and dates. This model is designed for efficient inference and can be easily combined with other preprocessing steps.

Example usage:

```python
from shekar import NER
from shekar import Normalizer

input_text = (
    "شاهرخ مسکوب به سالِ ۱۳۰۴ در بابل زاده شد و دوره ابتدایی را در تهران و در مدرسه علمیه پشت "
    "مسجد سپهسالار گذراند. از کلاس پنجم ابتدایی مطالعه رمان و آثار ادبی را شروع کرد. از همان زمان "
    "در دبیرستان ادب اصفهان ادامه تحصیل داد. پس از پایان تحصیلات دبیرستان در سال ۱۳۲۴ از اصفهان به تهران رفت و "
    "در رشته حقوق دانشگاه تهران مشغول به تحصیل شد."
)

normalizer = Normalizer()
normalized_text = normalizer(input_text)

albert_ner = NER()
entities = albert_ner(normalized_text)

for text, label in entities:
    print(f"{text} → {label}")
```

```output
شاهرخ مسکوب → PER
سال ۱۳۰۴ → DAT
بابل → LOC
دوره ابتدایی → DAT
تهران → LOC
مدرسه علمیه → LOC
مسجد سپهسالار → LOC
دبیرستان ادب اصفهان → LOC
در سال ۱۳۲۴ → DAT
اصفهان → LOC
تهران → LOC
دانشگاه تهران → ORG
فرانسه → LOC
```

**Entity Tags**

The following table summarizes the entity types used by the model (aggregating B- and I- tags):

| Tag     | Description                              |
| ------- | ---------------------------------------- |
| **PER** | Person names                             |
| **LOC** | Locations (cities, countries, landmarks) |
| **ORG** | Organizations (companies, institutions)  |
| **DAT** | Dates and temporal expressions           |
| **EVE** | Events (festivals, historical events)    |
| **O**   | Outside (non-entity text)                |

### Chaining with Pipelines

You can seamlessly chain `NER` with other components using the `|` operator:

```python
from shekar import NER
from shekar import Normalizer

normalizer = Normalizer()
albert_ner = NER()

ner_pipeline = normalizer | albert_ner
entities = ner_pipeline(input_text)

for text, label in entities:
    print(f"{text} → {label}")
```

This chaining enables clean and readable code, letting you build custom NLP flows with preprocessing and tagging in one pass.
 
## Keyword Extraction

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/keyword_extraction.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/keyword_extraction.ipynb)

The **shekar.keyword_extraction** module provides tools for automatically identifying and extracting key terms and phrases from Persian text. These algorithms help identify the most important concepts and topics within documents.

```python
from shekar import KeywordExtractor

extractor = KeywordExtractor(max_length=2, top_n=10)

input_text = (
    "زبان فارسی یکی از زبان‌های مهم منطقه و جهان است که تاریخچه‌ای کهن دارد. "
    "زبان فارسی با داشتن ادبیاتی غنی و شاعرانی برجسته، نقشی بی‌بدیل در گسترش فرهنگ ایرانی ایفا کرده است. "
    "از دوران فردوسی و شاهنامه تا دوران معاصر، زبان فارسی همواره ابزار بیان اندیشه، احساس و هنر بوده است. "
)

keywords = extractor(input_text)

for kw in keywords:
    print(kw)
```
```output
فرهنگ ایرانی
گسترش فرهنگ
ایرانی ایفا
زبان فارسی
تاریخچه‌ای کهن
```

## Spell Checking

The `SpellChecker` class provides simple and effective spelling correction for Persian text. It can automatically detect and fix common errors such as extra characters, spacing mistakes, or misspelled words. You can use it directly as a callable on a sentence to clean up the text, or call `suggest()` to get a ranked list of correction candidates for a single word.

```python
from shekar import SpellChecker

spell_checker = SpellChecker()
print(spell_checker("سسلام بر ششما ددوست من"))

print(spell_checker.suggest("درود"))
```

```output
سلام بر شما دوست من
['درود', 'درصد', 'ورود', 'درد', 'درون']
```

## WordCloud

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/word_cloud.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/word_cloud.ipynb)

The WordCloud class offers an easy way to create visually rich Persian word clouds. It supports reshaping and right-to-left rendering, Persian fonts, color maps, and custom shape masks for accurate and elegant visualization of word frequencies.

```python
import requests
from collections import Counter

from shekar import WordCloud
from shekar import WordTokenizer
from shekar.preprocessing import (
  HTMLTagRemover,
  PunctuationRemover,
  StopWordRemover,
  NonPersianRemover,
)
preprocessing_pipeline = HTMLTagRemover() | PunctuationRemover() | StopWordRemover() | NonPersianRemover()


url = f"https://ganjoor.net/ferdousi/shahname/siavosh/sh9"
response = requests.get(url)
html_content = response.text
clean_text = preprocessing_pipeline(html_content)

word_tokenizer = WordTokenizer()
tokens = word_tokenizer(clean_text)

word_freqs = Counter(tokens)

wordCloud = WordCloud(
        mask="Iran",
        width=1000,
        height=500,
        max_font_size=220,
        min_font_size=5,
        bg_color="white",
        contour_color="black",
        contour_width=3,
        color_map="Set2",
    )

# if shows disconnect words, try again with bidi_reshape=True
image = wordCloud.generate(word_freqs, bidi_reshape=False)
image.show()
```

![](https://raw.githubusercontent.com/amirivojdan/shekar/main/assets/wordcloud_example.png)


## Download Models

If Shekar Hub is unavailable, you can manually download the models and place them in the cache directory at `home/[username]/.shekar/` 

| Model Name                | Download Link |
|----------------------------|---------------|
| FastText Embedding d100    | [Download](https://drive.google.com/file/d/1qgd0slGA3Ar7A2ShViA3v8UTM4qXIEN6/view?usp=drive_link) (50MB)|
| FastText Embedding d300    | [Download](https://drive.google.com/file/d/1yeAg5otGpgoeD-3-E_W9ZwLyTvNKTlCa/view?usp=drive_link) (500MB)|
| SentenceEmbedding    | [Download](https://drive.google.com/file/d/1PftSG2QD2M9qzhAltWk_S38eQLljPUiG/view?usp=drive_link) (60MB)|
| POS Tagger  | [Download](https://drive.google.com/file/d/1d80TJn7moO31nMXT4WEatAaTEUirx2Ju/view?usp=drive_link) (38MB)|
| NER       | [Download](https://drive.google.com/file/d/1DLoMJt8TWlNnGGbHDWjwNGsD7qzlLHfu/view?usp=drive_link) (38MB)|
| AlbertTokenizer   | [Download](https://drive.google.com/file/d/1w-oe53F0nPePMcoor5FgXRwRMwkYqDqM/view?usp=drive_link) (2MB)|

