from pathlib import Path

import numpy as np

from shekar.base import BaseTransform
from shekar.hub import Hub
from shekar.tokenization import AlbertTokenizer
from shekar.utils import create_onnx_session


class AlbertNER(BaseTransform):
    supports_batching = True

    def __init__(self, model_path: str | Path | None = None, *, batch_size=32):
        super().__init__()
        self.batch_size = self._validate_batch_size(batch_size)
        resource_name = "albert_persian_ner_q8.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = create_onnx_session(model_path)
        self._session_batch_size(self.session, self.batch_size)
        self.tokenizer = AlbertTokenizer(
            enable_padding=True,
            enable_truncation=True,
            return_overflowing_tokens=True,
        )

        self.id2tag = {
            0: "B-DAT",
            1: "B-EVE",
            2: "B-LOC",
            3: "B-ORG",
            4: "B-PER",
            5: "I-DAT",
            6: "I-EVE",
            7: "I-LOC",
            8: "I-ORG",
            9: "I-PER",
            10: "O",
        }

    def _aggregate_entities(self, tokens, predicted_tag_ids):
        entities = []
        current_entity = ""
        current_label = None

        for token, tag_id in zip(tokens, predicted_tag_ids):
            label = self.id2tag[tag_id]

            if token in ["[CLS]", "[SEP]"]:
                continue

            is_new_word = token.startswith("▁")
            clean_token = token.lstrip("▁")

            if clean_token == "‌":
                if current_entity:
                    current_entity = current_entity.rstrip() + "\u200c"
                continue

            if label.startswith("B-"):
                if current_entity:
                    entities.append((current_entity.strip(), current_label))
                current_entity = clean_token
                current_label = label[2:]
            elif label.startswith("I-") and current_label == label[2:]:
                if current_entity.endswith("\u200c"):
                    current_entity += clean_token
                elif is_new_word:
                    current_entity += " " + clean_token
                else:
                    current_entity += clean_token
            else:
                if current_entity:
                    entities.append((current_entity.strip(), current_label))
                    current_entity = ""
                    current_label = None

        if current_entity:
            entities.append((current_entity.strip(), current_label))

        return entities

    def transform(self, X: str) -> list:
        """
        NER tag a possibly long input by running ONNX over tokenizer chunks
        and stitching predictions back into a single sequence.

        Returns:
            entities: list produced by self._aggregate_entities over the full text
        """

        if not isinstance(X, str):
            return self.transform_batch(X)
        batched = self.tokenizer(X)  # dict with (num_chunks, L) arrays
        input_ids = batched["input_ids"]  # (B, L)
        attention_mask = batched["attention_mask"]  # (B, L)

        onnx_input_names = {i.name for i in self.session.get_inputs()}
        feed = {k: v for k, v in batched.items() if k in onnx_input_names}

        size = self._session_batch_size(self.session, self.batch_size)
        logits = np.concatenate(
            [
                self.session.run(
                    None,
                    {k: v[start : start + size] for k, v in feed.items()},
                )[0]
                for start in range(0, len(input_ids), size)
            ]
        )  # (B, L, num_tags)
        pred_ids = np.argmax(logits, axis=-1)  # (B, L)

        special_names = ["<pad>", "[PAD]", "[CLS]", "[SEP]", "<cls>", "<sep>"]
        special_ids = {self.tokenizer.tokenizer.token_to_id(n) for n in special_names}
        special_ids = {i for i in special_ids if i is not None}

        stride = getattr(self.tokenizer, "stride", 0)
        B, L = input_ids.shape

        tokens_all: list[str] = []
        tags_all: list[int] = []

        for b in range(B):
            ids = input_ids[b]
            mask = attention_mask[b].astype(bool)

            valid_pos = [
                i for i in range(L) if mask[i] and int(ids[i]) not in special_ids
            ]

            if b > 0 and stride > 0:
                valid_pos = valid_pos[stride:]

            if not valid_pos:
                continue

            toks = [
                self.tokenizer.tokenizer.id_to_token(int(ids[i])) for i in valid_pos
            ]
            tags = pred_ids[b, valid_pos].tolist()

            tokens_all.extend(toks)
            tags_all.extend(tags)

        entities = self._aggregate_entities(
            tokens_all, np.asarray(tags_all, dtype=pred_ids.dtype)
        )
        return entities

    def _transform_batch(self, texts, batch_size):
        size = self._session_batch_size(self.session, batch_size)
        tokens_by_document = [[] for _ in texts]
        tags_by_document = [[] for _ in texts]
        input_names = {item.name for item in self.session.get_inputs()}
        special_ids = {
            self.tokenizer.pad_token_id,
            self.tokenizer.cls_token_id,
            self.tokenizer.sep_token_id,
        }
        encoded = (self.tokenizer(text) for text in texts)
        for inputs, owners in AlbertTokenizer._encoded_batches(
            encoded, size, self.tokenizer.pad_token_id
        ):
            predictions = self.session.run(
                None, {k: v for k, v in inputs.items() if k in input_names}
            )[0].argmax(axis=-1)
            for row, (document, chunk, _) in enumerate(owners):
                positions = [
                    i
                    for i, token in enumerate(inputs["input_ids"][row])
                    if inputs["attention_mask"][row, i]
                    and int(token) not in special_ids
                ]
                if chunk:
                    positions = positions[self.tokenizer.stride :]
                tokens_by_document[document].extend(
                    self.tokenizer.id_to_token(int(inputs["input_ids"][row, i]))
                    for i in positions
                )
                tags_by_document[document].extend(predictions[row, positions].tolist())
        return [
            self._aggregate_entities(tokens, tags)
            for tokens, tags in zip(tokens_by_document, tags_by_document)
        ]
