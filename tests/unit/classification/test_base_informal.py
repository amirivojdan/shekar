import pytest
from shekar.classification.base_informal import (
    InformalLanguageClassifier,
    INFORMAL_REGISTRY,
)


class TestInformalLanguageClassifier:
    def test_init_default_model(self):
        classifier = InformalLanguageClassifier()
        assert hasattr(classifier, "model")
        assert classifier.model is not None

    def test_init_with_valid_model(self):
        classifier = InformalLanguageClassifier(model="rule_based")
        assert hasattr(classifier, "model")
        assert classifier.model is not None

    def test_init_case_insensitive(self):
        classifier = InformalLanguageClassifier(model="RULE_BASED")
        assert hasattr(classifier, "model")
        assert classifier.model is not None

    def test_init_with_invalid_model(self):
        with pytest.raises(ValueError) as exc_info:
            InformalLanguageClassifier(model="nonexistent_model")
        assert "Unknown model 'nonexistent_model'" in str(exc_info.value)
        assert "Available:" in str(exc_info.value)

    def test_transform_returns_tuple(self):
        classifier = InformalLanguageClassifier()
        result = classifier.transform("نون بگیر بیار داری میای خونه")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_transform_informal_sentence(self):
        classifier = InformalLanguageClassifier()
        label, score = classifier.transform("نون بگیر بیار داری میای خونه")
        assert label == "informal"
        assert score == 1

    def test_transform_formal_sentence(self):
        classifier = InformalLanguageClassifier()
        label, score = classifier.transform("من به خانه می‌آیم")
        assert label == "informal"
        assert score == 0

    def test_transform_empty_string(self):
        classifier = InformalLanguageClassifier()
        result = classifier.transform("")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_informal_registry_contains_rule_based(self):
        assert "rule_based" in INFORMAL_REGISTRY
        assert callable(INFORMAL_REGISTRY["rule_based"])

    def test_inheritance_from_base_transform(self):
        classifier = InformalLanguageClassifier()
        assert hasattr(classifier, "transform")
