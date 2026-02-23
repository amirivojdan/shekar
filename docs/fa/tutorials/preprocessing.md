# پیش‌پردازش

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/preprocessing.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/preprocessing.ipynb)

## نرمال‌ساز (Normalizer)

کلاس داخلی `Normalizer` یک خط لولهٔ آماده و کاربردی برای نرمال‌سازی متن فارسی است. این کلاس رایج‌ترین و خطاپذیرترین مراحل نرمال‌سازی را در یک مؤلفه ترکیب می‌کند و بیشتر سناریوهای واقعی مانند متن وب، شبکه‌های اجتماعی، خروجی OCR و نوشتار نیمه‌رسمی/محاوره‌ای را پوشش می‌دهد.

مهم‌تر از همه، قواعد نرمال‌سازی در Shekar مطابق دستورالعمل‌های رسمی **[فرهنگستان زبان و ادب فارسی](https://apll.ir/)** پیاده‌سازی شده است؛ بنابراین خروجی، علاوه بر مناسب‌بودن برای پایپ‌لاین‌های NLP، از نظر زبانی نیز درست و قابل انتشار است.

```python
from shekar import Normalizer

normalizer = Normalizer()

text = "«فارسی شِکَر است» نام داستان ڪوتاه طنز    آمێزی از محمد علی جمالــــــــزاده ی گرامی می   باشد که در سال 1921 منتشر  شده است و آغاز   ڱر تحول بزرگی در ادَبێات معاصر ایران بۃ شمار میرود."
print(normalizer(text))

# نرمال‌سازی نویسه‌های گفتاری و روزمره
text = normalizer("می دونی که نمیخاستم ناراحتت کنم.اما خونه هاشون خیلی گرون تر شده")
print(text)

# نرمال‌سازی واژه‌های مرکب و افعال پیشوندی
text = normalizer("یک کار آفرین نمونه و سخت کوش ، پیروز مندانه از پس دشواری ها برخواهدآمد.")
print(text)
```

### پشتیبانی از پردازش دسته‌ای و دکوراتور

```python
texts = [
    "یادته گل رز قرمز 🌹 به تو دادم؟",
    "بگو یهویی از کجا پیدات شد؟"
]
outputs = normalizer.fit_transform(texts)
print(outputs)

@normalizer.on_args("text")
def process_text(text):
    return text

print(process_text("تو را من چشم👀 در راهم!"))
```

### سفارشی‌سازی

Shekar بر پایهٔ یک چارچوب ماژولار و ترکیب‌پذیر برای پیش‌پردازش متن ساخته شده است. مراحل پیش‌پردازش به‌صورت عملگرهای کوچک و مستقل مانند `filters`، `normalizers` و `maskers` ارائه می‌شوند که می‌توانند به‌صورت مستقل یا در قالب پایپ‌لاین ترکیب شوند.

پایپ‌لاین‌ها با انتزاع `Pipeline` ساخته می‌شوند و با عملگر `|` به هم متصل می‌گردند؛ بنابراین منطق پیش‌پردازش صریح، خوانا و قابل نگهداری خواهد بود.

برای مثال، پایپ‌لاین زیر از نظر عملکرد معادل نرمال‌ساز پیش‌فرض است:

```python
from shekar.preprocessing import (
    PunctuationNormalizer,
    AlphabetNormalizer,
    DigitNormalizer,
    SpacingNormalizer,
    RemoveDiacritics,
    RepeatedLetterNormalizer,
    ArabicUnicodeNormalizer,
    YaNormalizer,
)

normalizer = (
    AlphabetNormalizer()
    | ArabicUnicodeNormalizer()
    | DigitNormalizer()
    | PunctuationNormalizer()
    | RemoveDiacritics()
    | RepeatedLetterNormalizer()
    | SpacingNormalizer()
    | YaNormalizer(style="joda")
)
```

همچنین می‌توانید برای سناریوهای سبک‌تر، عملگرها را با هم ترکیب کنید. مثال: حذف ایموجی و نشانه‌گذاری.

```python
from shekar.preprocessing import EmojiRemover, PunctuationRemover

text = "ز ایران دلش یاد کرد و بسوخت! 🌍🇮🇷"
pipeline = EmojiRemover() | PunctuationRemover()
output = pipeline(text)
print(output)
```

#### ویژگی‌های پایپ‌لاین

- ترکیب‌پذیری مراحل در ترتیب مشخص
- زنجیره‌سازی خلاصه با عملگر `|`
- پشتیبانی از ورودی تکی و دسته‌ای
- قابلیت فراخوانی مستقیم پایپ‌لاین (`pipeline(text)`)
- پشتیبانی از دکوراتور با `.on_args(...)`
- خطاهای واضح برای ورودی یا پیکربندی نامعتبر

#### اجزای ماژولار پیش‌پردازش

پکیج `shekar.preprocessing` بلوک‌های قابل استفادهٔ مجددی فراهم می‌کند که می‌توانند مستقل یا داخل `Pipeline` استفاده شوند.

#### ۱) نرمال‌سازها

| مؤلفه | نام‌های جایگزین | توضیح |
|------------|----------|-------------|
| `AlphabetNormalizer` | `NormalizeAlphabets` | تبدیل نویسه‌های عربی به معادل فارسی |
| `ArabicUnicodeNormalizer` | `NormalizeArabicUnicodes` | جایگزینی فرم‌های نمایشی عربی (مثل ﷽) با معادل فارسی |
| `DigitNormalizer` | `NormalizeDigits` | تبدیل ارقام انگلیسی/عربی به فارسی |
| `PunctuationNormalizer` | `NormalizePunctuations` | استانداردسازی علائم نگارشی |
| `RepeatedLetterNormalizer` | `NormalizeRepeatedLetters` | نرمال‌سازی حروف تکراری (مثال: «سسسلام» → «سسلام») |
| `SpacingNormalizer` | `NormalizeSpacings` | اصلاح فاصله‌ها، نیم‌فاصله و فاصله‌گذاری نشانه‌گذاری |
| `YaNormalizer` | `NormalizeYas` | یکدست‌سازی «یـا» در حالت `standard` یا `joda` |

```python
from shekar.preprocessing import AlphabetNormalizer, PunctuationNormalizer, SpacingNormalizer

print(AlphabetNormalizer()("نشان‌دهندة"))
print(PunctuationNormalizer()("سلام!چطوری?"))
print(SpacingNormalizer()("اینجا کجاست؟تو میدانی؟نمیدانم!"))
```

#### ۲) فیلترها / حذف‌کننده‌ها

| مؤلفه | نام‌های جایگزین | توضیح |
|----------|---------|-------------|
| `DiacriticFilter` | `DiacriticRemover`, `RemoveDiacritics` | حذف اعراب فارسی/عربی |
| `EmojiFilter` | `EmojiRemover`, `RemoveEmojis` | حذف ایموجی |
| `NonPersianLetterFilter` | `NonPersianRemover`, `RemoveNonPersianLetters` | حذف محتوای غیرفارسی (اختیاری: حفظ انگلیسی) |
| `PunctuationFilter` | `PunctuationRemover`, `RemovePunctuations` | حذف نشانه‌های نگارشی |
| `StopWordFilter` | `StopWordRemover`, `RemoveStopWords` | حذف ایست‌واژه‌های پرتکرار فارسی |
| `DigitFilter` | `DigitRemover`, `RemoveDigits` | حذف ارقام |
| `RepeatedLetterFilter` | `RepeatedLetterRemover`, `RemoveRepeatedLetters` | کاهش کشیدگی/تکرار حروف |
| `HTMLTagFilter` | `HTMLRemover`, `RemoveHTMLTags` | حذف تگ‌های HTML همراه با حفظ محتوا |
| `HashtagFilter` | `HashtagRemover`, `RemoveHashtags` | حذف هشتگ |
| `MentionFilter` | `MentionRemover`, `RemoveMentions` | حذف منشن (@) |

```python
from shekar.preprocessing import EmojiFilter, DiacriticFilter

print(EmojiFilter()("😊🇮🇷سلام گلای تو خونه!🎉🎉🎊🎈"))
print(DiacriticFilter()("مَنْ"))
```

#### ۳) پوشاننده‌ها (Maskers)

| مؤلفه | نام‌های جایگزین | توضیح |
|----------|---------|-------------|
| `EmailMasker` | `MaskEmails` | پوشاندن یا حذف ایمیل |
| `URLMasker` | `MaskURLs` | پوشاندن یا حذف URL |

```python
from shekar.preprocessing import URLMasker

print(URLMasker(mask="")("وب‌سایت ما: https://example.com"))
```

#### ۴) تبدیل‌های کاربردی

| مؤلفه | کاربرد |
| ---------------- | ------- |
| `NGramExtractor` | استخراج n-gram از متن |
| `Flatten` | تخت‌کردن لیست‌های تودرتو |

```python
from shekar.transforms import NGramExtractor, Flatten

ngrams = NGramExtractor(range=(1, 2))("سلام دنیا")
print(ngrams)

nested = [["سلام", "دنیا"], ["خوبی؟", "چطوری؟"]]
print(list(Flatten()(nested)))
```
