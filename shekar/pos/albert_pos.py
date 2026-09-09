from pathlib import Path

import numpy as np

from shekar.base import BaseTransform
from shekar.hub import Hub
from shekar.tokenization import AlbertTokenizer, WordTokenizer
from shekar.utils import create_onnx_session


class AlbertPOS(BaseTransform):
    supports_batching = True

    def __init__(self, model_path: str | Path | None = None, *, batch_size=32):
        super().__init__()
        self.batch_size = self._validate_batch_size(batch_size)
        resource_name = "albert_persian_pos_batch_q8.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = create_onnx_session(model_path)
        self._session_batch_size(self.session, self.batch_size)
        self.tokenizer = AlbertTokenizer()
        self.word_tokenizer = WordTokenizer()

        self.id2tag = {
            0: "ADJ",
            1: "ADP",
            2: "ADV",
            3: "AUX",
            4: "CCONJ",
            5: "DET",
            6: "INTJ",
            7: "NOUN",
            8: "NUM",
            9: "PART",
            10: "PRON",
            11: "PROPN",
            12: "PUNCT",
            13: "SCONJ",
            14: "VERB",
            15: "X",
            16: "_",
        }

    def transform(self, text):
        if not isinstance(text, str):
            return self.transform_batch(text)
        return self._transform_batch([text], self.batch_size)[0]

    def _encode_words(self, words):
        # Training used independently encoded words, without CLS/SEP tokens.
        chunks, ids, alignment = [], [], []
        limit = self.tokenizer.model_max_length
        for index, word in enumerate(words):
            pieces = self.tokenizer.sp.encode(word, out_type=int) or [
                self.tokenizer.unk_token_id
            ]
            if len(pieces) > limit:
                raise ValueError("A single word exceeds the POS model token limit.")
            if ids and len(ids) + len(pieces) > limit:
                chunks.append((ids, alignment))
                ids, alignment = [], []
            alignment.append((index, len(ids)))
            ids.extend(pieces)
        if ids:
            chunks.append((ids, alignment))
        return chunks

    def _transform_batch(self, texts, batch_size):
        size = self._session_batch_size(self.session, batch_size)
        words_by_document = [list(self.word_tokenizer(text)) for text in texts]
        results = [[] for _ in texts]
        encoded, alignments, owners = [], [], []
        for document, words in enumerate(words_by_document):
            for ids, alignment in self._encode_words(words):
                length = self.tokenizer.model_max_length
                mask = [1] * len(ids) + [0] * (length - len(ids))
                ids = ids + [self.tokenizer.pad_token_id] * (length - len(ids))
                encoded.append(
                    {
                        "input_ids": np.array([ids], dtype=np.int64),
                        "attention_mask": np.array([mask], dtype=np.int64),
                    }
                )
                alignments.append(alignment)
                owners.append(document)
        for inputs, rows in AlbertTokenizer._encoded_batches(
            encoded, size, self.tokenizer.pad_token_id, trim_padding=True
        ):
            tags = self.session.run(None, inputs)[0].argmax(axis=-1)
            for row, (encoded_index, _, _) in enumerate(rows):
                document = owners[encoded_index]
                for word_index, position in alignments[encoded_index]:
                    results[document].append(
                        (
                            words_by_document[document][word_index],
                            self.id2tag[int(tags[row, position])],
                        )
                    )
        return results
