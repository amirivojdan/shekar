# Quick Start Guide

Welcome to **Shekar**, a Python library for Persian Natural Language Processing. This guide will walk you through the most essential components so you can get started quickly with preprocessing, tokenization, pipelines, normalization, and embeddings.

---

## 1. Normalize Your Text

Use the `Normalizer` to standardize noisy or non-standard Persian text by applying a built-in pipeline of transformations.

```python
from shekar import Normalizer

normalizer = Normalizer()
text = "ۿدف ما ػمګ بۀ ێڪډيڱڕ أښټ"
print(normalizer.normalize(text))  # Output: "هدف ما کمک به یکدیگر است"
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
from shekar.tokenizers import SentenceTokenizer

text = "هدف ما کمک به یکدیگر است! ما می‌توانیم با هم کار کنیم."
sentences = SentenceTokenizer().tokenize(text)

for s in sentences:
    print(s)
```

---
 
## Summary

| Task           | Tool / Class         |
|----------------|----------------------|
| Normalize text | `Normalizer`         |
| Clean text     | `shekar.preprocessing` |
| Create pipeline| `Pipeline`           |
| Tokenize       | `SentenceTokenizer`  |
| Word Cloud   | `WordCloud`           |

All components work with both single strings and lists. Pipelines are composable and can be reused, tested, or applied dynamically via decorators.
