# Text Augmentation

The `transforms.noise` module provides noise-based data augmentation operators for Persian text. These are useful for training robust NLP models by simulating real-world text corruption such as OCR errors, keyboard typos, and irregular whitespace.

| Operator | Description |
|---|---|
| `KeyboardNoise` | Replaces characters with visually or positionally adjacent keys on a Persian keyboard layout |
| `OCRNoise` | Substitutes characters with visually similar ones to simulate OCR scanning errors |
| `WhitespaceNoise` | Randomly inserts, removes, or alters whitespace between words and subwords |

**Example Usage**

```python
from shekar import WhitespaceNoise, OCRNoise, KeyboardNoise

text = "عمری دگر بباید بعد از وفات ما را"

keyboard_noise = KeyboardNoise()
print(keyboard_noise(text))

ocr_noise = OCRNoise()
print(ocr_noise(text))

white_noise = WhitespaceNoise()
print(white_noise(text))
```

```output
عمریی دگر بباید بعد از وفات ما را
عمری ذگر بباید بعد از وفات ما را
عمری‌دگر بباید‌بعد‌از وفاتما را
```

!!! note
    The output of each operator is stochastic, results will vary between runs. Use a fixed random seed during experiments to ensure reproducibility.
