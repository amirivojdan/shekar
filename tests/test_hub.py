import os
import hashlib
from pathlib import Path
from unittest import mock

import pytest

from shekar.hub import Hub, MODEL_HASHES, MIRRORS, TqdmUpTo


def _fake_home(tmp_path: Path):
    def _home():
        return tmp_path

    return _home


def test_compute_sha256_hash_small(tmp_path: Path):
    p = tmp_path / "small.txt"
    p.write_bytes(b"test content")
    assert Hub.compute_sha256_hash(p) == hashlib.sha256(b"test content").hexdigest()


def test_compute_sha256_hash_empty(tmp_path: Path):
    p = tmp_path / "empty.bin"
    p.write_bytes(b"")
    assert Hub.compute_sha256_hash(p) == hashlib.sha256(b"").hexdigest()


def test_compute_sha256_hash_large_blockwise(tmp_path: Path):
    data = os.urandom(1_000_000)
    p = tmp_path / "large.bin"
    p.write_bytes(data)
    assert (
        Hub.compute_sha256_hash(p, block_size=4096) == hashlib.sha256(data).hexdigest()
    )


def test_validate_file_missing_returns_false(tmp_path: Path):
    assert Hub.validate_file(tmp_path / "nonexistent.bin", "anyhash") is False


def test_validate_file_hash_matches(tmp_path: Path):
    p = tmp_path / "f.bin"
    p.write_bytes(b"abc")
    assert Hub.validate_file(p, hashlib.sha256(b"abc").hexdigest()) is True


def test_validate_file_hash_mismatch(tmp_path: Path):
    p = tmp_path / "f.bin"
    p.write_bytes(b"abc")
    assert Hub.validate_file(p, "wronghash") is False


def test_get_mirror_latencies_all_fail(monkeypatch):
    monkeypatch.setattr(
        "urllib.request.urlopen", mock.Mock(side_effect=Exception("unreachable"))
    )
    assert Hub.get_mirror_latencies("model.onnx") == []


def test_get_mirror_latencies_returns_sorted(monkeypatch):
    perf_values = iter([0.0, 0.2, 0.3, 0.4])

    ctx = mock.MagicMock()
    ctx.__enter__ = lambda s: s
    ctx.__exit__ = mock.MagicMock(return_value=False)

    monkeypatch.setattr("urllib.request.urlopen", mock.Mock(return_value=ctx))
    monkeypatch.setattr("time.perf_counter", lambda: next(perf_values))

    timings = Hub.get_mirror_latencies("model.onnx")
    assert len(timings) == len(MIRRORS)
    assert timings == sorted(timings, key=lambda x: x[0])
    assert all(isinstance(lat, float) and isinstance(url, str) for lat, url in timings)


def test_get_mirror_latencies_skips_failed_mirrors(monkeypatch):
    urls_seen = []

    def fake_urlopen(req, **_):
        urls_seen.append(req.full_url)
        if MIRRORS[0] in req.full_url:
            raise Exception("timeout")
        ctx = mock.MagicMock()
        ctx.__enter__ = lambda s: s
        ctx.__exit__ = mock.MagicMock(return_value=False)
        return ctx

    perf_values = iter([0.0, 0.1, 0.2])
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    monkeypatch.setattr("time.perf_counter", lambda: next(perf_values))

    timings = Hub.get_mirror_latencies("model.onnx")
    assert len(timings) == len(MIRRORS) - 1
    assert all(MIRRORS[0] not in url for _, url in timings)


def test_get_fastest_mirror_raises_when_no_mirrors_reachable(monkeypatch):
    monkeypatch.setattr(Hub, "get_mirror_latencies", mock.Mock(return_value=[]))
    with pytest.raises(RuntimeError, match="No available mirrors"):
        Hub.get_fastest_mirror("model.onnx")


def test_get_fastest_mirror_returns_first_sorted(monkeypatch):
    monkeypatch.setattr(
        Hub,
        "get_mirror_latencies",
        mock.Mock(return_value=[(0.05, "https://fast/"), (0.2, "http://slow/")]),
    )
    assert Hub.get_fastest_mirror("model.onnx") == "https://fast/"


def test_download_file_success(monkeypatch, tmp_path: Path):
    dest = tmp_path / "file.bin"
    data = b"x" * 100

    response = mock.MagicMock()
    response.headers.get.return_value = str(len(data))
    response.read.side_effect = [data, b""]
    cm = mock.MagicMock()
    cm.__enter__.return_value = response
    cm.__exit__.return_value = False
    opener = mock.MagicMock()
    opener.open.return_value = cm

    monkeypatch.setattr("urllib.request.build_opener", mock.Mock(return_value=opener))
    assert Hub.download_file("https://example.com/file.bin", dest) is True
    assert dest.read_bytes() == data


def test_download_file_failure_returns_false_and_prints(
    monkeypatch, tmp_path: Path, capsys
):
    opener = mock.MagicMock()
    opener.open.side_effect = Exception("boom")

    monkeypatch.setattr("urllib.request.build_opener", mock.Mock(return_value=opener))
    ok = Hub.download_file("https://example.com/f.bin", tmp_path / "f.bin")
    assert ok is False
    out = capsys.readouterr().out
    assert "Error downloading file from" in out
    assert "boom" in out


def test_download_from_mirrors_no_mirrors_reachable(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(Hub, "get_mirror_latencies", mock.Mock(return_value=[]))
    assert (
        Hub.download_from_mirrors("model.bin", tmp_path / "model.bin", "anyhash")
        is False
    )


def test_download_from_mirrors_success_on_first(monkeypatch, tmp_path: Path):
    dest = tmp_path / "model.bin"
    monkeypatch.setattr(
        Hub,
        "get_mirror_latencies",
        mock.Mock(return_value=[(0.05, "https://m1/"), (0.1, "https://m2/")]),
    )
    monkeypatch.setattr(Hub, "validate_file", mock.Mock(return_value=True))

    def fake_download(url, dest_path):
        dest_path.write_bytes(b"data")
        return True

    monkeypatch.setattr(Hub, "download_file", fake_download)
    assert Hub.download_from_mirrors("model.bin", dest, "anyhash") is True
    assert dest.exists()


def test_download_from_mirrors_falls_back_to_second(monkeypatch, tmp_path: Path):
    dest = tmp_path / "model.bin"
    monkeypatch.setattr(
        Hub,
        "get_mirror_latencies",
        mock.Mock(return_value=[(0.05, "https://m1/"), (0.1, "https://m2/")]),
    )
    monkeypatch.setattr(Hub, "validate_file", mock.Mock(return_value=True))
    call_count = {"n": 0}

    def fake_download(url, dest_path):
        call_count["n"] += 1
        if "m1" in url:
            return False
        dest_path.write_bytes(b"data")
        return True

    monkeypatch.setattr(Hub, "download_file", fake_download)
    assert Hub.download_from_mirrors("model.bin", dest, "anyhash") is True
    assert call_count["n"] == 2


def test_download_from_mirrors_all_fail(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        Hub,
        "get_mirror_latencies",
        mock.Mock(return_value=[(0.05, "https://m1/"), (0.1, "https://m2/")]),
    )
    monkeypatch.setattr(Hub, "download_file", mock.Mock(return_value=False))
    assert (
        Hub.download_from_mirrors("model.bin", tmp_path / "model.bin", "anyhash")
        is False
    )


def test_get_resource_unrecognized_file_raises():
    with pytest.raises(ValueError, match="is not recognized"):
        Hub.get_resource("not_in_registry.onnx")


@pytest.mark.parametrize("fname", list(MODEL_HASHES.keys()))
def test_get_resource_downloads_when_missing(monkeypatch, tmp_path: Path, fname: str):
    monkeypatch.setattr(Path, "home", _fake_home(tmp_path))
    cache_dir = tmp_path / ".shekar"
    cache_dir.mkdir(parents=True, exist_ok=True)

    def fake_download_from_mirrors(_, dest_path, __):
        dest_path.write_bytes(b"model bytes")
        return True

    monkeypatch.setattr(Hub, "download_from_mirrors", fake_download_from_mirrors)
    monkeypatch.setattr(
        Hub, "compute_sha256_hash", mock.Mock(return_value=MODEL_HASHES[fname])
    )

    result = Hub.get_resource(fname)
    assert isinstance(result, Path)
    assert result.name == fname
    assert result.parent == cache_dir


def test_get_resource_uses_cached_file_without_download(monkeypatch, tmp_path: Path):
    fname = "albert_persian_tokenizer.json"
    monkeypatch.setattr(Path, "home", _fake_home(tmp_path))
    target = tmp_path / ".shekar" / fname
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"correct content")

    monkeypatch.setattr(
        Hub, "compute_sha256_hash", mock.Mock(return_value=MODEL_HASHES[fname])
    )

    with mock.patch.object(Hub, "download_file") as dl_mock:
        result = Hub.get_resource(fname)
        dl_mock.assert_not_called()
    assert result == target


def test_get_resource_download_failure_raises(monkeypatch, tmp_path: Path):
    fname = "albert_persian_tokenizer.json"
    monkeypatch.setattr(Path, "home", _fake_home(tmp_path))
    cache_dir = tmp_path / ".shekar"
    cache_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(Hub, "download_from_mirrors", mock.Mock(return_value=False))

    with pytest.raises(FileNotFoundError, match="Failed to download"):
        Hub.get_resource(fname)

    assert not (cache_dir / fname).exists()


def test_get_resource_hash_mismatch_redownload_fails(monkeypatch, tmp_path: Path):
    fname = "albert_persian_tokenizer.json"
    monkeypatch.setattr(Path, "home", _fake_home(tmp_path))
    target = tmp_path / ".shekar" / fname
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"corrupted")

    monkeypatch.setattr(Hub, "compute_sha256_hash", mock.Mock(return_value="badhash"))
    monkeypatch.setattr(Hub, "download_from_mirrors", mock.Mock(return_value=False))

    with pytest.raises(FileNotFoundError, match="Failed to download"):
        Hub.get_resource(fname)


def test_get_resource_hash_mismatch_triggers_redownload_success(
    monkeypatch, tmp_path: Path
):
    fname = "albert_persian_tokenizer.json"
    monkeypatch.setattr(Path, "home", _fake_home(tmp_path))
    target = tmp_path / ".shekar" / fname
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"corrupted")

    monkeypatch.setattr(Hub, "compute_sha256_hash", mock.Mock(return_value="badhash"))

    def fake_redownload(_, dest_path, expected_hash):
        assert expected_hash == MODEL_HASHES[fname]
        dest_path.write_bytes(b"good content")
        return True

    monkeypatch.setattr(Hub, "download_from_mirrors", fake_redownload)

    result = Hub.get_resource(fname)
    assert result == target
    assert target.exists()


def test_tqdm_up_to_updates_and_sets_total():
    t = TqdmUpTo(total=0)
    n_before = t.n
    t.update_to(b=2, bsize=10)
    assert t.n - n_before == 20
    t.update_to(b=3, bsize=10, tsize=200)
    assert t.total == 200
    assert t.n - n_before == 30
    t.close()
