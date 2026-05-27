# Classification

The `classification` module provides high-level text classification utilities for Persian, covering sentiment analysis, offensive language detection, and informal language classification through a unified and consistent interface. Each classifier returns a predicted label along with a confidence score.

## Sentiment Analysis

The `SentimentClassifier` uses a lightweight ALBERT model fine-tuned on the Snapfood dataset to classify text as **positive** or **negative**.

**Example Usage**

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

## Toxicity Detection

The `OffensiveLanguageClassifier` uses a Logistic Regression classifier trained on TF-IDF features extracted from the [Naseza (ناسزا) dataset](https://github.com/amirivojdan/naseza). It determines whether text is neutral or offensive, returning both the predicted label and its confidence score.

**Example Usage**

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

## Informal Language Classification

The `InformalLanguageClassifier` detects whether Persian text is written in an informal (colloquial) or formal style. This is useful for preprocessing pipelines, style-aware normalization, and sociolinguistic analysis.

**Example Usage**

```python
from shekar.classification import InformalLanguageClassifier

informal_classifer = InformalLanguageClassifier()
informal_classifer("میرم خونه یکم استراحت کنم.")
```
