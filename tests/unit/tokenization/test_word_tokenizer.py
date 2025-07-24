from shekar.tokenization import WordTokenizer


def test_word_tokenizer():
    tokenizer = WordTokenizer()
    text = "چه سیب‌های قشنگی! حیات نشئهٔ تنهایی است."
    expected_output = [
        "چه",
        "سیب‌های",
        "قشنگی",
        "!",
        "حیات",
        "نشئهٔ",
        "تنهایی",
        "است",
        ".",
    ]
    print(tokenizer.tokenize(text))
    assert list(tokenizer.tokenize(text)) == expected_output

    text = "سلام دنیا"
    expected_output = ["سلام", "دنیا"]
    assert list(tokenizer.tokenize(text)) == expected_output

    text = "این یک متن آزمایشی است."
    expected_output = ["این", "یک", "متن", "آزمایشی", "است", "."]
    assert list(tokenizer.tokenize(text)) == expected_output
