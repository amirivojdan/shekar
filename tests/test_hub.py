import pytest
import tempfile
import hashlib
from pathlib import Path
from unittest.mock import patch, mock_open

from shekar.hub import Hub, MODEL_HASHES


@pytest.fixture
def temp_cache_dir(monkeypatch):
    """Create a temporary .shekar cache directory and patch Path.home()."""
    temp_dir = tempfile.TemporaryDirectory()
    monkeypatch.setattr(Path, "home", lambda: Path(temp_dir.name))
    yield Path(temp_dir.name)
    temp_dir.cleanup()


@pytest.fixture
def valid_file_name():
    """Return a valid file name from MODEL_HASHES."""
    return "albert_persian_tokenizer.json"


@pytest.fixture
def expected_hash():
    """Return the expected hash for the valid file."""
    return MODEL_HASHES["albert_persian_tokenizer.json"]


def test_get_resource_unrecognized_file(temp_cache_dir):
    """Test that ValueError is raised for unrecognized files."""
    file_name = "unknown_model.onnx"
    
    with pytest.raises(ValueError, match=f"File {file_name} is not recognized"):
        Hub.get_resource(file_name)


def test_get_resource_download_success_with_hash_validation(temp_cache_dir, valid_file_name, expected_hash):
    """Test successful download with correct hash validation."""
    cache_path = temp_cache_dir / ".shekar" / valid_file_name
    
    # Mock successful download and correct hash
    with patch.object(Hub, "download_file", return_value=True) as mock_download, \
         patch.object(Hub, "compute_sha256_hash", return_value=expected_hash) as mock_hash:
        
        result = Hub.get_resource(valid_file_name)
        
        assert result == cache_path
        assert result.parent.exists()
        mock_download.assert_called_once_with(f"https://shekar.ai/{valid_file_name}", cache_path)
        mock_hash.assert_called_with(cache_path)


def test_get_resource_file_exists_with_correct_hash(temp_cache_dir, valid_file_name, expected_hash):
    """Test that existing file with correct hash is returned without download."""
    cached_path = temp_cache_dir / ".shekar" / valid_file_name
    cached_path.parent.mkdir(parents=True, exist_ok=True)
    cached_path.write_text("dummy data")
    
    with patch.object(Hub, "download_file") as mock_download, \
         patch.object(Hub, "compute_sha256_hash", return_value=expected_hash) as mock_hash:
        
        result = Hub.get_resource(valid_file_name)
        
        assert result == cached_path
        mock_download.assert_not_called()
        mock_hash.assert_called_with(cached_path)


def test_get_resource_file_exists_with_wrong_hash(temp_cache_dir, valid_file_name, expected_hash):
    """Test that existing file with wrong hash raises ValueError."""
    cached_path = temp_cache_dir / ".shekar" / valid_file_name
    cached_path.parent.mkdir(parents=True, exist_ok=True)
    cached_path.write_text("dummy data")
    
    wrong_hash = "wrong_hash_value"
    
    with patch.object(Hub, "compute_sha256_hash", return_value=wrong_hash) as mock_hash, \
         patch.object(Path, "unlink") as mock_unlink:
        
        with pytest.raises(ValueError, match=f"Hash mismatch for {valid_file_name}"):
            Hub.get_resource(valid_file_name)
        
        mock_unlink.assert_called_once_with(missing_ok=True)
        # Hash is computed twice: once for comparison, once in error message
        assert mock_hash.call_count >= 1


def test_get_resource_hash_mismatch_after_download(temp_cache_dir, valid_file_name, expected_hash):
    """Test that hash validation only occurs for existing files, not after downloads."""
    cache_path = temp_cache_dir / ".shekar" / valid_file_name
    
    # The file doesn't exist initially, so it will be downloaded
    # Based on the implementation, hash validation only happens for existing files
    with patch.object(Hub, "download_file", return_value=True) as mock_download, \
         patch.object(Hub, "compute_sha256_hash", return_value="any_hash") as mock_hash:
        
        result = Hub.get_resource(valid_file_name)
        
        # Should succeed because hash validation doesn't happen after download
        assert result == cache_path
        mock_download.assert_called_once_with(f"https://shekar.ai/{valid_file_name}", cache_path)
        # Hash is only computed for the final print statements
        mock_hash.assert_called()


def test_existing_file_wrong_hash_behavior(temp_cache_dir, valid_file_name, expected_hash):
    """Test the actual behavior when existing file has wrong hash - it raises ValueError and deletes file."""
    cached_path = temp_cache_dir / ".shekar" / valid_file_name
    cached_path.parent.mkdir(parents=True, exist_ok=True)
    cached_path.write_text("dummy data")
    
    wrong_hash = "definitely_wrong_hash"
    
    # Mock to return wrong hash consistently
    with patch.object(Hub, "compute_sha256_hash", return_value=wrong_hash), \
         patch.object(Path, "unlink") as mock_unlink:
        
        with pytest.raises(ValueError) as exc_info:
            Hub.get_resource(valid_file_name)
        
        # Verify the error message format
        assert "Hash mismatch" in str(exc_info.value)
        assert valid_file_name in str(exc_info.value)
        assert expected_hash in str(exc_info.value)
        assert wrong_hash in str(exc_info.value)
        
        # Verify file was deleted
        mock_unlink.assert_called_once_with(missing_ok=True)


def test_get_resource_download_failure(temp_cache_dir, valid_file_name):
    """Test FileNotFoundError when download fails."""
    cache_path = temp_cache_dir / ".shekar" / valid_file_name
    
    with patch.object(Hub, "download_file", return_value=False), \
         patch.object(Path, "unlink") as mock_unlink:
        
        with pytest.raises(FileNotFoundError, match=f"Failed to download {valid_file_name}"):
            Hub.get_resource(valid_file_name)
        
        mock_unlink.assert_called_once_with(missing_ok=True)


def test_compute_sha256_hash():
    """Test SHA-256 hash computation."""
    test_data = b"Hello, World!"
    expected_hash = hashlib.sha256(test_data).hexdigest()
    
    with patch("builtins.open", mock_open(read_data=test_data)):
        result = Hub.compute_sha256_hash("dummy_path")
        assert result == expected_hash


def test_compute_sha256_hash_large_file():
    """Test SHA-256 hash computation with custom block size."""
    test_data = b"A" * 100000  # Large data to test block reading
    expected_hash = hashlib.sha256(test_data).hexdigest()
    
    with patch("builtins.open", mock_open(read_data=test_data)):
        result = Hub.compute_sha256_hash("dummy_path", block_size=1024)
        assert result == expected_hash


@patch('urllib.request.urlretrieve')
def test_download_file_success(mock_urlretrieve, temp_cache_dir):
    """Test successful file download."""
    dest_path = temp_cache_dir / "test_file.txt"
    mock_urlretrieve.return_value = None
    
    result = Hub.download_file("https://example.com/file.txt", dest_path)
    
    assert result is True
    mock_urlretrieve.assert_called_once()


@patch('urllib.request.urlretrieve')
def test_download_file_failure(mock_urlretrieve, temp_cache_dir):
    """Test download failure handling."""
    dest_path = temp_cache_dir / "test_file.txt"
    mock_urlretrieve.side_effect = Exception("Network error")
    
    result = Hub.download_file("https://example.com/file.txt", dest_path)
    
    assert result is False


def test_model_hashes_dictionary():
    """Test that MODEL_HASHES contains expected entries."""
    expected_files = [
        "albert_persian_tokenizer.json",
        "albert_persian_ner_q8.onnx",
        "albert_persian_mlm_embeddings.onnx",
        "fasttext_d100_w5_v100k_cbow_wiki.bin",
        "fasttext_d300_w10_v250k_cbow_naab.bin"
    ]
    
    for file_name in expected_files:
        assert file_name in MODEL_HASHES
        assert len(MODEL_HASHES[file_name]) == 64  # SHA-256 hash length


def test_cache_directory_creation(temp_cache_dir, valid_file_name, expected_hash):
    """Test that cache directory is created if it doesn't exist."""
    cache_dir = temp_cache_dir / ".shekar"
    assert not cache_dir.exists()
    
    with patch.object(Hub, "download_file", return_value=True), \
         patch.object(Hub, "compute_sha256_hash", return_value=expected_hash):
        
        Hub.get_resource(valid_file_name)
        assert cache_dir.exists()
        assert cache_dir.is_dir()


@patch('builtins.print')
def test_debug_output(mock_print, temp_cache_dir, valid_file_name, expected_hash):
    """Test that debug information is printed."""
    cached_path = temp_cache_dir / ".shekar" / valid_file_name
    cached_path.parent.mkdir(parents=True, exist_ok=True)
    cached_path.write_text("dummy data")
    
    with patch.object(Hub, "compute_sha256_hash", return_value=expected_hash):
        result = Hub.get_resource(valid_file_name)
        
        # Verify that print was called with hash and path
        assert mock_print.call_count == 2
        mock_print.assert_any_call(expected_hash)
        mock_print.assert_any_call(cached_path)