# Pipeline

The `Pipeline` class in the `shekar` library enables you to chain together multiple preprocessing steps into a single, reusable transformation flow. It is particularly useful when you want to apply several text normalization, cleaning, or masking operations in sequence. The `Pipeline` is fully compatible with all preprocessors in `shekar.preprocessing`.

## Key Features

-   **Composable**: Chain multiple transformations in a defined order.
-   **Operator Chaining**: Use the | operator for a clean, functional style.
-   **Flexible Input**: Works with single strings or batches of strings.
-   **Callable**: The pipeline object itself is callable.
-   **Decorator Support**: Apply preprocessing automatically to specific function arguments.
-   **Error Handling**: Raises clear errors for invalid inputs or configuration.

## Initialization

You can create a pipeline in two ways:

1. Using the `Pipeline` class directly
   
```python
from shekar import Pipeline
from shekar.preprocessing import EmojiRemover, PunctuationRemover

steps = [
    ("removeEmoji", EmojiRemover()),
    ("removePunct", PunctuationRemover()),
]

pipeline = Pipeline(steps)
```

2. Using the `|` operator for cleaner chaining

```python
from shekar.preprocessing import AlphabetNormalizer, SpacingNormalizer, StopWordFilter

pipeline = AlphabetNormalizer() | SpacingNormalizer() | StopWordFilter()
```

Both approaches produce identical pipelines. The `|` operator is ideal for quick and readable pipeline definitions.

## Basic Usage

Apply the pipeline to a string:

```python
text = "پرنده‌های 🐔 قفسی، عادت دارن به بی‌کسی!"
result = pipeline.fit_transform(text)
print(result)  # Output: "پرنده‌های  قفسی عادت دارن به بی‌کسی"
```

## Batch Processing

You can pass a list of strings:

```python
texts = [
    "یادته گل رز قرمز 🌹 به تو دادم؟",
    "بگو یهویی از کجا پیدات شد؟"
]
results = pipeline.fit_transform(texts)
print(results)
# Output: ["یادته گل رز قرمز  به تو دادم", "بگو یهویی از کجا پیدات شد"]
```

## Callable Interface

The **`Pipeline`** object is callable and equivalent to **`fit_transform()`**:

```python
output = pipeline("تو را من چشم👀 در راهم!")
print(output)  # Output: "تو را من چشم در راهم"
```

## Using with Decorators

Apply the pipeline automatically to specific function arguments:

```python
@pipeline.on_args("text")
def process_text(text):
    return text

print(process_text("عمری دگر بباید بعد از وفات ما را!🌞"))
# Output: "عمری دگر بباید بعد از وفات ما را"
```

Multiple arguments:

```python
@pipeline.on_args(["text", "description"])
def clean_inputs(text, description):
    return text, description

print(clean_inputs("ناز داره چو وای!", "مهرهٔ مار داره تو دلبری❤️"))
# Output: ("ناز داره چو وای", "مهرهٔ مار داره تو دلبری")
```

## Error Handling

The pipeline raises informative errors for invalid usage:

- `ValueError`: Raised if input is neither a string nor a list of strings.
- `TypeError`: Raised if `on_args` is called with invalid types.
- `ValueError`: Raised if the specified function argument does not exist.

## Notes

- Each preprocessor must implement `__call__` and `fit_transform`.
- Pipelines are compatible with **`Normalizer`**, which itself is a subclass of **`Pipeline`**.
- Ideal for building modular, testable, and reusable text processing flows.

---

The **`Pipeline`** class provides a clean and extensible architecture for combining multiple preprocessing steps, making it a powerful component for building robust NLP workflows.