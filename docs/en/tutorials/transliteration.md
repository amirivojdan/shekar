# Transliteration

The transliteration module provides bidirectional script conversion between Persian (Farsi) and Tajik scripts. `FarsiToTajik` converts Persian Arabic-script text to Tajik Cyrillic, and `TajikToFarsi` performs the reverse conversion.

**Example Usage**

```python
from shekar import FarsiToTajik, TajikToFarsi

fa = FarsiToTajik()
print(fa("ایران مادر است!"))

tj = TajikToFarsi()
print(tj("Эрон модар аст!"))
```
