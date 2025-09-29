from shekar.base import BaseTransform
from shekar.tokenization import AlbertTokenizer
from shekar.hub import Hub
from pathlib import Path
import onnxruntime
import numpy as np
from shekar.utils import get_onnx_providers


class AlbertNER(BaseTransform):
    def __init__(self, model_path: str | Path = None):
        super().__init__()
        resource_name = "albert_persian_ner_q8.onnx"
        if model_path is None or not Path(model_path).exists():
            model_path = Hub.get_resource(file_name=resource_name)

        self.session = onnxruntime.InferenceSession(
            model_path, providers=get_onnx_providers()
        )
        self.tokenizer = AlbertTokenizer(enable_padding=True, enable_truncation=True)

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

        batched = self.tokenizer(X)  # dict with (num_chunks, L) arrays
        input_ids = batched["input_ids"]  # (B, L)
        attention_mask = batched["attention_mask"]  # (B, L)

        onnx_input_names = {i.name for i in self.session.get_inputs()}
        feed = {k: v for k, v in batched.items() if k in onnx_input_names}

        outputs = self.session.run(None, feed)
        logits = outputs[0]  # (B, L, num_tags)
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
