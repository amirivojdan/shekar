from shekar.base import BaseTransform
from shekar.tokenization import AlbertTokenizer, WordTokenizer
from shekar.hub import Hub
from pathlib import Path
import onnxruntime
import numpy as np
from shekar.utils import get_onnx_providers


class AlbertDepParser(BaseTransform):
    dep_relations = [
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
    id2deprel = {i: rel for i, rel in enumerate(dep_relations)}

    def __init__(self, model_path: str | Path = None):
        super().__init__()
        resource_name = "albert_persian_dep_parser_q8.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = onnxruntime.InferenceSession(
            model_path, providers=get_onnx_providers()
        )
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
            all_ids = all_ids[: self.tokenizer.model_max_length - 1] + [
                self.tokenizer.sep_token_id
            ]

        attention_mask = [1] * len(all_ids)
        pad_len = self.tokenizer.model_max_length - len(all_ids)
        all_ids += [self.tokenizer.pad_token_id] * pad_len
        attention_mask += [0] * pad_len

        return (
            np.array([all_ids], dtype=np.int64),
            np.array([attention_mask], dtype=np.int64),
            np.array([word_to_first_subtoken], dtype=np.int64),
        )

    def transform(self, text: str) -> list[tuple[str, int, str]]:
        """Parse a Persian text string.

        Returns:
            list of (word, head, deprel) where head is 1-indexed (0 = ROOT).
        """
        words = list(self.word_tokenizer(text))
        n = len(words)
        if n == 0:
            return []

        input_ids, attention_mask, word_to_first_subtoken = self._build_inputs(words)

        arc_logits, rel_logits = self.session.run(
            None,
            {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "word_to_first_subtoken": word_to_first_subtoken,
            },
        )
        # arc_logits: (1, n+1, n+1)
        # rel_logits: (1, n+1, n+1, num_deprels)

        results = []
        for i in range(n):
            dep_pos = i + 1
            pred_head = int(arc_logits[0, dep_pos, : n + 1].argmax())
            pred_deprel = int(rel_logits[0, dep_pos, pred_head].argmax())
            results.append((words[i], pred_head, self.id2deprel[pred_deprel]))

        return results
