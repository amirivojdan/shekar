from shekar.transliteration.byt5_transliterator import ByT5Transliterator


class FarsiToTajik(ByT5Transliterator):
    def __init__(
        self,
        encoder_path: str | None = None,
        decoder_path: str | None = None,
        num_beams: int = 4,
        max_new_tokens: int = 256,
    ):
        super().__init__(encoder_path, decoder_path, num_beams, max_new_tokens)
        self._direction = "fa2tg"
