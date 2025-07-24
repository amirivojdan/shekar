import pytest
from shekar.keyword_extraction import KeywordExtractor
from shekar.keyword_extraction.rake import RAKE


def test_keyword_extractor_default_model_is_rake():
    extractor = KeywordExtractor()
    assert isinstance(extractor.model, RAKE)


def test_keyword_extractor_invalid_model_raises():
    with pytest.raises(ValueError, match="Unknown keyword extraction model 'invalid'"):
        KeywordExtractor(model="invalid")


def test_keyword_extractor_fit_returns_model():
    extractor = KeywordExtractor()
    result = extractor.fit(["متن تست"])
    assert result is extractor.model


def test_keyword_extractor_transform_returns_keywords():
    extractor = KeywordExtractor(top_n=5, max_length=3)
    text = "امروز هوا بسیار خوب و آفتابی است و من به پارک رفتم تا قدم بزنم."

    output = extractor.transform(text)

    assert isinstance(output, list)
    assert len(output) <= 5

    for item in output:
        # Accept either list of strings or list of (phrase, score)
        if isinstance(item, tuple):
            phrase, score = item
            assert isinstance(phrase, str)
            assert isinstance(score, (int, float))
        else:
            assert isinstance(item, str)


def test_keyword_extractor_respects_top_n_limit():
    extractor = KeywordExtractor(top_n=2)
    text = "کتابخانه مرکزی دانشگاه تهران بسیار بزرگ و مجهز است."

    keywords = extractor.transform(text)

    assert len(keywords) <= 2
