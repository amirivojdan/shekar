# Quick Start Guide

Welcome to **Shekar**, a Python library for Persian Natural Language Processing. This guide will walk you through the most essential components so you can get started quickly with preprocessing, tokenization, pipelines, normalization, and embeddings.

---

## 1. Normalize Your Text

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

---

## 2. Use Preprocessing Components

Import and use individual text cleaners like `EmojiRemover`, `DiacriticsRemover`, or `URLMasker`.

```python
from shekar.preprocessing import EmojiRemover

text = "سلام 🌹😊"
print(EmojiRemover()(text))  # Output: "سلام"
```

See the full list of components in `shekar.preprocessing`.

---

## 3. Build Custom Pipelines

Create your own pipeline by chaining any number of preprocessing steps:

```python
from shekar import Pipeline
from shekar.preprocessing import EmojiRemover, PunctuationRemover

pipeline = Pipeline([
    ("emoji", EmojiRemover()),
    ("punct", PunctuationRemover())
])

text = "پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!"
print(pipeline(text))  # Output: "پرنده‌های  قفسی عادت دارن به بی‌کسی"
```

Supports:
- Single strings or batches
- Function decorators for auto-cleaning input arguments

---

## 4. Tokenize Text into Sentences

Use `SentenceTokenizer` to split text into sentences:

```python
from shekar import SentenceTokenizer

text = "هدف ما کمک به یکدیگر است! ما می‌توانیم با هم کار کنیم."
sentences = SentenceTokenizer()(text)

for s in sentences:
    print(s)
```
