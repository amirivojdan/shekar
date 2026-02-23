# استخراج کلیدواژه

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/keyword_extraction.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/keyword_extraction.ipynb)

ماژول `shekar.keyword_extraction` ابزارهایی برای شناسایی و استخراج خودکار واژه‌ها و عبارت‌های کلیدی از متن فارسی فراهم می‌کند. این الگوریتم‌ها به برجسته‌سازی مفاهیم اصلی اسناد کمک می‌کنند و در کارهایی مانند خلاصه‌سازی، مدل‌سازی موضوعی و بازیابی اطلاعات مفید هستند.

در حال حاضر، مدل پیش‌فرض استخراج کلیدواژه در Shekar، **RAKE (Rapid Automatic Keyword Extraction)** است.

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
