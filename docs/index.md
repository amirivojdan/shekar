
![Banner](https://amirivojdan.io/wp-content/uploads/2025/01/shekar-lib.png)

<p align="center">
    <em>Simplifying Persian NLP for Everyone</em>
</p>

<p align="center">
 <a href="https://img.shields.io/github/actions/workflow/status/amirivojdan/shekar/test.yml" target="_blank">
 <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/amirivojdan/shekar/test.yml?color=00A693">
</a>
<a href="https://pypi.org/project/shekar" target="_blank">
    <img src="https://img.shields.io/pypi/v/shekar?color=00A693" alt="Package version">
</a>

<a href="https://pypi.org/project/shekar" target="_blank">
    <img src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Famirivojdan%2Fshekar%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&color=00A693" alt="Supported Python versions">
</a>
</p>

Shekar (meaning 'sugar' in Persian) is a Python library for Persian natural language processing, named after the influential satirical story *"فارسی شکر است"* (Persian is Sugar) published in 1921 by Mohammad Ali Jamalzadeh.
The story became a cornerstone of Iran's literary renaissance, advocating for accessible yet eloquent expression.
## Installation

To install the package, you can use **`pip`**. Run the following command:

<!-- termynal -->
```bash
$ pip install shekar
```

## Usage

### Normalization

The **`Normalizer`** is built on top of the **`Pipeline`** class, meaning it inherits all its features, including batch processing, argument decorators, and callability. This makes the Normalizer both powerful and flexible: you can use it directly for comprehensive Persian text normalization.

```python

from shekar import Normalizer
normalizer = Normalizer()

text = "ۿدف ما ػمګ بۀ ێڪډيڱڕ أښټ"
text = normalizer.fit_transform(text) # Output: هدف ما کمک به یکدیگر است
print(text)
```
```shell
هدف ما کمک به یکدیگر است
```

#### Batch Support
You can apply the normalizer to a list of strings to enable batch processing.

```python
texts = [
    "یادته گل رز قرمز 🌹 به تو دادم؟",
    "بگو یهویی از کجا پیدات شد؟"
]
outputs = normalizer.fit_transform(texts)
# outputs = normalizer(texts) # Normalizer is callable! 
print(outputs)
# ["یادته گل رز قرمز  به تو دادم", "بگو یهویی از کجا پیدات شد"]
```

#### Normalizer Decorator
Use normalizer decorator to normalize specific arguments.
```python
@normalizer.on_args(["text"])
def process_text(text):
    return text

print(process_text("تو را من چشم👀 در راهم!"))
# Output: "تو را من چشم در راهم"
```

## Custom Normalization Pipeline

The **`Pipeline`** class enables you to chain together multiple preprocessing steps into a single, reusable transformation flow. It is particularly useful when you want to apply several text normalization, cleaning, or masking operations in sequence. The **`Pipeline`** is fully compatible with all preprocessors in **`shekar.preprocessing`**.

### Example Pipeline

```python
from shekar import Pipeline
from shekar.preprocessing import EmojiRemover, PunctuationRemover

steps = [
    ("removeEmoji", EmojiRemover()),
    ("removePunct", PunctuationRemover()),
]

pipeline = Pipeline(steps= steps)

text = "پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!"
output = pipeline.fit_transform(text)
print(output)  # Output: "پرنده‌های  قفسی عادت دارن به بی‌کسی"
```

#### Batch and Decorator Support

Note that **`Pipeline`** objects are **callable**, meaning you can use them like functions to process input data directly.

```python

texts = [
    "یادته گل رز قرمز 🌹 به تو دادم؟",
    "بگو یهویی از کجا پیدات شد؟"
]
outputs = pipeline(texts)
print(outputs)
# ["یادته گل رز قرمز  به تو دادم", "بگو یهویی از کجا پیدات شد"]

# Use decorator to apply pipeline on specific arguments
@pipeline.on_args("text")
def process_text(text):
    return text

print(process_text("تو را من چشم👀 در راهم!"))
# Output: "تو را من چشم در راهم"
```

## Sentence Tokenization

```python

from shekar.tokenizers import SentenceTokenizer

text = "هدف ما کمک به یکدیگر است! ما می‌توانیم با هم کار کنیم."
tokenizer = SentenceTokenizer()
sentences = tokenizer.tokenize(text)

for sentence in sentences:
    print(sentence)
```

```output
هدف ما کمک به یکدیگر است!
ما می‌توانیم با هم کار کنیم.
```


## Word Embeddings

The **`Embedder`** class provides a simple interface for loading and using pre-trained word embeddings. It supports FastText word vectors and allows retrieving word representations and finding similar words.

The following pre-trained models are available for use:

- `fasttext-d300-w5-cbow-naab`: Trained on the Naab corpus with 300-dimensional word vectors.
- `fasttext-d100-w10-cbow-blogs`: Trained on Persian blog texts with 100-dimensional word vectors.

```python

from shekar import Embedder

# Load pre-trained embeddings
embedder = Embedder(model_name="fasttext-d100-w10-cbow-blogs")

# Retrieve word vector
word = "کتاب"
vector = embedder[word]
print(f"Vector for {word}: {vector}")

# Find similar words
similar_words = embedder.most_similar(word, topn=5)
print(f"Words similar to {word}: {similar_words}")

```