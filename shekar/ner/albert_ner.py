from pathlib import Path

from shekar.base import BaseTransform
from shekar.hub import resolve_model_path
from shekar.tokenization import AlbertTokenizer
from shekar.utils import create_onnx_session


class AlbertNER(BaseTransform):
    supports_batching = True

    def __init__(self, model_path: str | Path | None = None, *, batch_size=32):
        super().__init__()
        self.batch_size = self._validate_batch_size(batch_size)
        resource_name = "albert_persian_ner_q8.onnx"
        model_path = resolve_model_path(model_path, resource_name)

        self.session = create_onnx_session(model_path)
        self._session_batch_size(self.session, self.batch_size)
        self.tokenizer = AlbertTokenizer(
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
        return self._transform_batch([X], self.batch_size)[0]

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
        # Pad each batch only to its longest row instead of model_max_length.
        for inputs, owners in AlbertTokenizer._encoded_batches(
            encoded, size, self.tokenizer.pad_token_id, trim_padding=True
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
