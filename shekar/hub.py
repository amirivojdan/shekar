import hashlib
import time
import urllib.request
from pathlib import Path

from tqdm import tqdm


MODEL_HASHES = {
    "albert_persian_tokenizer.json": "79716aa7d8aeee80d362835da4f33e2b36b69fe65c257ead32c5ecd850e9ed17",
    "albert_persian_sentiment_binary_q8.onnx": "377c322edc3c0de0c48bf3fd4420c7385158bd34492f5b157ea6978745c50e4a",
    "albert_persian_ner_q8.onnx": "a3d2b1d2c167abd01e6b663279d3f8c3bb1b3d0411f693515cd0b31a5a3d3e80",
    "albert_persian_pos_q8.onnx": "8b5a2761aae83911272763034e180345fe12b2cd45b6de0151db9fbf9d3d8b31",
    "albert_persian_mlm_embeddings.onnx": "6b2d987ba409fd6957764742e30bfbbe385ab33c210caeb313aa9a2eb9afa51a",
    "fasttext_d100_w5_v100k_cbow_wiki.bin": "27daf69dc030e028dda33465c488e25f72c2ea65a53b5c1e0695b883a8be061c",
    "fasttext_d300_w10_v250k_cbow_naab.bin": "8db1e1e50f4b889c7e1774501541be2832240892b9ca00053772f0af7cd2526b",
    "tfidf_logistic_offensive.onnx": "1ac778114c9e2ec1f94fe463df03008032ce75306c5ed494bb06c4542430df44",
    "albert_persian_tokenizer.model": "5f7e2e33114b079febc60e221a2c2400527b3bef10a8d838720f7810c6984964",
    "albert_persian_dep_parser_q8.onnx": "d14840365ed70a393a6b91457f742733434f63b47476670798562386c8c8ab04",
    "byt5_tg2fa_encoder_q8.onnx": "8ab09bdf12d1d4dc8da9ecaf333078453db31bacbaec95f58bd3984a33b0297c",
    "byt5_tg2fa_decoder_q8.onnx": "ed7f952e2906bc31ffa92e43c8a3999299f21a00c4b47f74c2ac08025d267335",
}

MIRRORS = [
    "https://shekar.ai/",
    "https://ir.shekar.ai/",
]

_DOWNLOAD_TIMEOUT = 10
_BLOCK_SIZE = 65536


class TqdmUpTo(tqdm):
    """Provides update_to(n) which uses tqdm.update(delta_n)."""

    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize

        self.update(b * bsize - self.n)


class Hub:
    USER_AGENT = "Shekar/1.0"

    @staticmethod
    def compute_sha256_hash(
        path: str | Path,
        block_size: int = _BLOCK_SIZE,
    ) -> str:
        """Compute SHA-256 hash of a file."""

        sha256 = hashlib.sha256()

        with open(path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                sha256.update(block)

        return sha256.hexdigest()

    @staticmethod
    def get_mirror_latencies(file_name: str) -> list[tuple[float, str]]:
        """Measure mirror response times."""

        timings = []

        for base_url in MIRRORS:
            url = base_url + file_name

            try:
                start = time.perf_counter()

                req = urllib.request.Request(
                    url,
                    method="HEAD",
                    headers={"User-Agent": Hub.USER_AGENT},
                )

                with urllib.request.urlopen(req, timeout=3):
                    latency = time.perf_counter() - start

                timings.append((latency, base_url))

            except Exception:
                continue

        return sorted(timings, key=lambda x: x[0])

    @staticmethod
    def get_fastest_mirror(file_name: str) -> str:
        """Return fastest available mirror."""

        timings = Hub.get_mirror_latencies(file_name)

        if not timings:
            raise RuntimeError("No available mirrors are reachable at the moment.")

        return timings[0][1]

    @staticmethod
    def validate_file(file_path: Path, expected_hash: str) -> bool:
        """Validate file integrity using SHA-256."""

        if not file_path.exists():
            return False

        actual_hash = Hub.compute_sha256_hash(file_path)

        return actual_hash == expected_hash

    @staticmethod
    def download_file(url: str, dest_path: Path) -> bool:
        """Download url into dest_path using a local opener (no global state mutation)."""

        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-Agent", Hub.USER_AGENT)]

            with opener.open(url, timeout=_DOWNLOAD_TIMEOUT) as response:
                total_size = int(response.headers.get("Content-Length", 0) or 0)

                with TqdmUpTo(
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    miniters=1,
                    desc="Downloading model",
                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
                    total=total_size or None,
                ) as t:
                    with open(dest_path, "wb") as f:
                        while True:
                            block = response.read(_BLOCK_SIZE)
                            if not block:
                                break
                            f.write(block)
                            t.update(len(block))

            return True

        except Exception as e:
            print(f"Error downloading file from {url}: {e}")
            dest_path.unlink(missing_ok=True)
            return False

    @staticmethod
    def download_from_mirrors(
        file_name: str,
        dest_path: Path,
        expected_hash: str,
    ) -> bool:
        """Try mirrors in latency order; validate hash before committing the file."""

        timings = Hub.get_mirror_latencies(file_name)

        if not timings:
            return False

        tmp_path = dest_path.with_suffix(dest_path.suffix + ".tmp")

        for _, base_url in timings:
            url = base_url + file_name

            print(f"Trying mirror: {base_url}")

            tmp_path.unlink(missing_ok=True)

            if not Hub.download_file(url, tmp_path):
                continue

            if not Hub.validate_file(tmp_path, expected_hash):
                print(f"Hash mismatch from {base_url}, trying next mirror...")
                tmp_path.unlink(missing_ok=True)
                continue

            tmp_path.rename(dest_path)
            return True

        tmp_path.unlink(missing_ok=True)
        return False

    @staticmethod
    def get_resource(file_name: str) -> Path:
        """Download and validate resource file, safe for parallel processes."""

        if file_name not in MODEL_HASHES:
            raise ValueError(f"File {file_name} is not recognized.")

        cache_dir = Path.home() / ".shekar"
        cache_dir.mkdir(parents=True, exist_ok=True)

        model_path = cache_dir / file_name
        expected_hash = MODEL_HASHES[file_name]

        if Hub.validate_file(model_path, expected_hash):
            return model_path

        if model_path.exists():
            print(f"Hash mismatch detected for {file_name}. Re-downloading...")
            model_path.unlink(missing_ok=True)

        success = Hub.download_from_mirrors(file_name, model_path, expected_hash)

        if not success:
            raise FileNotFoundError(
                f"Failed to download {file_name} from available mirrors.\n"
                f"Please try again later.\n\n"
                f"You can also manually download the model files from:\n"
                f"https://github.com/amirivojdan/shekar\n\n"
                f"Then place them in the cache directory:\n"
                f"{cache_dir}"
            )

        return model_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python hub.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    print(Hub.compute_sha256_hash(file_path))
