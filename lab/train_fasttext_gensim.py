from pprint import pprint as print
from gensim.models.fasttext import FastText
import multiprocessing
from shekar import Normalizer
from shekar.tokenization import WordTokenizer, SentenceTokenizer
from datasets import load_dataset

hf_dataset = "SLPL/naab"

class DatasetIter:
    def __init__(self, hf_dataset):
        
        self.word_tokenizer = WordTokenizer()
        self.sentence_tokenizer = SentenceTokenizer()
        self.normalizer = Normalizer()
        self.dataset = load_dataset(hf_dataset, split="train")

    def __iter__(self):
        for example in self.dataset:
            text = self.normalizer(example["text"])
            sentences = self.sentence_tokenizer(text)
            for sentence in sentences:
                words = self.word_tokenizer(sentence)
                yield [word for word in words]

dataset_iter = DatasetIter(hf_dataset)

cpu_count = multiprocessing.cpu_count()
print(f"CPU count: {cpu_count}")

d=300
w=10
vs=250
ds= hf_dataset.split("/")[-1]
model_type = "cbow"

model = FastText(vector_size=d,
                  window=w,
                  sorted_vocab=1,
                  max_final_vocab=vs*1000,
                  workers=cpu_count-10,
                  sg=0 if model_type == "cbow" else 1,
                  epochs=3)

model.build_vocab(corpus_iterable=dataset_iter, progress_per=10000)
print(f"Vocabulary size: {len(model.wv)}")

model.train(corpus_iterable=dataset_iter, total_examples=model.corpus_count, epochs=model.epochs)
model.save(f"fasttext_d{d}_w{w}_v{vs}k_{model_type}_{ds}.model")