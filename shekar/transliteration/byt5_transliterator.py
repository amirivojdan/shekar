from collections import defaultdict
from pathlib import Path

import numpy as np

from shekar.base import BaseTextTransform
from shekar.hub import Hub
from shekar.transliteration.byt5_decoder import ByT5Decoder
from shekar.transliteration.byt5_encoder import ByT5Encoder


class ByT5Transliterator(BaseTextTransform):
    supports_batching = True

    def __init__(
        self,
        encoder_path: str | Path | None = None,
        decoder_path: str | Path | None = None,
        num_beams: int = 1,
        max_new_tokens: int = 256,
        *,
        batch_size=32,
    ):
        self.batch_size = self._validate_batch_size(batch_size)
        self._direction = None  # to be set by subclasses
        ByT5Decoder.validate_generation_parameters(num_beams, max_new_tokens)

        if encoder_path is None or not Path(encoder_path).exists():
            encoder_path = Hub.get_resource("byt5_tg2fa_encoder_q8.onnx")
        if decoder_path is None or not Path(decoder_path).exists():
            decoder_path = Hub.get_resource("byt5_tg2fa_decoder_q8.onnx")

        self.encoder = ByT5Encoder(encoder_path)
        self.decoder = ByT5Decoder(decoder_path)
        self.num_beams = num_beams
        self.max_new_tokens = max_new_tokens

    def _function(self, X: str) -> str:
        enc_out, attention_mask = self.encoder.encode(f"{self._direction}: {X.strip()}")
        token_ids = self.decoder.decode(
            enc_out, attention_mask, self.num_beams, self.max_new_tokens
        )
        return self.encoder.tokenizer.detokenize(token_ids)

    def transform(self, X):
        if isinstance(X, str):
            return self._function(X)
        # The existing iterable API returns a generator; retain its laziness.
        return self._iter_transliterations(X)

    def _iter_transliterations(self, texts):
        for batch in self._text_batches(texts, self.batch_size):
            yield from self._transform_batch(batch, self.batch_size)

    def _transform_batch(self, texts, batch_size):
        if not texts:
            return []
        # The legacy encoder dynamically quantizes across all input rows. Even
        # equal-length distinct texts can change each other's output. Encode
        # identical inputs together; batch the expensive decoder independently.
        prefixed = [f"{self._direction}: {text.strip()}" for text in texts]
        groups = defaultdict(list)
        for i, text in enumerate(prefixed):
            groups[text].append(i)
        states, masks = [None] * len(texts), [None] * len(texts)
        for indices in groups.values():
            encoded, attention = self.encoder.encode_batch(
                [prefixed[i] for i in indices]
            )
            for row, document in enumerate(indices):
                states[document] = encoded[row]
                masks[document] = attention[row]
        length = max(len(mask) for mask in masks)
        encoded = np.stack(
            [np.pad(state, ((0, length - len(state)), (0, 0))) for state in states]
        )
        mask = np.stack([np.pad(mask, (0, length - len(mask))) for mask in masks])
        sequences = self.decoder.decode_batch(
            encoded, mask, self.num_beams, self.max_new_tokens
        )
        return [self.encoder.tokenizer.detokenize(ids) for ids in sequences]
