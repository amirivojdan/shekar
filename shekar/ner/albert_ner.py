from shekar.base import BaseTransform
from shekar.tokenization import AlbertTokenizer
from shekar.hub import Hub
from pathlib import Path
import onnxruntime
import numpy as np


class AlbertNER(BaseTransform):
    def __init__(self, model_path: str | Path = None):
        super().__init__()
        resource_name = "albert_persian_ner_q8.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = onnxruntime.InferenceSession(model_path)
        self.tokenizer = AlbertTokenizer()

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
        inputs = self.tokenizer.fit_transform(X)
        inputs.pop("token_type_ids", None)
        outputs = self.session.run(None, inputs)
        logits = outputs[0]
        predicted_tag_ids = np.argmax(logits, axis=-1)[0]
        tokens = [
            self.tokenizer.tokenizer.id_to_token(id) for id in inputs["input_ids"][0]
        ]
        entities = self._aggregate_entities(tokens, predicted_tag_ids)
        return entities
