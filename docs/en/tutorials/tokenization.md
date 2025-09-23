# Tokenization 

Tokenization is the process of breaking down text into smaller units called tokens. These tokens can be sentences, words, or even characters. Tokenization is a crucial step in natural language processing (NLP) as it helps in understanding and analyzing the structure of the text. It is commonly used in text preprocessing for machine learning models, search engines, and text analysis tools.

## WordTokenizer

The `WordTokenizer` class splits text into individual words and punctuation marks. It is useful for tasks such as part-of-speech tagging, keyword extraction, and any NLP pipeline where token-level analysis is required. The tokenizer handles Persian-specific punctuation, spacing, and diacritics to produce accurate token boundaries.

Below is an example of how to use the `WordTokenizer`:

```python
from shekar import WordTokenizer

text = "چه سیب‌های قشنگی! حیات نشئهٔ تنهایی است."
tokenizer = WordTokenizer()
tokens = tokenizer.tokenize(text)

print(list(tokens)) 
```

```shell
['چه', 'سیب‌های', 'قشنگی', '!', 'حیات', 'نشئهٔ', 'تنهایی', 'است', '.']
```

## SentenceTokenizer

The `SentenceTokenizer` class is designed to split a given text into individual sentences. This class is particularly useful in natural language processing tasks where understanding the structure and meaning of sentences is important. The `SentenceTokenizer` class can handle various punctuation marks and language-specific rules to accurately identify sentence boundaries.

Below is an example of how to use the `SentenceTokenizer`:

```python
from shekar import SentenceTokenizer

text = "هدف ما کمک به یکدیگر است! ما می‌توانیم با هم کار کنیم."
tokenizer = SentenceTokenizer()
sentences = tokenizer(text)

for sentence in sentences:
    print(sentence)
```

```shell
هدف ما کمک به یکدیگر است!
ما می‌توانیم با هم کار کنیم.
```