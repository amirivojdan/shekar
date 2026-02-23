# Preprocessing

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/preprocessing.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/preprocessing.ipynb)


## Normalizer

The built-in `Normalizer` class provides a ready-to-use, opinionated normalization pipeline for Persian text. It combines the most common and error-prone normalization steps into a single component, covering the majority of real-world use cases such as web text, social media, OCR output, and mixed informal–formal writing.

Most importantly, the normalization rules in Shekar strictly follow the official guidelines of **[Academy of Persian Language and Literature](https://apll.ir/)** (فرهنگستان زبان و ادب فارسی). This makes the output suitable not only for NLP pipelines, but also for linguistically correct and publishable Persian text.

```python
from shekar import Normalizer

normalizer = Normalizer()

text = "«فارسی شِکَر است» نام داستان ڪوتاه طنز    آمێزی از محمد علی جمالــــــــزاده ی گرامی می   باشد که در سال 1921 منتشر  شده است و آغاز   ڱر تحول بزرگی در ادَبێات معاصر ایران بۃ شمار میرود."
print(normalizer(text))

# نرمال‌سازی نویسه‌های گفتاری و روزمره
text = normalizer("می دونی که نمیخاستم ناراحتت کنم.اما خونه هاشون خیلی گرون تر شده")
print(text)

# نرمال‌سازی واژه‌های مرکب و افعال پیشوندی! 
text = normalizer("یک کار آفرین نمونه و سخت کوش ، پیروز مندانه از پس دشواری ها برخواهدآمد.")
print(text) 

```

### Batch and Decorator Support

```python
texts = [
	"یادته گل رز قرمز 🌹 به تو دادم؟",
	"بگو یهویی از کجا پیدات شد؟"
]
outputs = normalizer.fit_transform(texts)
print(outputs)

@normalizer.on_args("text")
def process_text(text):
	return text

print(process_text("تو را من چشم👀 در راهم!"))
```

### Customization

Shekar is built around a modular and composable preprocessing framework that allows fine-grained control over each step of text processing. Preprocessing is implemented as small, independent operators such as `filters`, `normalizers`, and `maskers`, which can be used on their own or combined into flexible pipelines.

Pipelines are constructed using the Pipeline abstraction and composed with the `|` operator, making preprocessing logic explicit, readable, and easy to customize. 

For example, the following pipeline is functionally equivalent to the default normalizer:

```python
from shekar.preprocessing import (
    PunctuationNormalizer,
    AlphabetNormalizer,
    DigitNormalizer,
    SpacingNormalizer,
    RemoveDiacritics,
    RepeatedLetterNormalizer,
    ArabicUnicodeNormalizer,
    YaNormalizer,
)

normalizer = (
            AlphabetNormalizer()
            | ArabicUnicodeNormalizer()
            | DigitNormalizer()
            | PunctuationNormalizer()
            | RemoveDiacritics()
            | RepeatedLetterNormalizer()
            | SpacingNormalizer()
            | YaNormalizer(style="joda")
        )
```

Operators can also be composed for lightweight, task-specific preprocessing. For example, removing emojis and punctuation:

```python
from shekar.preprocessing import EmojiRemover, PunctuationRemover

text = "ز ایران دلش یاد کرد و بسوخت! 🌍🇮🇷"
pipeline = EmojiRemover() | PunctuationRemover()
output = pipeline(text)
print(output)
```

#### Pipeline Features

- Composable steps in a defined order
- `|` operator chaining for concise definitions
- Single-string and batch input support
- Callable pipeline object (`pipeline(text)`)
- Decorator support via `.on_args(...)`
- Clear errors for invalid inputs or configuration

#### Modular Preprocessing Components

The `shekar.preprocessing` package provides reusable blocks that can be used standalone or inside `Pipeline`.

#### 1) Normalizers

| Component | Aliases | Description |
|------------|----------|-------------|
| `AlphabetNormalizer` | `NormalizeAlphabets` | Converts Arabic characters to Persian equivalents |
| `ArabicUnicodeNormalizer` | `NormalizeArabicUnicodes` | Replaces Arabic presentation forms (e.g., ﷽) with Persian equivalents |
| `DigitNormalizer` | `NormalizeDigits` | Converts English/Arabic digits to Persian |
| `PunctuationNormalizer` | `NormalizePunctuations` | Standardizes punctuation symbols |
| `RepeatedLetterNormalizer` | `NormalizeRepeatedLetters` | Normalizes repeated letters (e.g., “سسسلام” → “سسلام”) |
| `SpacingNormalizer` | `NormalizeSpacings` | Fixes spacing, ZWNJ placement, and punctuation spacing |
| `YaNormalizer` | `NormalizeYas` | Normalizes Persian “یـا” in either `standard` or `joda` style |

```python
from shekar.preprocessing import AlphabetNormalizer, PunctuationNormalizer, SpacingNormalizer

print(AlphabetNormalizer()("نشان‌دهندة"))
print(PunctuationNormalizer()("سلام!چطوری?"))
print(SpacingNormalizer()("اینجا کجاست؟تو میدانی؟نمیدانم!"))
```

#### 2) Filters / Removers

| Component | Aliases | Description |
|----------|---------|-------------|
| `DiacriticFilter` | `DiacriticRemover`, `RemoveDiacritics` | Removes Persian/Arabic diacritics |
| `EmojiFilter` | `EmojiRemover`, `RemoveEmojis` | Removes emojis |
| `NonPersianLetterFilter` | `NonPersianRemover`, `RemoveNonPersianLetters` | Removes non-Persian content (optionally keeps English) |
| `PunctuationFilter` | `PunctuationRemover`, `RemovePunctuations` | Removes punctuation characters |
| `StopWordFilter` | `StopWordRemover`, `RemoveStopWords` | Removes frequent Persian stopwords |
| `DigitFilter` | `DigitRemover`, `RemoveDigits` | Removes digit characters |
| `RepeatedLetterFilter` | `RepeatedLetterRemover`, `RemoveRepeatedLetters` | Shrinks repeated letters |
| `HTMLTagFilter` | `HTMLRemover`, `RemoveHTMLTags` | Removes HTML tags while keeping content |
| `HashtagFilter` | `HashtagRemover`, `RemoveHashtags` | Removes hashtags |
| `MentionFilter` | `MentionRemover`, `RemoveMentions` | Removes @mentions |

```python
from shekar.preprocessing import EmojiFilter, DiacriticFilter

print(EmojiFilter()("😊🇮🇷سلام گلای تو خونه!🎉🎉🎊🎈"))
print(DiacriticFilter()("مَنْ"))
```

#### 3) Maskers

| Component | Aliases | Description |
|----------|---------|-------------|
| `EmailMasker` | `MaskEmails` | Masks or removes email addresses |
| `URLMasker` | `MaskURLs` | Masks or removes URLs |

```python
from shekar.preprocessing import URLMasker

print(URLMasker(mask="")("وب‌سایت ما: https://example.com"))
```

#### 4) Utility Transforms

| Component        | Purpose |
| ---------------- | ------- |
| `NGramExtractor` | Extracts n-grams from text |
| `Flatten`        | Flattens nested lists into one list |

```python
from shekar.transforms import NGramExtractor, Flatten

ngrams = NGramExtractor(range=(1, 2))("سلام دنیا")
print(ngrams)

nested = [["سلام", "دنیا"], ["خوبی؟", "چطوری؟"]]
print(list(Flatten()(nested)))
```