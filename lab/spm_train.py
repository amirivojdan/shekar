import sentencepiece as spm

spm.SentencePieceTrainer.train(
    input="./corpus.txt",
    model_prefix="sp_unigram",
    vocab_size=32000,
    model_type="unigram",
    normalization_rule_name="identity",
    character_coverage=1.0,
    byte_fallback=True,
    train_extremely_large_corpus=True,
)
