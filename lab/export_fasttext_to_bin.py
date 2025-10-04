from gensim.models import FastText
import pickle
import numpy as np

model = FastText.load("fasttext_d300_w10_v250k_cbow_naab.model")

embedding = model.wv["سلام"]
print(embedding)


similarity = model.wv.similarity("سلام", "درود")
print(f"Similarity between 'سلام' and 'درود': {similarity}")

top_similar = model.wv.most_similar("سلام", topn=5)
print("Top 5 most similar words to 'سلام':")
for word, score in top_similar:
    print(f"{word}: {score}")

words = np.array(list(model.wv.index_to_key))
embeddings = np.array([model.wv[word] for word in words])

model_export = {
    "words": words,
    "embeddings": embeddings,
    "vector_size": model.vector_size,
    "window": model.window,
    "model": "fasttext-" + ("cbow" if model.sg == 0 else "skipgram"),
    "epochs": model.epochs,
    "dataset": "SLPL/naab"
}

with open("fasttext_d300_w10_v250k_cbow_naab.bin", "wb") as f:
    pickle.dump(model_export, f)

with open("fasttext_d300_w10_v250k_cbow_naab.bin", "rb") as f:
    loaded_model_export = pickle.load(f)
    new_embedding = loaded_model_export["embeddings"][np.where(loaded_model_export["words"] == "سلام")[0][0]]

if np.array_equal(embedding, new_embedding):
    print("The embeddings match!")
else:
    print("The embeddings do not match.")