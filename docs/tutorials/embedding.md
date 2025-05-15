# Word Embeddings

Word embeddings are dense vector representations of words in a continuous space. They capture semantic relationships between words—placing similar words closer together—which enables machine learning models to better understand meaning, perform clustering, and analyze textual similarity.

## Embedder Class

The `Embedder` class provides a simple interface for loading and using pre-trained word embeddings. It currently supports FastText models and allows you to retrieve word vectors or find semantically similar words.

### Available Models

The following pre-trained models are available:

- `fasttext-d300-w5-cbow-naab`: Trained on the Naab corpus with 300-dimensional vectors.
- `fasttext-d100-w10-cbow-blogs`: Trained on Persian blog data with 100-dimensional vectors.

### Initialization

To load a specific model:

```python
from shekar import Embedder

embedder = Embedder(model_name="fasttext-d100-w10-cbow-blogs")
```

### Usage

#### 1. Retrieve Word Vector

```python
vector = embedder["کتاب"]
print(vector)  # Output: NumPy array representing the word vector
```

#### 2. Find Similar Words

```python
similar_words = embedder.most_similar("کتاب", topn=5)
print(similar_words)
```

## Best Practices

- Use pre-trained embeddings to improve model performance and generalization.
- Load the **`Embedder`** once and reuse it to avoid repeated I/O overhead.
- Ensure models are downloaded and extracted before use.
- Handle out-of-vocabulary (OOV) words gracefully—FastText supports subword features for this purpose.
- Choose model dimensions based on the trade-off between performance and memory usage.

## Common Issues and Solutions

| Issue                        | Solution                                                                 |
|-----------------------------|--------------------------------------------------------------------------|
| **Model not found**         | Check that the model name exists in `available_models`.                  |
| **Download failure**        | Verify internet connection and retry.                                   |
| **OOV word access**         | Use subword-based models like FastText, or expand your training corpus. |
| **High memory consumption** | Opt for lower-dimensional vectors.                                       |
| **Encoding errors**         | Make sure input text is UTF-8 encoded.                                   |

---

By using the **`Embedder`** class, you can seamlessly integrate rich semantic representations into your Persian NLP pipeline, improving downstream tasks like classification, clustering, and semantic analysis.