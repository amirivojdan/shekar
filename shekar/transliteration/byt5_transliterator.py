from pathlib import Path

from shekar.base import BaseTextTransform
from shekar.hub import Hub
from shekar.transliteration.byt5_encoder import ByT5Encoder
from shekar.transliteration.byt5_decoder import ByT5Decoder


class ByT5Transliterator(BaseTextTransform):
    def __init__(
        self,
        encoder_path: str | Path | None = None,
        decoder_path: str | Path | None = None,
        num_beams: int = 1,
        max_new_tokens: int = 256,
    ):
        self._direction = None  # to be set by subclasses

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
