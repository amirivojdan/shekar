import os
import shutil
import urllib.request
from pathlib import Path
from tqdm import tqdm
import sys


class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


class Hub:
    @staticmethod
    def get_resource(file_name: str):
        base_url = "https://shekar.ai/"
        cache_dir = Path.home() / ".shekar"
        model_path = cache_dir / file_name

        cache_dir.mkdir(parents=True, exist_ok=True)

        if not model_path.exists():
            
            if Hub.download_file(base_url + file_name, model_path):
                return model_path
            else:
                raise FileNotFoundError(
                    f"Failed to download {file_name} from {base_url}. "
                    f"You can also download it manually from {base_url + file_name} and place it in {cache_dir}."
                )
        return model_path


    @staticmethod
    def download_file(url: str, dest_path: Path) -> bool:
        try:
            
            with TqdmUpTo(
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                miniters=1,
                desc=dest_path.name,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
            ) as t:
                urllib.request.urlretrieve(
                    url,
                    filename=dest_path,
                    reporthook=t.update_to,
                    data=None
                )
                t.total = t.n
            return True
        except Exception as e:
            print(f"Error downloading the file: {e}")
            return False
