import os
import hashlib
from pathlib import Path
from unittest import mock

import pytest

from shekar.hub import Hub, MODEL_HASHES, TqdmUpTo


def test_compute_sha256_hash_bytesio(tmp_path: Path):
    p = tmp_path / "small.txt"
    p.write_bytes(b"test content")
    expected = hashlib.sha256(b"test content").hexdigest()
    assert Hub.compute_sha256_hash(p) == expected


def test_compute_sha256_hash_empty(tmp_path: Path):
    p = tmp_path / "empty.bin"
    p.write_bytes(b"")
    expected = hashlib.sha256(b"").hexdigest()
    assert Hub.compute_sha256_hash(p) == expected


def test_compute_sha256_hash_large_blockwise(tmp_path: Path):
    # create a file larger than default block size to exercise the loop
    p = tmp_path / "large.bin"
    data = os.urandom(1_000_000)  # 1 MB
    p.write_bytes(data)
    expected = hashlib.sha256(data).hexdigest()
    # use a small block size to ensure multiple iterations
    assert Hub.compute_sha256_hash(p, block_size=4096) == expected


def _fake_home(tmp_path: Path):
    """Return a function that makes Path.home() return tmp_path."""

    def _home():
        return tmp_path

    return _home


@pytest.mark.parametrize("fname", list(MODEL_HASHES.keys()))
def test_get_resource_downloads_when_missing(monkeypatch, tmp_path: Path, fname: str):
    # redirect cache to a temp home
    monkeypatch.setattr(Path, "home", _fake_home(tmp_path))
    # pretend file does not exist
    monkeypatch.setattr(
        Path,
        "exists",
        lambda self: False if self.name == fname else Path(self).exists(),
    )

    # stub download to write a file with the correct hash
    def fake_urlretrieve(url, filename, reporthook=None, data=None):
        # write some bytes, then overwrite with a file whose hash matches expected
        Path(filename).write_bytes(b"placeholder")
        # replace content with a deterministic file that matches expected hash
        # we cannot reconstruct the exact bytes, so instead patch compute_sha256_hash below
        return (url, filename, None)

    monkeypatch.setattr("urllib.request.urlretrieve", fake_urlretrieve)

    # patch compute_sha256_hash to return the registry value for our target file
    monkeypatch.setattr(Hub, "compute_sha256_hash", lambda p: MODEL_HASHES[fname])

    result = Hub.get_resource(fname)
    assert isinstance(result, Path)
    assert result.name == fname
    assert result.parent == tmp_path / ".shekar"


def test_get_resource_download_failure_raises(monkeypatch, tmp_path: Path):
    fname = "albert_persian_tokenizer.json"
    monkeypatch.setattr(Path, "home", _fake_home(tmp_path))
    # force "missing"
    monkeypatch.setattr(Path, "exists", lambda self: False)
    # simulate download failure
    monkeypatch.setattr(Hub, "download_file", lambda url, dest: False)
    # track unlink calls
    unlinked = {"called": False}

    def fake_unlink(self, missing_ok=False):
        unlinked["called"] = True

    monkeypatch.setattr(Path, "unlink", fake_unlink)

    with pytest.raises(FileNotFoundError) as exc:
        Hub.get_resource(fname)
    assert "Failed to download" in str(exc.value)
    assert unlinked["called"] is True


def test_get_resource_hash_mismatch_raises_and_unlinks(monkeypatch, tmp_path: Path):
    fname = "albert_persian_tokenizer.json"
    monkeypatch.setattr(Path, "home", _fake_home(tmp_path))
    target = tmp_path / ".shekar" / fname
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"wrong content")
    # exists -> True
    monkeypatch.setattr(Path, "exists", lambda self: True)
    # hash mismatch
    monkeypatch.setattr(Hub, "compute_sha256_hash", lambda p: "badbadbad")
    # capture unlink
    calls = {"count": 0}

    def fake_unlink(self, missing_ok=False):
        calls["count"] += 1
        try:
            self.unlink(missing_ok=True)  # attempt actual delete if possible
        except Exception:
            pass

    monkeypatch.setattr(Path, "unlink", fake_unlink)

    with pytest.raises(ValueError) as exc:
        Hub.get_resource(fname)
    assert "Hash mismatch" in str(exc.value)
    assert calls["count"] >= 1


def test_get_resource_uses_cached_when_hash_ok(monkeypatch, tmp_path: Path):
    fname = "albert_persian_tokenizer.json"
    monkeypatch.setattr(Path, "home", _fake_home(tmp_path))
    target = tmp_path / ".shekar" / fname
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"correct content")

    # exists -> True
    monkeypatch.setattr(Path, "exists", lambda self: True)
    # hash matches registry
    monkeypatch.setattr(Hub, "compute_sha256_hash", lambda p: MODEL_HASHES[fname])
    # ensure download is NOT called
    with mock.patch.object(Hub, "download_file") as dl_mock:
        out = Hub.get_resource(fname)
        dl_mock.assert_not_called()
        assert out == target


def test_get_resource_unrecognized_file_raises():
    with pytest.raises(ValueError) as exc:
        Hub.get_resource("not_in_registry.onnx")
    assert "is not recognized" in str(exc.value)


def test_download_file_success_sets_progress(monkeypatch, tmp_path: Path):
    url = "https://example.com/file.bin"
    dest = tmp_path / "file.bin"

    # fake progress: call reporthook with chunks to simulate 100 bytes
    def fake_urlretrieve(url, filename, reporthook=None, data=None):
        total = 100
        # call reporthook a few times to simulate progress
        if reporthook:
            reporthook(1, 25, total)  # 25
            reporthook(2, 25, total)  # 50
            reporthook(3, 25, total)  # 75
            reporthook(4, 25, total)  # 100
        Path(filename).write_bytes(b"x" * total)
        return (url, filename, None)

    monkeypatch.setattr("urllib.request.urlretrieve", fake_urlretrieve)
    assert Hub.download_file(url, dest) is True
    assert dest.exists()
    assert dest.stat().st_size == 100


def test_download_file_failure_prints_and_returns_false(
    monkeypatch, tmp_path: Path, capsys
):
    monkeypatch.setattr(
        "urllib.request.urlretrieve", mock.Mock(side_effect=Exception("boom"))
    )
    ok = Hub.download_file("https://example.com/f.bin", tmp_path / "f.bin")
    captured = capsys.readouterr()
    assert ok is False
    assert "Error downloading the file: boom" in captured.out


def test_tqdm_up_to_updates_and_sets_total():
    t = TqdmUpTo(total=0)
    # first call without tsize
    n_before = t.n
    t.update_to(b=2, bsize=10)  # should call update with delta 20
    assert t.n - n_before == 20
    # now with tsize to set total
    t.update_to(b=3, bsize=10, tsize=200)
    assert t.total == 200
    # ensure cumulative n moved by another 10
    assert t.n - n_before == 30
    t.close()
