from shekar.transliteration.byt5_transliterator import ByT5Transliterator


class FarsiToTajik(ByT5Transliterator):
    def __init__(
        self,
        encoder_path: str | None = None,
        decoder_path: str | None = None,
        num_beams: int = 1,
        max_new_tokens: int | None = None,
        *,
        batch_size=32,
    ):
        super().__init__(
            encoder_path, decoder_path, num_beams, max_new_tokens, batch_size=batch_size
        )
        self._direction = "fa2tg"
