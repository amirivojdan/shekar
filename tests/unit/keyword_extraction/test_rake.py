from shekar.keyword_extraction.rake import RAKE


def test_rake_instantiates_with_defaults():
    extractor = RAKE()
    assert extractor.top_n == 5
    assert callable(extractor.transform)


def test_rake_fit_returns_self():
    rake = RAKE()
    result = rake.fit(["نمونه متن برای آزمایش"])
    assert result is rake


def test_rake_extract_keywords_basic():
    rake = RAKE(top_n=5)
    text = "هوش مصنوعی یکی از مهم‌ترین فناوری‌های قرن حاضر است. یادگیری ماشین نیز زیرمجموعه‌ای از آن محسوب می‌شود."

    keywords = rake.transform(text)

    assert isinstance(keywords, list)
    assert len(keywords) <= 5
    assert all(isinstance(kw, str) for kw in keywords)
    assert all(len(kw) > 0 for kw in keywords)


def test_rake_top_n_limit():
    rake = RAKE(top_n=2)
    text = "مهندسی، ریاضی و فیزیک از پایه‌های اصلی علوم پایه هستند."

    keywords = rake.transform(text)

    assert isinstance(keywords, list)
    assert len(keywords) <= 2


def test_rake_handles_empty_text_gracefully():
    rake = RAKE()
    keywords = rake.transform("")
    assert isinstance(keywords, list)
    assert keywords == []
