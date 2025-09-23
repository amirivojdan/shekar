# Normalization

Normalization is the process of transforming text into a standard format. This involves converting Arabic characters and numbers to Persian equivalents, replacing spaces with ZERO WIDTH NON-JOINER (half-space) where appropriate, and removing or unifying special characters. Normalization is an essential step in Persian natural language processing (NLP) as it reduces textual variation and improves the performance of downstream models such as search engines, classifiers, or information extraction tools.

## Normalizer

The **`Normalizer`** is a composite tool that standardizes input Persian text by applying a sequence of text transformations. 

### Example Usage

```python
from shekar import Normalizer

normalizer = Normalizer()
text = "«فارسی شِکَر است» نام داستان ڪوتاه طنز    آمێزی از محمد علی جمالــــــــزاده  می   باشد که در سال 1921 منتشر  شده است و آغاز   ڱر تحول بزرگی در ادَبێات معاصر ایران 🇮🇷 بۃ شمار میرود."
normalized = normalizer.normalize(text)
print(normalized)  # Output: "هدف ما کمک به یکدیگر است"
```

```shell
«فارسی شکر است» نام داستان کوتاه طنزآمیزی از محمد‌علی جمالزاده می‌باشد که در سال ۱۹۲۱ منتشر شده‌است و آغازگر تحول بزرگی در ادبیات معاصر ایران به شمار می‌رود.
```

### Batch and Decorator Support

```python
# Apply pipeline to multiple strings
texts = [
    "یادته گل رز قرمز 🌹 به تو دادم؟",
    "بگو یهویی از کجا پیدات شد؟"
]
outputs = normalizer.fit_transform(texts)
print(outputs)
# ["یادته گل رز قرمز  به تو دادم", "بگو یهویی از کجا پیدات شد"]

# Use decorator to apply pipeline on specific arguments
@normalizer.on_args("text")
def process_text(text):
    return text

print(process_text("تو را من چشم👀 در راهم!"))
# Output: "تو را من چشم در راهم"
```


## Custom Normalization Pipeline

You can also build a custom pipeline by selecting specific preprocessors using **`Pipeline`** from **`shekar.preprocessing`**.

### Example Pipeline

```python
from shekar import Pipeline
from shekar.preprocessing import EmojiRemover, PunctuationRemover

steps = [
    ("removeEmoji", EmojiRemover()),
    ("removePunct", PunctuationRemover()),
]

pipeline = Pipeline(steps)

text = "پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!"
output = pipeline.fit_transform(text)
print(output)  # Output: "پرنده‌های  قفسی عادت دارن به بی‌کسی"
```

### Batch and Decorator Support

```python
# Apply pipeline to multiple strings
texts = [
    "یادته گل رز قرمز 🌹 به تو دادم؟",
    "بگو یهویی از کجا پیدات شد؟"
]
outputs = pipeline.fit_transform(texts)
print(outputs)
# ["یادته گل رز قرمز  به تو دادم", "بگو یهویی از کجا پیدات شد"]

# Use decorator to apply pipeline on specific arguments
@pipeline.on_args("text")
def process_text(text):
    return text

print(process_text("تو را من چشم👀 در راهم!"))
# Output: "تو را من چشم در راهم"
```

## Notes

**`Normalizer`** class internally uses transformation steps listed in order as following:

```python
steps = [
                ("AlphabetNormalizer", AlphabetNormalizer()),
                ("ArabicUnicodeNormalizer", ArabicUnicodeNormalizer()),
                ("DigitNormalizer", DigitNormalizer()),
                ("PunctuationNormalizer", PunctuationNormalizer()),
                ("EmailMasker", EmailMasker(mask="")),
                ("URLMasker", URLMasker(mask="")),
                ("EmojiFilter", EmojiFilter()),
                ("HTMLTagFilter", HTMLTagFilter()),
                ("DiacriticFilter", DiacriticFilter()),
                ("RepeatedLetterFilter", RepeatedLetterFilter()),
                ("SpacingNormalizer", SpacingNormalizer()),
            ]
```