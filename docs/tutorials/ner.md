# Named Entity Recognition (NER)

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/ner.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/ner.ipynb)


The `NER` module in **Shekar** provides a fast and quantized Named Entity Recognition pipeline powered by a fine-tuned ALBERT model (**default**) exported to ONNX format for efficient inference.

It automatically identifies common Persian entities such as persons, locations, organizations, dates, and events. The NER pipeline is designed for speed and easy integration with other preprocessing components like normalization and tokenization.


**Example usage**:

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

## Entity Tags

The following table summarizes the entity types used by the model (aggregating B- and I- tags):

| Tag     | Description                              |
| ------- | ---------------------------------------- |
| **PER** | Person names                             |
| **LOC** | Locations (cities, countries, landmarks) |
| **ORG** | Organizations (companies, institutions)  |
| **DAT** | Dates and temporal expressions           |
| **EVE** | Events (festivals, historical events)    |
| **O**   | Outside (non-entity text)                |

## Chaining with Pipelines

You can seamlessly chain `NER` with other components using the `|` operator:

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

This chaining enables clean and readable code, letting you build custom NLP flows with preprocessing and tagging in one pass.