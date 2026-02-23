# شناسایی موجودیت‌های نامدار (NER)

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/ner.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/ner.ipynb)

ماژول `NER` در **Shekar** یک پایپ‌لاین سریع و کوانتایزشده برای شناسایی موجودیت‌های نامدار ارائه می‌دهد. این ماژول از مدل ALBERT ریزتنظیم‌شده (**پیش‌فرض**) استفاده می‌کند که برای استنتاج سریع به فرمت ONNX صادر شده است.

این مدل موجودیت‌های رایج فارسی مانند نام اشخاص، مکان‌ها، سازمان‌ها، تاریخ‌ها و رویدادها را به‌صورت خودکار تشخیص می‌دهد. پایپ‌لاین NER برای سرعت بالا طراحی شده و به‌راحتی با مؤلفه‌های دیگر مانند نرمال‌سازی و توکن‌سازی ترکیب می‌شود.

**نمونهٔ استفاده**

```python
from shekar import NER
from shekar import Normalizer

input_text = (
    "شاهرخ مسکوب به سالِ ۱۳۰۴ در بابل زاده شد و دوره ابتدایی را در تهران و در مدرسه علمیه پشت "
    "مسجد سپهسالار گذراند. از کلاس پنجم ابتدایی مطالعه رمان و آثار ادبی را شروع کرد. از همان زمان "
    "در دبیرستان ادب اصفهان ادامه تحصیل داد. پس از پایان تحصیلات دبیرستان در سال ۱۳۲۴ از اصفهان به تهران رفت و "
    "در رشته حقوق دانشگاه تهران مشغول به تحصیل شد."
)

normalizer = Normalizer()
normalized_text = normalizer(input_text)

albert_ner = NER()
entities = albert_ner(normalized_text)

for text, label in entities:
    print(f"{text} → {label}")
```

```shell
شاهرخ مسکوب → PER
سال ۱۳۰۴ → DAT
بابل → LOC
دوره ابتدایی → DAT
تهران → LOC
مدرسه علمیه → LOC
مسجد سپهسالار → LOC
دبیرستان ادب اصفهان → LOC
در سال ۱۳۲۴ → DAT
اصفهان → LOC
تهران → LOC
دانشگاه تهران → ORG
فرانسه → LOC
```

## برچسب‌های موجودیت

جدول زیر انواع برچسب‌های موجودیت مدل را نشان می‌دهد (با تجمیع برچسب‌های B- و I-):

| Tag     | توضیح |
| ------- | ---------------------------------------- |
| **PER** | نام اشخاص |
| **LOC** | مکان‌ها (شهر، کشور، نشانه‌های جغرافیایی) |
| **ORG** | سازمان‌ها (شرکت‌ها، نهادها) |
| **DAT** | تاریخ‌ها و عبارات زمانی |
| **EVE** | رویدادها (جشن‌ها، رخدادهای تاریخی) |
| **O**   | خارج از موجودیت (متن عادی) |

## زنجیره‌سازی با پایپ‌لاین

می‌توانید `NER` را با مؤلفه‌های دیگر و عملگر `|` ترکیب کنید:

```python
from shekar import NER
from shekar import Normalizer

normalizer = Normalizer()
albert_ner = NER()

ner_pipeline = normalizer | albert_ner
entities = ner_pipeline(input_text)

for text, label in entities:
    print(f"{text} → {label}")
```

این مدل زنجیره‌سازی باعث می‌شود جریان پردازش شما تمیز، خوانا و قابل گسترش باشد.
