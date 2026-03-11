import pytest
from unittest.mock import patch
from shekar.dep_parsing.albert_dep_parser import AlbertDepParser
from shekar.dep_parsing.base import DependencyParser, DEP_PARSER_REGISTRY


class TestDependencyParser:
    def test_init_with_valid_model(self):
        parser = DependencyParser(model="albert")
        assert isinstance(parser.model, AlbertDepParser)

    def test_init_default_model(self):
        parser = DependencyParser()
        assert isinstance(parser.model, AlbertDepParser)

    def test_init_with_invalid_model(self):
        with pytest.raises(ValueError) as exc_info:
            DependencyParser(model="unknown_model")
        assert "Unknown dependency parser model 'unknown_model'" in str(exc_info.value)
        assert str(list(DEP_PARSER_REGISTRY.keys())) in str(exc_info.value)

    def test_init_case_insensitive_model_name(self):
        parser = DependencyParser(model="AlBeRt")
        assert isinstance(parser.model, AlbertDepParser)

    def test_init_with_custom_model_path(self):
        custom_path = "some/nonexistent/path"
        # Should fall back to Hub download without raising on init
        parser = DependencyParser(model="albert", model_path=custom_path)
        assert isinstance(parser.model, AlbertDepParser)

    @patch.object(AlbertDepParser, "transform")
    def test_transform_delegates_to_model(self, mock_transform):
        mock_transform.return_value = [("کتاب", 2, "obj"), ("خواندم", 0, "root")]
        parser = DependencyParser()
        text = "کتاب خواندم."
        result = parser.transform(text)

        mock_transform.assert_called_once_with(text)
        assert result == [("کتاب", 2, "obj"), ("خواندم", 0, "root")]

    def test_transform_returns_list(self):
        parser = DependencyParser()
        result = parser.transform("من کتاب می‌خوانم.")
        assert isinstance(result, list)

    def test_transform_empty_text(self):
        parser = DependencyParser()
        result = parser.transform("")
        assert result == []

    def test_registry_contains_albert(self):
        assert "albert" in DEP_PARSER_REGISTRY
        assert DEP_PARSER_REGISTRY["albert"] is AlbertDepParser

    def test_print_tree_empty(self, capsys):
        parser = DependencyParser()
        parser.print_tree([])
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_print_tree_single_token(self, capsys):
        parser = DependencyParser()
        parser.print_tree([("رفت", 0, "root")])
        captured = capsys.readouterr()
        assert "ROOT" in captured.out
        assert "رفت" in captured.out
        assert "root" in captured.out

    def test_print_tree_multiple_tokens(self, capsys):
        parser = DependencyParser()
        # علی(1) -> root(0), رفت(2) -> علی(1)
        results = [("علی", 0, "root"), ("رفت", 1, "nsubj")]
        parser.print_tree(results)
        captured = capsys.readouterr()
        assert "ROOT" in captured.out
        assert "علی" in captured.out
        assert "رفت" in captured.out
        assert "root" in captured.out
        assert "nsubj" in captured.out

    def test_print_tree_format(self, capsys):
        parser = DependencyParser()
        results = [("خواند", 0, "root"), ("کتاب", 1, "obj")]
        parser.print_tree(results)
        captured = capsys.readouterr()
        lines = captured.out.strip().splitlines()
        assert lines[0] == "ROOT"
        # Children lines use tree connectors
        assert any("└──" in line or "├──" in line for line in lines[1:])

    def test_integration_full_parse(self):
        parser = DependencyParser()
        result = parser.transform("دانش‌آموز کتاب را خواند.")

        assert isinstance(result, list)
        assert len(result) > 0
        for word, head, deprel in result:
            assert isinstance(word, str)
            assert isinstance(head, int)
            assert isinstance(deprel, str)
            assert deprel in AlbertDepParser.dep_relations
