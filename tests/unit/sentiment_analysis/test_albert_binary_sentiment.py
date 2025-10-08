from shekar.sentiment_analysis.albert_sentiment_binary import (
    AlbertBinarySentimentClassifier,
)
from shekar.base import BaseTransform


class TestAlbertBinarySentimentClassifier:
    def setup_method(self):
        """Setup test fixtures before each test method."""
        self.classifier = AlbertBinarySentimentClassifier()

    def test_init_default_model(self):
        """Test initialization with default model."""
        classifier = AlbertBinarySentimentClassifier()
        assert classifier.session is not None
        assert classifier.tokenizer is not None
        assert classifier.id2tag == {0: "negative", 1: "positive"}

    def test_init_custom_model_path(self):
        """Test initialization with custom model path."""
        # Test with None path (should use default)
        classifier = AlbertBinarySentimentClassifier(model_path=None)
        assert classifier.session is not None

        # Test with non-existent path (should use default)
        classifier = AlbertBinarySentimentClassifier(
            model_path="non_existent_path.onnx"
        )
        assert classifier.session is not None

    def test_transform_returns_tuple(self):
        """Test that transform returns a tuple with label and score."""
        result = self.classifier.transform("این یک متن تست است")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], float)

    def test_transform_negative_sentiment_docstring_example(self):
        """Test negative sentiment example from docstring."""
        result = self.classifier.transform("فیلم ۳۰۰ افتضاح بود.")
        label, score = result
        assert label == "negative"
        assert isinstance(score, float)
        assert 0 <= score <= 1

    def test_transform_positive_sentiment_docstring_example(self):
        """Test positive sentiment example from docstring."""
        result = self.classifier.transform("سریال قصه‌های مجید عالی بود!")
        label, score = result
        assert label == "positive"
        assert isinstance(score, float)
        assert 0 <= score <= 1

    def test_transform_empty_string(self):
        """Test transform with empty string."""
        result = self.classifier.transform("")
        label, score = result
        assert label in ["positive", "negative"]
        assert isinstance(score, float)
        assert 0 <= score <= 1

    def test_transform_multiple_calls(self):
        """Test multiple calls to transform method."""
        text1 = "خوب"
        text2 = "بد"

        result1 = self.classifier.transform(text1)
        result2 = self.classifier.transform(text2)

        assert isinstance(result1, tuple)
        assert isinstance(result2, tuple)
        assert result1[0] in ["positive", "negative"]
        assert result2[0] in ["positive", "negative"]

    def test_id2tag_mapping(self):
        """Test id2tag mapping is correct."""
        assert self.classifier.id2tag[0] == "negative"
        assert self.classifier.id2tag[1] == "positive"

    def test_inheritance(self):
        """Test that class inherits from BaseTransform."""
        assert isinstance(self.classifier, BaseTransform)

    def test_transform_score_range(self):
        """Test that confidence scores are in valid range [0, 1]."""
        test_texts = ["خوب", "بد", "عادی", "فوق العاده"]

        for text in test_texts:
            _, score = self.classifier.transform(text)
            assert 0 <= score <= 1, (
                f"Score {score} for text '{text}' is out of range [0, 1]"
            )
