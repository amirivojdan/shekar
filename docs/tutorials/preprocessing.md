# Preprocessing

[![Notebook](https://img.shields.io/badge/Notebook-Jupyter-00A693.svg)](examples/preprocessing.ipynb)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amirivojdan/shekar/blob/main/examples/preprocessing.ipynb)

The `shekar.preprocessing` module offers a suite of tools designed to clean and standardize Persian (and mixed) text for NLP tasks. These tools include removers, normalizers, and maskers. Below is a detailed guide to each class.

---

## 1. `SpacingStandardizer`
**Purpose:** Cleans extra spaces and newlines, and fixes spacing around punctuation and ZWNJ.

```python
from shekar.preprocessing import SpacingStandardizer

text = "   این یک   متن   تستی   است. "
standardizer = SpacingStandardizer()
print(standardizer(text))  # Output: "این یک متن تستی است."
```

---

## 2. `AlphabetNormalizer`
**Purpose:** Unifies variant or Arabic forms of Persian characters (e.g., "ۀ" to "ه").

```python
from shekar.preprocessing import AlphabetNormalizer

text = "نشان‌دهندة سایة"
normalizer = AlphabetNormalizer()
print(normalizer(text))  # Output: "نشان‌دهنده سایه"
```

---

## 3. `NumericNormalizer`
**Purpose:** Converts English, Arabic, and circled numerals into Persian digits.

```python
from shekar.preprocessing import NumericNormalizer

text = "٠١٢٣ ⒈ 1"
normalizer = NumericNormalizer()
print(normalizer(text))  # Output: "۰۱۲۳ ۱ ۱"
```

---

## 4. `PunctuationNormalizer`
**Purpose:** Converts various forms of punctuation to their Persian equivalents.

```python
from shekar.preprocessing import PunctuationNormalizer

text = "؟?،٬!%:؛"
normalizer = PunctuationNormalizer()
print(normalizer(text))  # Output: "؟؟،،!٪:؛"
```

---

## 5. `EmojiRemover`
**Purpose:** Removes all emoji characters from the text.

```python
from shekar.preprocessing import EmojiRemover

text = "سلام 😊🌹🎉"
remover = EmojiRemover()
print(remover(text))  # Output: "سلام"
```

---

## 6. `EmailMasker`
**Purpose:** Masks or removes email addresses.

```python
from shekar.preprocessing import EmailMasker

text = "تماس با ما: test@example.com"
masker = EmailMasker(mask="")
print(masker(text))  # Output: "تماس با ما: "
```

---

## 7. `URLMasker`
**Purpose:** Masks or removes URLs.

```python
from shekar.preprocessing import URLMasker

text = "وب‌سایت ما: https://example.com"
masker = URLMasker(mask="")
print(masker(text))  # Output: "وب‌سایت ما: "
```

---

## 8. `DiacriticsRemover`
**Purpose:** Removes diacritical marks (e.g., َ ,ِ ,ُ ) from Persian/Arabic text.

```python
from shekar.preprocessing import DiacriticsRemover

text = "کُجا نِشانِ قَدَم"
remover = DiacriticsRemover()
print(remover(text))  # Output: "کجا نشان قدم"
```

---

## 9. `PunctuationRemover`
**Purpose:** Removes all punctuation symbols.

```python
from shekar.preprocessing import PunctuationRemover

text = "سلام، دنیا!"
remover = PunctuationRemover()
print(remover(text))  # Output: "سلام دنیا"
```

---

## 10. `RedundantCharacterRemover`
**Purpose:** Reduces sequences of repeated characters (like stretched letters).

```python
from shekar.preprocessing import RedundantCharacterRemover

text = "سلاممممممممم"
remover = RedundantCharacterRemover()
print(remover(text))  # Output: "سلامم"
```

---

## 11. `ArabicUnicodeNormalizer`
**Purpose:** Converts Arabic presentation forms and symbols into Persian equivalents or full phrases.

```python
from shekar.preprocessing import ArabicUnicodeNormalizer

text = "﷽ پنجاه هزار ﷼"
normalizer = ArabicUnicodeNormalizer()
print(normalizer(text))  # Output: "بسم الله الرحمن الرحیم پنجاه هزار ریال"
```

---

## 12. `StopwordRemover`
**Purpose:** Removes common Persian stopwords (e.g., "این", "است", "به").

```python
from shekar.preprocessing import StopwordRemover

text = "این یک جملهٔ نمونه است"
remover = StopwordRemover()
print(remover(text))  # Output: "جملهٔ نمونه"
```

---

## 13. `NonPersianRemover`
**Purpose:** Removes all non-Persian characters (can keep English/diacritics if configured).

```python
from shekar.preprocessing import NonPersianRemover

text = "This is یک متن ترکیبی!"
remover = NonPersianRemover()
print(remover(text))  # Output: " یک متن ترکیبی!"
```

**With English support:**
```python
remover = NonPersianRemover(keep_english=True)
print(remover("Test در کنار تست"))  # Output: "Test در کنار تست"
```

---

## 14. `HTMLTagRemover`
**Purpose:** Removes HTML tags while keeping the content.

```python
from shekar.preprocessing import HTMLTagRemover

text = "<p>سلام دنیا</p>"
remover = HTMLTagRemover()
print(remover(text))  # Output: "سلام دنیا"
```

---

## Notes on Usage

- All preprocessors implement `__call__` and `fit_transform()` for pipeline compatibility.
- You can pass a single string or an iterable of strings to all classes.
- Raise `ValueError` if input is invalid (e.g., not a string or list of strings).