# برچسب‌گذاری نقش‌های دستوری (POS)

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/pos_tagging.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/pos_tagging.ipynb)

برچسب‌گذاری نقش دستوری (POS Tagging) به هر واژهٔ جمله یک برچسب دستوری اختصاص می‌دهد. کلاس `POSTagger` در Shekar از یک مدل مبتنی بر ترنسفورمر (پیش‌فرض: **ALBERT**) استفاده می‌کند و خروجی را براساس استاندارد **Universal Dependencies (UD)** تولید می‌کند.

برای هر واژه یک برچسب مانند `NOUN`، `VERB` یا `ADJ` اختصاص داده می‌شود. این خروجی در کارهایی مانند تحلیل نحوی، chunking و استخراج اطلاعات کاربرد دارد.

**ویژگی‌ها**

- **مدل مبتنی بر ترنسفورمر** با دقت بالا
- **برچسب‌های جهانی POS** براساس استاندارد UD
- رابط پایتونی ساده و مستقیم

**نمونهٔ استفاده**

```python
from shekar import POSTagger

# مقداردهی اولیه
pos_tagger = POSTagger()

text = "نوروز، جشن سال نو ایرانی، بیش از سه هزار سال قدمت دارد و در کشورهای مختلف جشن گرفته می‌شود."

# دریافت برچسب‌ها
result = pos_tagger(text)

# چاپ هر واژه همراه برچسب
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
