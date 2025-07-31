import pytest
from unittest.mock import patch
from shekar.pos.albert_pos import AlbertPOS
from shekar.pos.base import POSTagger, POS_REGISTRY


class TestPOSTagger:
    def test_init_with_valid_model(self):
        # Test initialization with a valid model
        tagger = POSTagger(model="albert")
        assert isinstance(tagger.model, AlbertPOS)

    def test_init_with_custom_model_path(self):
        # Test initialization with a custom model path
        custom_path = "custom/model/path"
        tagger = POSTagger(model="albert", model_path=custom_path)
        assert isinstance(tagger.model, AlbertPOS)
        # We can't directly check the model_path without exposing it in the AlbertPOS class

    def test_init_with_invalid_model(self):
        # Test initialization with an invalid model name
        with pytest.raises(ValueError) as exc_info:
            POSTagger(model="invalid_model")
        assert "Unknown POS model 'invalid_model'" in str(exc_info.value)
        assert str(list(POS_REGISTRY.keys())) in str(exc_info.value)

    def test_init_with_case_insensitive_model_name(self):
        # Test that model name is case-insensitive
        tagger = POSTagger(model="AlBeRt")
        assert isinstance(tagger.model, AlbertPOS)

    @patch.object(AlbertPOS, "transform")
    def test_transform_delegates_to_model(self, mock_transform):
        # Test that transform method delegates to the model's transform method
        mock_transform.return_value = [("word", "POS")]
        tagger = POSTagger()
        text = "Sample text"
        result = tagger.transform(text)

        mock_transform.assert_called_once_with(text)
        assert result == [("word", "POS")]

    def test_integration_with_model(self):
        # This is a more integration-style test
        tagger = POSTagger()
        # Assuming the model.transform returns list of (word, pos) tuples
        result = tagger.transform("سلام بر شما.")
        assert isinstance(result, list)
        # Further assertions would depend on the actual implementation of AlbertPOS
