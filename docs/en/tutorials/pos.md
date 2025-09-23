# Part-of-Speech Tagging

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/pos_tagging.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/pos_tagging.ipynb)

Part-of-Speech (POS) tagging assigns a grammatical tag to each word in a sentence. The `POSTagger` class in Shekar uses a transformer-based model (default: **ALBERT**) to generate POS tags based on the **Universal Dependencies (UD) standard**.

Each word is assigned a single tag, such as `NOUN`, `VERB`, or `ADJ`, enabling downstream tasks like syntactic parsing, chunking, and information extraction.

**Features**

-   **Transformer-based model** for high accuracy
-   **Universal POS tags** following the UD standard
-   Easy-to-use Python interface

**Example Usage**

```python
from shekar import POSTagger

# Initialize the POS tagger
pos_tagger = POSTagger()

text = "نوروز، جشن سال نو ایرانی، بیش از سه هزار سال قدمت دارد و در کشورهای مختلف جشن گرفته می‌شود."

# Get POS tags
result = pos_tagger(text)

# Print each word with its tag
for word, tag in result:
    print(f"{word}: {tag}")
```

```shell
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