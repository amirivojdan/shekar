# Keyword Extraction

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/keyword_extraction.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/keyword_extraction.ipynb)

The `shekar.keyword_extraction` module provides tools for automatically identifying and extracting key terms and phrases from Persian text. These algorithms help highlight the most important concepts and topics within documents for tasks such as document summarization, topic modeling, and information retrieval.

Currently, **RAKE (Rapid Automatic Keyword Extraction)** is used as the **default** keyword extraction model.


```python
from shekar import KeywordExtractor

extractor = KeywordExtractor(max_length=2, top_n=10)

input_text = (
    "زبان فارسی یکی از زبان‌های مهم منطقه و جهان است که تاریخچه‌ای کهن دارد. "
    "زبان فارسی با داشتن ادبیاتی غنی و شاعرانی برجسته، نقشی بی‌بدیل در گسترش فرهنگ ایرانی ایفا کرده است. "
    "از دوران فردوسی و شاهنامه تا دوران معاصر، زبان فارسی همواره ابزار بیان اندیشه، احساس و هنر بوده است. "
)

keywords = extractor(input_text)

for kw in keywords:
    print(kw)
```
```shell
فرهنگ ایرانی
گسترش فرهنگ
ایرانی ایفا
زبان فارسی
تاریخچه‌ای کهن
```