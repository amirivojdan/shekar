import pytest
import os
import tempfile
import hashlib
from pathlib import Path
from unittest import mock
from shekar.hub import Hub, MODEL_HASHES, TqdmUpTo


class TestHub:
    def test_compute_sha256_hash(self):
        # Create a temporary file with known content
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name

        try:
            # Calculate expected hash
            expected_hash = hashlib.sha256(b"test content").hexdigest()
            # Test the method
            actual_hash = Hub.compute_sha256_hash(tmp_path)
            assert actual_hash == expected_hash
        finally:
            # Clean up
            os.unlink(tmp_path)

    def test_compute_sha256_hash_with_path_object(self):
        # Test with a Path object instead of a string
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content with path")
            tmp_path = Path(tmp.name)

        try:
            expected_hash = hashlib.sha256(b"test content with path").hexdigest()
            actual_hash = Hub.compute_sha256_hash(tmp_path)
            assert actual_hash == expected_hash
        finally:
            os.unlink(tmp_path)

    def test_get_resource_file_not_recognized(self):
        # Test for an unrecognized file
        with pytest.raises(ValueError) as excinfo:
            Hub.get_resource("nonexistent_file.txt")
        assert "File nonexistent_file.txt is not recognized" in str(excinfo.value)

    @mock.patch("shekar.hub.Hub.download_file")
    @mock.patch("shekar.hub.Hub.compute_sha256_hash")
    @mock.patch("pathlib.Path.exists")
    @mock.patch("pathlib.Path.mkdir")
    def test_get_resource_download_success(
        self, mock_mkdir, mock_exists, mock_hash, mock_download
    ):
        # Setup mocks
        mock_exists.return_value = False
        mock_download.return_value = True
        mock_hash.return_value = MODEL_HASHES["albert_persian_tokenizer.json"]

        # Call the method
        result = Hub.get_resource("albert_persian_tokenizer.json")

        # Assertions
        assert mock_mkdir.called
        assert mock_download.called
        assert isinstance(result, Path)
        assert result.name == "albert_persian_tokenizer.json"

    @mock.patch("shekar.hub.Hub.download_file")
    @mock.patch("pathlib.Path.exists")
    @mock.patch("pathlib.Path.unlink")
    @mock.patch("pathlib.Path.mkdir")
    def test_get_resource_download_failure(
        self, mock_mkdir, mock_unlink, mock_exists, mock_download
    ):
        # Setup mocks
        mock_exists.return_value = False
        mock_download.return_value = False

        # Call the method and check for exception
        with pytest.raises(FileNotFoundError) as excinfo:
            Hub.get_resource("albert_persian_tokenizer.json")

        assert "Failed to download" in str(excinfo.value)
        assert mock_unlink.called

    @mock.patch("shekar.hub.Hub.compute_sha256_hash")
    @mock.patch("pathlib.Path.exists")
    @mock.patch("pathlib.Path.unlink")
    @mock.patch("pathlib.Path.mkdir")
    def test_get_resource_hash_mismatch(
        self, mock_mkdir, mock_unlink, mock_exists, mock_hash
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_hash.return_value = "wrong_hash_value"

        # Call the method and check for exception
        with pytest.raises(ValueError) as excinfo:
            Hub.get_resource("albert_persian_tokenizer.json")

        assert "Hash mismatch" in str(excinfo.value)
        assert mock_unlink.called

    @mock.patch("urllib.request.urlretrieve")
    def test_download_file_success(self, mock_urlretrieve):
        # Setup
        url = "https://example.com/file.txt"
        dest_path = Path(tempfile.gettempdir()) / "file.txt"

        # Test
        result = Hub.download_file(url, dest_path)

        # Assertions
        assert result is True
        mock_urlretrieve.assert_called_once()

    @mock.patch("urllib.request.urlretrieve")
    def test_download_file_failure(self, mock_urlretrieve):
        # Setup
        mock_urlretrieve.side_effect = Exception("Download failed")
        url = "https://example.com/file.txt"
        dest_path = Path(tempfile.gettempdir()) / "file.txt"

        # Test
        result = Hub.download_file(url, dest_path)

        # Assertions
        assert result is False

    def test_tqdm_up_to(self):
        # Create a TqdmUpTo instance
        with mock.patch("tqdm.tqdm.update") as mock_update:
            t = TqdmUpTo(total=100)

            # Test with tsize=None
            t.update_to(b=1, bsize=10)
            mock_update.assert_called_with(10)

            # Test with tsize specified
            t.update_to(b=2, bsize=10, tsize=200)
            assert t.total == 200
            mock_update.assert_called_with(20)
