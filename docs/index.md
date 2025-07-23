
![Shekar](https://amirivojdan.io/wp-content/uploads/2025/01/shekar-lib.png)
![PyPI - Version](https://img.shields.io/pypi/v/shekar?color=00A693)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/amirivojdan/shekar/test.yml?color=00A693)
![Codecov](https://img.shields.io/codecov/c/github/amirivojdan/shekar?color=00A693)
![PyPI - Downloads](https://img.shields.io/pypi/dm/shekar?color=00A693)
![PyPI - License](https://img.shields.io/pypi/l/shekar?color=00A693)

<p align="center">
    <em>Simplifying Persian NLP for Modern Applications</em>
</p>

**Shekar** (meaning 'sugar' in Persian) is a Python library for Persian natural language processing, named after the influential satirical story *"فارسی شکر است"* (Persian is Sugar) published in 1921 by Mohammad Ali Jamalzadeh.
The story became a cornerstone of Iran's literary renaissance, advocating for accessible yet eloquent expression.
## Installation

To install the package, you can use **`pip`**. Run the following command:

<!-- termynal -->
```bash
$ pip install shekar
```

## Preprocessing

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/preprocessing.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/preprocessing.ipynb)

The `shekar.preprocessing` module provides a rich set of building blocks for cleaning, normalizing, and transforming Persian text. These classes form the foundation of text preprocessing workflows and can be used independently or combined in a `Pipeline`.

Here are some of the key text transformers available in the module:

- **`SpacingStandardizer`**: Removes extra spaces and adjusts spacing around punctuation.
- **`AlphabetNormalizer`**: Converts Arabic characters to standard Persian forms.
- **`NumericNormalizer`**: Converts English and Arabic numerals into Persian digits.
- **`PunctuationNormalizer`**: Standardizes punctuation symbols.
- **`EmojiRemover`**: Removes emojis.
- **`EmailMasker` / `URLMasker`**: Mask or remove emails and URLs.
- **`DiacriticsRemover`**: Removes Persian/Arabic diacritics.
- **`PunctuationRemover`**: Removes all punctuation characters.
- **`RedundantCharacterRemover`**: Shrinks repeated characters like "سسسلام".
- **`ArabicUnicodeNormalizer`**: Converts Arabic presentation forms (e.g., ﷽) into Persian equivalents.
- **`StopwordRemover`**: Removes frequent Persian stopwords.
- **`NonPersianRemover`**: Removes all non-Persian content (optionally keeps English).
- **`HTMLTagRemover`**: Cleans HTML tags but retains content.

Shekar's `Pipeline` class allows you to chain multiple text preprocessing steps together into a seamless and reusable workflow. Inspired by Unix-style piping, Shekar also supports the `|` operator for combining transformers, making your code not only more readable but also expressive and modular.

Example: 

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

Note that **`Pipeline`** objects are **callable**, meaning you can use them like functions to process input data directly.

#### Normalization

The **`Normalizer`** is built on top of the **`Pipeline`** class, meaning it inherits all its features, including batch processing, argument decorators, and callability. This makes the Normalizer both powerful and flexible: you can use it directly for comprehensive Persian text normalization.

```python

from shekar import Normalizer
normalizer = Normalizer()

text = "ۿدف ما ػمګ بۀ ێڪډيڱڕ أښټ"
text = normalizer(text) 
print(text)
```
```shell
هدف ما کمک به یکدیگر است
```

#### Batch Support
You can apply the normalizer/pipeline to a list of strings to enable batch processing.

```python
texts = [
    "پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!",
    "تو را من چشم👀 در راهم!"
]
outputs = normalizer.fit_transform(texts)
# outputs = normalizer(texts) # Normalizer is callable! 
print(list(outputs))
```

```shell
["پرنده‌های  قفسی عادت دارن به بی‌کسی", "تو را من چشم در راهم"]
```

Keep in mind that the result is a **generator**, not a list. This makes the pipeline more memory-efficient, especially when processing large datasets. You can convert the output to a list if needed:

#### Normalizer/Pipeline Decorator
Use pipeline decorator to transform specific arguments.
```python
@normalizer.on_args(["text"])
def process_text(text):
    return text

print(process_text("تو را من چشم👀 در راهم!"))
```

```shell
"تو را من چشم در راهم"
```

## SentenceTokenizer

The `SentenceTokenizer` class is designed to split a given text into individual sentences. This class is particularly useful in natural language processing tasks where understanding the structure and meaning of sentences is important. The `SentenceTokenizer` class can handle various punctuation marks and language-specific rules to accurately identify sentence boundaries.

Below is an example of how to use the `SentenceTokenizer`:

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

counwords = Counter()
for word in tokens:
  counwords[word] += 1

worCloud = WordCloud(
        mask="Iran",
        max_font_size=220,
        min_font_size=5,
        bg_color="white",
        contour_color="black",
        contour_width=5,
        color_map="Greens",
    )

image = worCloud.generate(counwords)
image.show()
```

![](https://raw.githubusercontent.com/amirivojdan/shekar/main/assets/wordcloud_example.png)