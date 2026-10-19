import re
from pathlib import Path

import pytest

from shekar.classification import OffensiveLanguageClassifier


class TestOffensiveLanguageClassifier:
    def test_init_default_model(self):
        classifier = OffensiveLanguageClassifier()
        assert classifier.model is not None

    def test_init_logistic_model(self):
        classifier = OffensiveLanguageClassifier(model="logistic")
        assert classifier.model is not None

    def test_init_logistic_model_uppercase(self):
        classifier = OffensiveLanguageClassifier(model="LOGISTIC")
        assert classifier.model is not None

    def test_init_invalid_model(self):
        with pytest.raises(ValueError, match="Unknown model 'invalid'"):
            OffensiveLanguageClassifier(model="invalid")

    def test_init_with_missing_model_path_raises(self):
        with pytest.raises(
            FileNotFoundError, match=re.escape(str(Path("/path/to/model")))
        ):
            OffensiveLanguageClassifier(model_path="/path/to/model")

    def test_transform_persian_clean_text(self):
        classifier = OffensiveLanguageClassifier()
        result = classifier.transform("زبان فارسی میهن من است!")
        assert isinstance(result, tuple)

    def test_transform_persian_offensive_text(self):
        classifier = OffensiveLanguageClassifier()
        result = classifier.transform("تو خیلی احمق و بی‌شرفی!")
        assert isinstance(result, tuple)

    def test_callable_interface(self):
        classifier = OffensiveLanguageClassifier()
        result = classifier("زبان فارسی میهن من است!")
        assert isinstance(result, tuple)
