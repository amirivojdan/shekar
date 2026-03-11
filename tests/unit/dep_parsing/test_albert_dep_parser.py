import pytest
from shekar.dep_parsing.albert_dep_parser import AlbertDepParser
from shekar.hub import Hub


class TestAlbertDepParser:
    @pytest.fixture
    def parser(self):
        return AlbertDepParser()

    def test_initialization(self, parser):
        assert parser.session is not None
        assert parser.tokenizer is not None
        assert parser.word_tokenizer is not None
        assert isinstance(parser.id2deprel, dict)
        assert len(parser.id2deprel) == len(AlbertDepParser.dep_relations)

    def test_dep_relations_coverage(self, parser):
        expected = {
            "acl",
            "advcl",
            "advmod",
            "amod",
            "appos",
            "aux",
            "case",
            "cc",
            "ccomp",
            "compound",
            "compound:lvc",
            "conj",
            "cop",
            "csubj",
            "dep",
            "det",
            "fixed",
            "flat:name",
            "flat:num",
            "goeswith",
            "iobj",
            "mark",
            "nmod",
            "nsubj",
            "nsubj:pass",
            "nummod",
            "obj",
            "obl",
            "obl:arg",
            "parataxis",
            "punct",
            "root",
            "vocative",
            "xcomp",
        }
        assert set(parser.id2deprel.values()) == expected

    def test_transform_empty_text(self, parser):
        result = parser.transform("")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_transform_simple_text(self, parser):
        text = "من به خانه رفتم."
        result = parser.transform(text)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_transform_output_structure(self, parser):
        text = "علی کتاب را خواند."
        result = parser.transform(text)

        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 3
            word, head, deprel = item
            assert isinstance(word, str)
            assert isinstance(head, int)
            assert isinstance(deprel, str)
            assert deprel in AlbertDepParser.dep_relations
            assert head >= 0

    def test_transform_head_indices_in_range(self, parser):
        text = "دانش‌آموزان در کلاس درس می‌خوانند."
        result = parser.transform(text)

        n = len(result)
        for _, head, _ in result:
            assert 0 <= head <= n, f"head={head} out of range [0, {n}]"

    def test_transform_exactly_one_root(self, parser):
        text = "او هر روز به پارک می‌رود."
        result = parser.transform(text)

        roots = [(w, h, r) for w, h, r in result if h == 0]
        assert len(roots) >= 1, "Expected at least one token with head=0 (ROOT)"

    def test_transform_word_count_matches(self, parser):
        text = "کتاب روی میز است."
        result = parser.transform(text)

        # Each word in the tokenized output should have an entry
        from shekar.tokenization import WordTokenizer

        words = list(WordTokenizer()(text))
        assert len(result) == len(words)

    def test_transform_words_preserved(self, parser):
        text = "ایران کشور بزرگی است."
        result = parser.transform(text)

        words_in_result = [w for w, _, _ in result]
        from shekar.tokenization import WordTokenizer

        expected_words = list(WordTokenizer()(text))
        assert words_in_result == expected_words

    def test_transform_consistency(self, parser):
        text = "من هر روز کتاب می‌خوانم."
        result1 = parser.transform(text)
        result2 = parser.transform(text)
        assert result1 == result2

    def test_custom_model_path(self):
        model_path = Hub.get_resource("albert_persian_dep_parser_q8.onnx")
        parser = AlbertDepParser(model_path=model_path)
        result = parser.transform("این یک آزمون است.")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_build_inputs_shape(self, parser):
        words = ["علی", "رفت"]
        input_ids, attention_mask, word_to_first_subtoken = parser._build_inputs(words)

        assert input_ids.shape[0] == 1
        assert attention_mask.shape[0] == 1
        assert word_to_first_subtoken.shape == (1, len(words))
        assert input_ids.shape == attention_mask.shape

    def test_build_inputs_cls_sep_tokens(self, parser):
        words = ["سلام"]
        input_ids, _, _ = parser._build_inputs(words)

        assert input_ids[0, 0] == parser.tokenizer.cls_token_id
        # SEP should appear somewhere before padding
        sep_id = parser.tokenizer.sep_token_id
        assert sep_id in input_ids[0]

    def test_build_inputs_attention_mask(self, parser):
        words = ["من", "رفتم"]
        input_ids, attention_mask, _ = parser._build_inputs(words)

        # The mask should have 1s for real tokens followed by 0s for padding
        mask = attention_mask[0].tolist()
        # Find the boundary: first 0 after the real tokens
        if 0 in mask:
            first_pad = mask.index(0)
            assert all(m == 1 for m in mask[:first_pad])
            assert all(m == 0 for m in mask[first_pad:])
        else:
            # No padding — all tokens are real
            assert all(m == 1 for m in mask)

    def test_transform_punctuation_tagged(self, parser):
        text = "سلام! حالت چطور است؟"
        result = parser.transform(text)

        punct_words = {"!", "؟", ".", "،"}
        for word, _, deprel in result:
            if word in punct_words:
                assert deprel == "punct", (
                    f"Expected 'punct' for '{word}', got '{deprel}'"
                )
