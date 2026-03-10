from shekar.keyword_extraction.textrank import TextRank


def test_textrank_instantiates_with_defaults():
    extractor = TextRank()
    assert extractor.top_n == 5
    assert extractor.window == 2
    assert extractor.damping == 0.85
    assert extractor.iterations == 30
    assert extractor.max_length == 3
    assert callable(extractor.transform)


def test_textrank_fit_returns_self():
    tr = TextRank()
    result = tr.fit(["نمونه متن برای آزمایش"])
    assert result is tr


def test_textrank_extract_keywords_basic():
    tr = TextRank(top_n=5)
    text = "هوش مصنوعی یکی از مهم‌ترین فناوری‌های قرن حاضر است. یادگیری ماشین نیز زیرمجموعه‌ای از آن محسوب می‌شود."

    keywords = tr.transform(text)

    assert isinstance(keywords, list)
    assert len(keywords) <= 5
    assert all(isinstance(kw, str) for kw in keywords)
    assert all(len(kw) > 0 for kw in keywords)


def test_textrank_top_n_limit():
    tr = TextRank(top_n=2)
    text = "مهندسی نرم‌افزار، هوش مصنوعی و یادگیری ماشین از مهم‌ترین حوزه‌های علوم کامپیوتر هستند."

    keywords = tr.transform(text)

    assert isinstance(keywords, list)
    assert len(keywords) <= 2


def test_textrank_handles_empty_text():
    tr = TextRank()
    keywords = tr.transform("")
    assert isinstance(keywords, list)
    assert keywords == []


def test_textrank_returns_unique_keywords():
    tr = TextRank(top_n=5)
    text = "پردازش زبان طبیعی یک حوزه مهم در هوش مصنوعی است. پردازش زبان طبیعی کاربردهای فراوانی دارد."

    keywords = tr.transform(text)

    assert len(keywords) == len(set(keywords))


def test_textrank_build_graph_empty():
    tr = TextRank()
    graph = tr._build_graph([])
    assert graph == {}


def test_textrank_build_graph_single_word():
    tr = TextRank()
    graph = tr._build_graph([["کلمه"]])
    assert "کلمه" not in graph or graph["کلمه"] == {}


def test_textrank_pagerank_empty_graph():
    tr = TextRank()
    scores = tr._pagerank({})
    assert scores == {}


def test_textrank_pagerank_scores_positive():
    tr = TextRank()
    graph = {
        "هوش": {"مصنوعی": 2.0, "یادگیری": 1.0},
        "مصنوعی": {"هوش": 2.0},
        "یادگیری": {"هوش": 1.0},
    }
    scores = tr._pagerank(graph)

    assert all(v > 0 for v in scores.values())
    assert set(scores.keys()) == {"هوش", "مصنوعی", "یادگیری"}


def test_textrank_custom_window():
    tr_narrow = TextRank(window=1, top_n=3)
    tr_wide = TextRank(window=4, top_n=3)
    text = "هوش مصنوعی یادگیری ماشین پردازش زبان طبیعی"

    kw_narrow = tr_narrow.transform(text)
    kw_wide = tr_wide.transform(text)

    assert isinstance(kw_narrow, list)
    assert isinstance(kw_wide, list)


def test_textrank_no_stopwords_only_text():
    tr = TextRank()
    # Text consisting mostly of stop words
    keywords = tr.transform("و یا در از به با")
    assert isinstance(keywords, list)
