from shekar.base import BaseTransform
from shekar.tokenization import AlbertTokenizer, WordTokenizer
from shekar.hub import Hub
from pathlib import Path
import onnxruntime
import numpy as np


class AlbertPOS(BaseTransform):
    def __init__(self, model_path: str | Path = None):
        super().__init__()
        resource_name = "albert_persian_pos_q8.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = onnxruntime.InferenceSession(model_path)
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

    def transform(self, text: str) -> list:
        words = self.word_tokenizer(text)
        tokens = []
        word_ids = []
        for word in words:
            encoded = self.tokenizer.tokenizer.encode(word, add_special_tokens=False)
            tokens.extend(encoded.tokens)
            word_ids.extend([word] * len(encoded.tokens))

        # Convert to IDs
        input_ids = []
        for token in tokens:
            token_id = self.tokenizer.tokenizer.token_to_id(token)
            if token_id is None:
                token_id = self.tokenizer.pad_token_id
            input_ids.append(token_id)

        attention_mask = [1] * len(input_ids)
        # Pad to max length (optional or if needed)
        pad_len = self.tokenizer.model_max_length - len(input_ids)
        input_ids += (
            [self.tokenizer.pad_token_id] * pad_len
        )  # Using self.tokenizer.pad_token_id as the padding token ID for ALBERT
        attention_mask += [0] * pad_len

        inputs = {
            "input_ids": np.array([input_ids], dtype=np.int64),
            "attention_mask": np.array([attention_mask], dtype=np.int64),
        }

        outputs = self.session.run(None, inputs)
        logits = outputs[0]
        logits = logits[0, : len(tokens), :]
        tags_ids = np.argmax(logits, axis=-1)
        tags = [self.id2tag[tag] for tag in tags_ids]

        final_preds = []
        match_words = []
        prev_word = None
        for token, word, pred_tag in zip(tokens, word_ids, tags):
            if word != prev_word:
                final_preds.append(pred_tag)
                match_words.append(word)
                prev_word = word

        return list(zip(match_words, final_preds))
