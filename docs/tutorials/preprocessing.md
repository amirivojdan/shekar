# Preprocessing

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/preprocessing.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/preprocessing.ipynb)

The `shekar.preprocessing` module provides a modular framework for cleaning and standardizing Persian (and mixed-language) text for NLP tasks. It includes normalizers, filters/removers, and maskers, all of which can be used individually or composed into pipelines.

Each component supports:

-   __call__ and fit_transform() for direct usage and pipeline compatibility.
-   Single strings or iterables as input.
-   Error handling for invalid inputs (e.g., raising ValueError for non-string inputs).


## Components

---

## 1. `Normalizers`

| Component | Aliases | Description |
|----------|---------|-------------|
| `DigitNormalizer` | `NormalizeDigits` | Converts English/Arabic digits to Persian |
| `PunctuationNormalizer` | `NormalizePunctuations` | Standardizes punctuation symbols |
| `AlphabetNormalizer` | `NormalizeAlphabets` | Converts Arabic characters to Persian equivalents |
| `ArabicUnicodeNormalizer` | `NormalizeArabicUnicodes` | Replaces Arabic presentation forms (e.g. ﷽) with Persian equivalents |
| `SpacingNormalizer` | `NormalizeSpacings` | Corrects spacings in Persian text by fixing issues like misplaced spaces, missing zero-width non-joiners (ZWNJ), and incorrect spacing around punctuation and affixes. |

**Examples:**

```python
from shekar.preprocessing import AlphabetNormalizer, PunctuationNormalizer,SpacingNormalizer

print(AlphabetNormalizer()("نشان‌دهندة"))  # "نشان‌دهنده"
print(PunctuationNormalizer()("سلام!چطوری?"))  # "سلام!چطوری؟"
print(SpacingNormalizer()("اینجا کجاست؟تو میدانی؟نمیدانم!")) # "اینجا کجاست؟ تو می‌دانی؟ نمی‌دانم!"
```

## 2. `Filters / Removers`

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

**Examples:**

```python
from shekar.preprocessing import EmojiFilter, DiacriticFilter

print(EmojiFilter()("😊🇮🇷سلام گلای تو خونه!🎉🎉🎊🎈"))  # "سلام گلای تو خونه!"
print(DiacriticFilter()("مَنْ"))  # "من"
```

## 3. `Maskers`

| Component | Aliases | Description |
|----------|---------|-------------|
| `EmailMasker` | `MaskEmails` | Masks or removes email addresses |
| `URLMasker` | `MaskURLs` | Masks or removes URLs |

**Examples:**

```python
from shekar.preprocessing import URLMasker
print(URLMasker(mask="")("وب‌سایت ما: https://example.com"))  # "وب‌سایت ما:"
```

## 4. `Utility Transforms`

| Component        | Purpose                                   |
| ---------------- | ----------------------------------------- |
| `NGramExtractor` | Extracts n-grams from text.               |
| `Flatten`        | Flattens nested lists into a single list. |

**Examples:**

```python
from shekar.transforms import NGramExtractor, Flatten

ngrams = NGramExtractor(range=(1, 2))("سلام دنیا")
print(ngrams)  # ['سلام', 'دنیا', 'سلام دنیا']

nested = [["سلام", "دنیا"], ["خوبی؟", "چطوری؟"]]
print(list(Flatten()(nested)))  # ['سلام', 'دنیا', 'خوبی؟', 'چطوری؟']
```