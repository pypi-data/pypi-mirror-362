# Author; alin m elena, alin@elena.re
# Contribs;
# Date: 26-07-2024
# ©alin m elena, GPL v3 https://www.gnu.org/licenses/gpl-3.0.en.html
"""
Simple module to download a file from a URL and save it in a specific folder.
"""

from urllib.request import urlretrieve
from pathlib import Path

# this is only for python 3.9 once done use str| list[str]
from typing import Union
from tqdm.auto import tqdm

DEFAULT_URL = "https://raw.githubusercontent.com/ddmms/data-tutorials/main/data/"

class TqdmUpTo(tqdm):
    """Alternative Class-based version of the above.

    Provides `update_to(n)` which uses `tqdm.update(delta_n)`.

    Inspired by [twine#242](https://github.com/pypa/twine/pull/242),
    [here](https://github.com/pypa/twine/commit/42e55e06).
    """

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize


def download_file(url: str, filename: str, dest: Path) -> None:
    save_file = dest / filename
    url = url if url.endswith('/') else url + '/'
    print(f"try to download {filename} from {url} and save it in {save_file}")
    with TqdmUpTo(unit = 'B', unit_scale = True, unit_divisor = 1024, miniters = 1, desc = filename) as t:
        path, _ = urlretrieve(url + filename, save_file, reporthook = t.update_to)
    if path.exists():
        print(f"saved in {save_file}")
    else:
        print(f"{save_file} could not be downloaded, check url.")


def get_data(
    url: str = DEFAULT_URL, filename: Union[str, list[str]] = "", folder: str = "data"
) -> None:
    p = Path(folder)
    p.mkdir(parents=True, exist_ok=True)
    if isinstance(filename, str):
        download_file(url, filename, p)
    elif isinstance(filename, list):
        for f in filename:
            download_file(url, f, p)
