
![Shekar](https://amirivojdan.io/wp-content/uploads/2025/01/shekar-lib.png)
![PyPI - Version](https://img.shields.io/pypi/v/shekar?color=00A693)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/amirivojdan/shekar/test.yml?color=00A693)
![Codecov](https://img.shields.io/codecov/c/github/amirivojdan/shekar?color=00A693)
![PyPI - Downloads](https://img.shields.io/pypi/dm/shekar?color=00A693)
![PyPI - License](https://img.shields.io/pypi/l/shekar?color=00A693)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shekar?color=00A693)


<p align="center">
    <em>Simplifying Persian NLP for Modern Applications</em>
</p>

**Shekar** (meaning 'sugar' in Persian) is a Python library for Persian natural language processing, named after the influential satirical story *"فارسی شکر است"* (Persian is Sugar) published in 1921 by Mohammad Ali Jamalzadeh.
The story became a cornerstone of Iran's literary renaissance, advocating for accessible yet eloquent expression.

---

### Table of Contents

- [Installation](#installation)
- [Preprocessing](#preprocessing)
  - [Component Overview](#component-overview)
  - [Using Pipelines](#using-pipelines)
  - [Normalizer](#normalizer)
  - [Batch Processing](#batch-processing)
  - [Decorator Support](#decorator-support)
- [Tokenization](#tokenization)
  - [WordTokenizer](#wordtokenizer)
  - [SentenceTokenizer](#sentencetokenizer)
- [Embeddings](#embeddings)
  - [Word Embeddings](#word-embeddings)
  - [Sentence Embeddings](#sentence-embeddings)
- [Part-of-Speech Tagging](#part-of-speech-tagging)
- [Named Entity Recognition (NER)](#named-entity-recognition-ner)
- [Keyword Extraction](#keyword-extraction)
- [WordCloud](#wordcloud)

---

## Installation

To install the package, you can use **`pip`**. Run the following command:

<!-- termynal -->
```bash
$ pip install shekar
```

## Preprocessing

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/preprocessing.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/preprocessing.ipynb)

Shekar provides a modular, composable system for Persian text preprocessing through `filters`, `normalizers`, `standardizers`, and `maskers`. You can use these independently or combine them using the `Pipeline` class and the `|` operator.

---

### Component Overview

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

</details>

<details>
<summary>Standardizers</summary>

| Component | Aliases | Description |
|----------|---------|-------------|
| `SpacingStandardizer` | `StandardizeSpacings` | Removes extra spaces and fixes spacing around words |
| `PunctuationSpacingStandardizer` | `StandardizePunctuationSpacings` | Adjusts spacing around punctuation marks |

</details>

<details>
<summary>Maskers</summary>

| Component | Aliases | Description |
|----------|---------|-------------|
| `EmailMasker` | `MaskEmails` | Masks or removes email addresses |
| `URLMasker` | `MaskURLs` | Masks or removes URLs |

</details>

---

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

---

### Normalizer

The built-in `Normalizer` class wraps the most common filters and normalizers:

```python
from shekar import Normalizer

normalizer = Normalizer()
text = "ۿدف ما ػمګ بۀ ێڪډيڱڕ أښټ"
print(normalizer(text))
```

```shell
هدف ما کمک به یکدیگر است
```

---

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

---

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

**Shekar** offers two main embedding classes:

- **`WordEmbedder`**: Provides static word embeddings using pre-trained FastText models.
- **`SentenceEmbedder`**: Provides contextual embeddings using a fine-tuned ALBERT model.

Both classes share a consistent interface:

- `embed(text)` returns a NumPy vector.
- `transform(text)` is an alias for `embed(text)` to integrate with pipelines.

---

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

### Sentence Embeddings
SentenceEmbedder uses an ALBERT model trained with Masked Language Modeling (MLM) on the Naab dataset to generate high-quality contextual embeddings.
The resulting embeddings are 768-dimensional vectors representing the semantic meaning of entire phrases or sentences.

```python
from shekar.embeddings import SentenceEmbedder

embedder = SentenceEmbedder(model="albert")

sentence = "کتاب‌ها دریچه‌ای به جهان دانش هستند."
embedding = embedder(sentence)
print(embedding.shape)  # (768,)
```

## Part-of-Speech Tagging

The POSTagger class provides part-of-speech tagging for Persian text using a transformer-based model (default: ALBERT). It returns one tag per word based on Universal POS tags (following the Universal Dependencies standard).

Example usage:

```python
from shekar.pos import POSTagger

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

---

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

You can seamlessly chain `NER` with other components using the `|` operator:

```python
ner_pipeline = normalizer | albert_ner
entities = ner_pipeline(input_text)

for text, label in entities:
    print(f"{text} → {label}")
```

This chaining enables clean and readable code, letting you build custom NLP flows with preprocessing and tagging in one pass.

## Keyword Extraction

The **shekar.keyword_extraction** module provides tools for automatically identifying and extracting key terms and phrases from Persian text. These algorithms help identify the most important concepts and topics within documents.

```python
from shekar.keyword_extraction import RAKE

input_text = (
    "زبان فارسی یکی از زبان‌های مهم منطقه و جهان است که تاریخچه‌ای کهن دارد. "
    "زبان فارسی با داشتن ادبیاتی غنی و شاعرانی برجسته، نقشی بی‌بدیل در گسترش فرهنگ ایرانی ایفا کرده است. "
    "از دوران فردوسی و شاهنامه تا دوران معاصر، زبان فارسی همواره ابزار بیان اندیشه، احساس و هنر بوده است. "
)

extractor = RAKE(max_length=2, top_n=5)
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
