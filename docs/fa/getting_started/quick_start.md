# راهنمای شروع سریع

به **Shekar** خوش آمدید؛ یک کتابخانهٔ پایتون برای پردازش زبان طبیعی فارسی. در این راهنما با مهم‌ترین بخش‌ها به‌صورت سریع آشنا می‌شوید: پیش‌پردازش، توکن‌سازی، خط لوله‌ها، نرمال‌سازی و بازنمایی‌ها.

---

## ۱) نرمال‌سازی متن

کلاس داخلی `Normalizer` یک خط لولهٔ آماده ارائه می‌دهد که رایج‌ترین مراحل فیلتر و نرمال‌سازی را ترکیب می‌کند و برای اغلب کاربردها مناسب است.

```python
from shekar import Normalizer

normalizer = Normalizer()
text = "«فارسی شِکَر است» نام داستان ڪوتاه طنز    آمێزی از محمد علی جمالــــــــزاده  می   باشد که در سال 1921 منتشر  شده است و آغاز   ڱر تحول بزرگی در ادَبێات معاصر ایران 🇮🇷 بۃ شمار میرود."

print(normalizer(text))
```

```shell
«فارسی شکر است» نام داستان کوتاه طنزآمیزی از محمد‌علی جمالزاده می‌باشد که در سال ۱۹۲۱ منتشر شده‌است و آغازگر تحول بزرگی در ادبیات معاصر ایران به شمار می‌رود.
```

---

## ۲) استفاده از مؤلفه‌های پیش‌پردازش

می‌توانید پاک‌سازهای مستقل مانند `EmojiRemover`، `DiacriticsRemover` یا `URLMasker` را جداگانه استفاده کنید.

```python
from shekar.preprocessing import EmojiRemover

text = "سلام 🌹😊"
print(EmojiRemover()(text))  # خروجی: "سلام"
```

فهرست کامل مؤلفه‌ها در `shekar.preprocessing` موجود است.

---

## ۳) ساخت خط لولهٔ سفارشی

می‌توانید با زنجیره‌کردن مراحل مختلف، خط لولهٔ مخصوص خود را بسازید:

```python
from shekar import Pipeline
from shekar.preprocessing import EmojiRemover, PunctuationRemover

pipeline = Pipeline([
    ("emoji", EmojiRemover()),
    ("punct", PunctuationRemover())
])

text = "پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!"
print(pipeline(text))  # خروجی: "پرنده‌های  قفسی عادت دارن به بی‌کسی"
```

پشتیبانی می‌شود:
- رشتهٔ تکی یا ورودی دسته‌ای
- دکوراتور تابع برای پاک‌سازی خودکار آرگومان‌ها

---

## ۴) توکن‌سازی جمله

برای شکستن متن به جمله‌ها از `SentenceTokenizer` استفاده کنید:

```python
from shekar import SentenceTokenizer

text = "هدف ما کمک به یکدیگر است! ما می‌توانیم با هم کار کنیم."
sentences = SentenceTokenizer()(text)

for s in sentences:
    print(s)
```
