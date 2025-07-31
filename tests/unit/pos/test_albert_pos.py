import pytest
from shekar.pos.albert_pos import AlbertPOS
from shekar.hub import Hub


class TestAlbertPOS:
    @pytest.fixture
    def pos_tagger(self):
        return AlbertPOS()

    def test_initialization(self, pos_tagger):
        assert pos_tagger.session is not None
        assert pos_tagger.tokenizer is not None
        assert pos_tagger.word_tokenizer is not None
        assert isinstance(pos_tagger.id2tag, dict)
        assert (
            len(pos_tagger.id2tag) == 17
        )  # Verify the tag dictionary has all expected entries

    def test_transform_empty_text(self, pos_tagger):
        result = pos_tagger.transform("")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_transform_simple_text(self, pos_tagger):
        text = "من به خانه رفتم."
        result = pos_tagger.transform(text)

        assert isinstance(result, list)
        assert len(result) > 0

        # Check structure of returned data
        for word_tag_pair in result:
            assert isinstance(word_tag_pair, tuple)
            assert len(word_tag_pair) == 2
            word, tag = word_tag_pair
            assert isinstance(word, str)
            assert isinstance(tag, str)
            assert tag in pos_tagger.id2tag.values()

    def test_transform_with_punctuation(self, pos_tagger):
        text = "سلام! این یک متن تست است. آیا همه چیز خوب است؟"
        result = pos_tagger.transform(text)

        # Check that punctuation is properly tagged
        punctuation_marks = {".", ",", "!", "؟", ":", ";", "«", "»"}
        for word, tag in result:
            if word in punctuation_marks:
                assert tag == "PUNCT"

    def test_custom_model_path(self, tmp_path):
        # This test will be skipped if the model file doesn't exist
        model_path = Hub.get_resource("albert_persian_pos_q8.onnx")

        # Create a POS tagger with explicit model path
        pos_tagger = AlbertPOS(model_path=model_path)

        # Verify it works
        result = pos_tagger.transform("این یک آزمون است.")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_transform_consistency(self, pos_tagger):
        text = "من به مدرسه می‌روم."

        # Run the transform twice to check for consistency
        result1 = pos_tagger.transform(text)
        result2 = pos_tagger.transform(text)

        assert result1 == result2
