from pathlib import Path
from typing import ClassVar

import numpy as np

from shekar.base import BaseTransform
from shekar.hub import resolve_model_path
from shekar.tokenization import AlbertTokenizer, WordTokenizer
from shekar.utils import create_onnx_session


class AlbertDepParser(BaseTransform):
    supports_batching = True

    dep_relations: ClassVar[list[str]] = [
        "acl",
        "advcl",
        "advmod",
        "amod",
        "appos",
        "aux",
        "case",
        "cc",
        "ccomp",
        "compound",
        "compound:lvc",
        "conj",
        "cop",
        "csubj",
        "dep",
        "det",
        "fixed",
        "flat:name",
        "flat:num",
        "goeswith",
        "iobj",
        "mark",
        "nmod",
        "nsubj",
        "nsubj:pass",
        "nummod",
        "obj",
        "obl",
        "obl:arg",
        "parataxis",
        "punct",
        "root",
        "vocative",
        "xcomp",
    ]
    id2deprel: ClassVar[dict[int, str]] = dict(enumerate(dep_relations))

    def __init__(self, model_path: str | Path | None = None, *, batch_size=32):
        super().__init__()
        self.batch_size = self._validate_batch_size(batch_size)
        resource_name = "albert_persian_dep_parser_q8.onnx"
        model_path = resolve_model_path(model_path, resource_name)

        self.session = create_onnx_session(model_path)
        self._session_batch_size(self.session, self.batch_size)
        self.tokenizer = AlbertTokenizer()
        self.word_tokenizer = WordTokenizer()

    def _build_inputs(self, words: list[str]):
        """Tokenize words and build ONNX-ready arrays.

        Returns:
            input_ids:              np.int64 (1, seq_len)
            attention_mask:         np.int64 (1, seq_len)
            word_to_first_subtoken: np.int64 (1, num_words)
        """
        all_ids = [self.tokenizer.cls_token_id]
        word_to_first_subtoken = []

        for word in words:
            sub_ids = self.tokenizer.sp.encode(word, out_type=int)
            if not sub_ids:
                sub_ids = [self.tokenizer.unk_token_id]
            word_to_first_subtoken.append(len(all_ids))
            all_ids.extend(sub_ids)

        all_ids.append(self.tokenizer.sep_token_id)

        if len(all_ids) > self.tokenizer.model_max_length:
            raise ValueError(
                "Dependency parsing input exceeds the model token limit; "
                "split the text into shorter sentences before parsing."
            )

        attention_mask = [1] * len(all_ids)
        pad_len = self.tokenizer.model_max_length - len(all_ids)
        all_ids += [self.tokenizer.pad_token_id] * pad_len
        attention_mask += [0] * pad_len

        return (
            np.array([all_ids], dtype=np.int64),
            np.array([attention_mask], dtype=np.int64),
            np.array([word_to_first_subtoken], dtype=np.int64),
        )

    def transform(self, text):
        if not isinstance(text, str):
            return self.transform_batch(text)
        return self._transform_batch([text], self.batch_size)[0]

    def _transform_batch(self, texts, batch_size):
        size = self._session_batch_size(self.session, batch_size)
        words = [list(self.word_tokenizer(text)) for text in texts]
        results = [[] for _ in texts]
        nonempty = [(i, self._build_inputs(ws)) for i, ws in enumerate(words) if ws]
        for start in range(0, len(nonempty), size):
            batch = nonempty[start : start + size]
            count = max(len(words[i]) for i, _ in batch)
            inputs = {
                "input_ids": np.concatenate([arrays[0] for _, arrays in batch]),
                "attention_mask": np.concatenate([arrays[1] for _, arrays in batch]),
                "word_to_first_subtoken": np.concatenate(
                    [
                        np.pad(arrays[2], ((0, 0), (0, count - arrays[2].shape[1])))
                        for _, arrays in batch
                    ]
                ),
            }
            arcs, relations = self.session.run(None, inputs)
            for row, (document, _) in enumerate(batch):
                n = len(words[document])
                for i, word in enumerate(words[document]):
                    head = int(arcs[row, i + 1, : n + 1].argmax())
                    relation = int(relations[row, i + 1, head].argmax())
                    results[document].append((word, head, self.id2deprel[relation]))
        return results
