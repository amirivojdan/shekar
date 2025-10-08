import pytest
from shekar.sentiment_analysis.base import SentimentClassifier, SENTIMENT_REGISTRY


class TestSentimentClassifier:
    def test_init_default_model(self):
        """Test initialization with default model."""
        classifier = SentimentClassifier()
        assert hasattr(classifier, "model")
        assert classifier.model is not None

    def test_init_with_valid_model(self):
        """Test initialization with valid model name."""
        classifier = SentimentClassifier(model="albert-binary")
        assert hasattr(classifier, "model")
        assert classifier.model is not None

    def test_init_case_insensitive(self):
        """Test that model name is case insensitive."""
        classifier = SentimentClassifier(model="ALBERT-BINARY")
        assert hasattr(classifier, "model")
        assert classifier.model is not None

    def test_init_with_invalid_model(self):
        """Test initialization with invalid model raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            SentimentClassifier(model="invalid-model")

        assert "Unknown sentiment model 'invalid-model'" in str(exc_info.value)
        assert "Available:" in str(exc_info.value)

    def test_init_with_model_path(self):
        """Test initialization with custom model path."""
        classifier = SentimentClassifier(
            model="albert-binary", model_path="/custom/path"
        )
        assert hasattr(classifier, "model")
        assert classifier.model is not None

    def test_transform_persian_positive_text(self):
        """Test sentiment analysis on Persian positive text."""
        classifier = SentimentClassifier()
        result = classifier.transform("سریال قصه‌های مجید عالی بود!")

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_transform_persian_negative_text(self):
        """Test sentiment analysis on Persian negative text."""
        classifier = SentimentClassifier()
        result = classifier.transform("فیلم ۳۰۰ افتضاح بود.")

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_transform_empty_string(self):
        """Test sentiment analysis on empty string."""
        classifier = SentimentClassifier()
        result = classifier.transform("")

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_transform_english_text(self):
        """Test sentiment analysis on English text."""
        classifier = SentimentClassifier()
        result = classifier.transform("This movie is great!")

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert len(result) > 0

    def test_multiple_transforms_same_instance(self):
        """Test multiple transform calls on same instance."""
        classifier = SentimentClassifier()

        result1 = classifier.transform("متن مثبت")
        result2 = classifier.transform("متن منفی")

        assert isinstance(result1, tuple)
        assert isinstance(result2, tuple)
        assert len(result1) == 2
        assert len(result2) == 2

    def test_sentiment_registry_contains_albert_binary(self):
        """Test that SENTIMENT_REGISTRY contains expected models."""
        assert "albert-binary" in SENTIMENT_REGISTRY
        assert callable(SENTIMENT_REGISTRY["albert-binary"])

    def test_inheritance_from_base_transform(self):
        """Test that SentimentClassifier inherits from BaseTransform."""
        classifier = SentimentClassifier()
        assert hasattr(classifier, "transform")
