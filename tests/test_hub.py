import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from shekar.hub import Hub


@pytest.fixture
def temp_cache_dir(monkeypatch):
    """Create a temporary .shekar cache directory and patch Path.home()."""
    temp_dir = tempfile.TemporaryDirectory()
    monkeypatch.setattr(Path, "home", lambda: Path(temp_dir.name))
    yield Path(temp_dir.name)
    temp_dir.cleanup()


def test_get_resource_download_success(temp_cache_dir):
    file_name = "dummy_model.onnx"
    fake_file_path = temp_cache_dir / ".shekar" / file_name

    # Patch download_file to simulate successful download
    with patch.object(Hub, "download_file", return_value=True) as mock_download:
        result = Hub.get_resource(file_name)
        assert result == fake_file_path
        assert result.parent.exists()
        mock_download.assert_called_once()


def test_get_resource_file_exists(temp_cache_dir):
    file_name = "cached_model.onnx"
    cached_path = temp_cache_dir / ".shekar" / file_name
    cached_path.parent.mkdir(parents=True, exist_ok=True)
    cached_path.write_text("dummy data")

    # Patch download_file to ensure it's not called
    with patch.object(Hub, "download_file") as mock_download:
        result = Hub.get_resource(file_name)
        assert result == cached_path
        mock_download.assert_not_called()


def test_get_resource_download_fail(temp_cache_dir):
    file_name = "broken_model.onnx"

    with patch.object(Hub, "download_file", return_value=False):
        with pytest.raises(FileNotFoundError):
            Hub.get_resource(file_name)
