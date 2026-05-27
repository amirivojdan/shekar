# دسته‌بندی متن

ماژول `classification` ابزارهای سطح‌بالا برای دسته‌بندی متن فارسی ارائه می‌دهد که شامل تحلیل احساسات، تشخیص زبان توهین‌آمیز و تشخیص زبان محاوره‌ای است. هر دسته‌بند برچسب پیش‌بینی‌شده را به همراه میزان اطمینان بازمی‌گرداند.

## تحلیل احساسات

`SentimentClassifier` از یک مدل سبک ALBERT که روی مجموعه‌داده اسنپ‌فود تنظیم‌دقیق شده استفاده می‌کند و متن را به عنوان **مثبت** یا **منفی** دسته‌بندی می‌کند.

**نمونهٔ استفاده**

```python
from shekar.classification import SentimentClassifier

sentiment_classifier = SentimentClassifier()

print(sentiment_classifier("سریال قصه‌های مجید عالی بود!"))
print(sentiment_classifier("فیلم ۳۰۰ افتضاح بود!"))
```

```output
('positive', 0.9923112988471985)
('negative', 0.9330866932868958)
```

## تشخیص زبان توهین‌آمیز

`OffensiveLanguageClassifier` از یک طبقه‌بند رگرسیون لجستیک آموزش‌دیده بر ویژگی‌های TF-IDF مستخرج از [مجموعه‌داده ناسزا](https://github.com/amirivojdan/naseza) استفاده می‌کند. این کلاس تعیین می‌کند که آیا متن خنثی است یا توهین‌آمیز و هم برچسب و هم میزان اطمینان را بازمی‌گرداند.

**نمونهٔ استفاده**

```python
from shekar.classification import OffensiveLanguageClassifier

offensive_classifier = OffensiveLanguageClassifier()

print(offensive_classifier("زبان فارسی میهن من است!"))
print(offensive_classifier("تو خیلی احمق و بی‌شرفی!"))
```

```output
('neutral', 0.7651197910308838)
('offensive', 0.7607775330543518)
```

## تشخیص زبان محاوره‌ای

`InformalLanguageClassifier` تشخیص می‌دهد که آیا متن فارسی به سبک محاوره‌ای (غیررسمی) یا رسمی نوشته شده است. این کلاس برای خطوط پیش‌پردازش، نرمال‌سازی آگاه از سبک، و تحلیل جامعه‌شناختی زبان مفید است.

**نمونهٔ استفاده**

```python
from shekar.classification import InformalLanguageClassifier

informal_classifer = InformalLanguageClassifier()
informal_classifer("میرم خونه یکم استراحت کنم.")
```
