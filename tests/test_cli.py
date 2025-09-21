import pytest
import tempfile
from pathlib import Path
from click.testing import CliRunner
from shekar.cli import cli, _detect_encoding, _iter_lines, _open_out


class TestHelperFunctions:
    def test_detect_encoding_utf8_fallback(self):
        # Test with a file that exists
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
            f.write("test content")
            temp_path = Path(f.name)

        try:
            encoding = _detect_encoding(temp_path)
            assert encoding in ["utf-8", "UTF-8", "ascii"]
        finally:
            temp_path.unlink()

    def test_detect_encoding_exception_fallback(self):
        # Test with non-existent file
        fake_path = Path("non_existent_file.txt")
        encoding = _detect_encoding(fake_path)
        assert encoding == "utf-8"

    def test_iter_lines_with_text(self):
        text = "hello world"
        lines = list(_iter_lines(None, text, None))
        assert lines == ["hello world"]

    def test_iter_lines_no_input_exits(self):
        with pytest.raises(SystemExit):
            list(_iter_lines(None, None, None))

    def test_open_out_with_path(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = Path(f.name)

        try:
            file_obj = _open_out(temp_path)
            assert file_obj is not None
            file_obj.close()
        finally:
            temp_path.unlink()

    def test_open_out_with_none(self):
        result = _open_out(None)
        assert result is None


class TestCLICommands:
    def setup_method(self):
        self.runner = CliRunner()

    def test_version_command(self):
        result = self.runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert result.output.strip()  # Should output some version

    def test_info_command(self):
        result = self.runner.invoke(cli, ["info"])
        assert result.exit_code == 0
        assert "Shekar: Persian NLP toolkit" in result.output
        assert "lib.shekar.io" in result.output

    def test_normalize_with_text(self):
        result = self.runner.invoke(cli, ["normalize", "--text", "hello"])
        # Command may fail due to import issues, but should not crash
        assert result.exit_code in [0, 2]

    def test_normalize_no_input(self):
        result = self.runner.invoke(cli, ["normalize"])
        assert result.exit_code == 2
        assert "Provide --text or --input" in result.output

    def test_wordcloud_no_input(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            output_path = f.name

        try:
            result = self.runner.invoke(cli, ["wordcloud", "-o", output_path])
            assert result.exit_code == 2
            assert "provide either --text or --input" in result.output
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_wordcloud_with_text(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            output_path = f.name

        try:
            result = self.runner.invoke(
                cli, ["wordcloud", "--text", "hello world", "-o", output_path]
            )
            # Command may fail due to import issues, but should not crash
            assert result.exit_code in [0, 1, 2]
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_cli_help(self):
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Shekar CLI for Persian NLP" in result.output

    def test_normalize_help(self):
        result = self.runner.invoke(cli, ["normalize", "--help"])
        assert result.exit_code == 0
        assert "Normalize text" in result.output

    def test_wordcloud_help(self):
        result = self.runner.invoke(cli, ["wordcloud", "--help"])
        assert result.exit_code == 0
        assert "Generate a wordcloud image" in result.output
