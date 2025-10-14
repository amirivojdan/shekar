import urllib.request
from pathlib import Path
from tqdm import tqdm
import hashlib

MODEL_HASHES = {
    "albert_persian_tokenizer.json": "79716aa7d8aeee80d362835da4f33e2b36b69fe65c257ead32c5ecd850e9ed17",
    "albert_persian_sentiment_binary_q8.onnx": "377c322edc3c0de0c48bf3fd4420c7385158bd34492f5b157ea6978745c50e4a",
    "albert_persian_ner_q8.onnx": "a3d2b1d2c167abd01e6b663279d3f8c3bb1b3d0411f693515cd0b31a5a3d3e80",
    "albert_persian_pos_q8.onnx": "8b5a2761aae83911272763034e180345fe12b2cd45b6de0151db9fbf9d3d8b31",
    "albert_persian_mlm_embeddings.onnx": "6b2d987ba409fd6957764742e30bfbbe385ab33c210caeb313aa9a2eb9afa51a",
    "fasttext_d100_w5_v100k_cbow_wiki.bin": "27daf69dc030e028dda33465c488e25f72c2ea65a53b5c1e0695b883a8be061c",
    "fasttext_d300_w10_v250k_cbow_naab.bin": "8db1e1e50f4b889c7e1774501541be2832240892b9ca00053772f0af7cd2526b",
    "tfidf_logistic_offensive.onnx": "1ac778114c9e2ec1f94fe463df03008032ce75306c5ed494bb06c4542430df44",
}


class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""

    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


class Hub:
    @staticmethod
    def compute_sha256_hash(path: str | Path, block_size=65536):
        """Compute the SHA-256 hash of a file."""
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                sha256.update(block)
        return sha256.hexdigest()

    @staticmethod
    def get_resource(file_name: str) -> Path:
        base_url = "https://shekar.ai/"
        cache_dir = Path.home() / ".shekar"

        if file_name not in MODEL_HASHES:
            raise ValueError(f"File {file_name} is not recognized.")

        model_path = cache_dir / file_name

        cache_dir.mkdir(parents=True, exist_ok=True)

        if not model_path.exists():
            if not Hub.download_file(base_url + file_name, model_path):
                model_path.unlink(missing_ok=True)
                raise FileNotFoundError(
                    f"Failed to download {file_name} from {base_url}. "
                    f"You can also download it manually from {base_url + file_name} and place it in {cache_dir}."
                )

        elif Hub.compute_sha256_hash(model_path) != MODEL_HASHES[file_name]:
            model_path.unlink(missing_ok=True)
            raise ValueError(
                f"Hash mismatch for {file_name}. Expected {MODEL_HASHES[file_name]}, got {Hub.compute_sha256_hash(model_path)}"
            )
        return model_path

    @staticmethod
    def download_file(url: str, dest_path: Path) -> bool:
        try:
            with TqdmUpTo(
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                miniters=1,
                desc="Downloading model: ",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
            ) as t:
                urllib.request.urlretrieve(
                    url, filename=dest_path, reporthook=t.update_to, data=None
                )
                t.total = t.n
            return True
        except Exception as e:
            print(f"Error downloading the file: {e}")
            return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python hub.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    print(Hub.compute_sha256_hash(file_path))
