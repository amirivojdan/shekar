from shekar.toxicity import LogisticOffensiveClassifier


class TestLogisticOffensiveClassifier:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.classifier = LogisticOffensiveClassifier()

    def test_init_default_model(self):
        """Test initialization with default model."""
        classifier = LogisticOffensiveClassifier()
        assert classifier.session is not None
        assert classifier.id2label == {0: "neutral", 1: "offensive"}
        assert classifier.stopword_remover is not None

    def test_init_custom_model_path_none(self):
        """Test initialization with None model path."""
        classifier = LogisticOffensiveClassifier(model_path=None)
        assert classifier.session is not None

    def test_transform_neutral_text(self):
        """Test transform with neutral text from docstring example."""
        result = self.classifier.transform("این یک متن معمولی است.")
        label, confidence = result
        assert isinstance(label, str)
        assert label in ["neutral", "offensive"]
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0

    def test_transform_offensive_text(self):
        """Test transform with offensive text from docstring example."""
        result = self.classifier.transform("تو خیلی احمق و بی‌شرفی!")
        label, confidence = result
        assert isinstance(label, str)
        assert label in ["neutral", "offensive"]
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0

    def test_transform_empty_string(self):
        """Test transform with empty string."""
        result = self.classifier.transform("")
        label, confidence = result
        assert isinstance(label, str)
        assert label in ["neutral", "offensive"]
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0

    def test_transform_return_type(self):
        """Test that transform returns a tuple with correct types."""
        result = self.classifier.transform("test text")
        assert isinstance(result, tuple)
        assert len(result) == 2
        label, confidence = result
        assert isinstance(label, str)
        assert isinstance(confidence, float)

    def test_transform_confidence_range(self):
        """Test that confidence scores are within valid range."""
        texts = ["سلام", "متن تست", "hello world"]
        for text in texts:
            _, confidence = self.classifier.transform(text)
            assert 0.0 <= confidence <= 1.0

    def test_multiple_transforms_consistency(self):
        """Test that multiple transforms of the same text return consistent results."""
        text = "این یک متن تست است"
        result1 = self.classifier.transform(text)
        result2 = self.classifier.transform(text)
        assert result1 == result2
