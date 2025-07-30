# Author; alin m elena, alin@elena.re
# Contribs;
# Date: 26-07-2024
# ©alin m elena, GPL v3 https://www.gnu.org/licenses/gpl-3.0.en.html

"""
Tests various downloads.
"""

from pathlib import Path
import hashlib
from data_tutorials.data import get_data


def test_download_file():
    get_data(filename="LiFePO4_supercell.cif", folder="data-test")
    with open(Path("data-test") / "LiFePO4_supercell.cif", "rb") as fd:
        try:
            h = hashlib.file_digest(fd, "sha256")
        except AttributeError:
            h = hashlib.sha256()
            h.update(fd.read())
    assert (
        h.hexdigest()
        == "ea9a538dde5bb84b92e9478dbcc078bb560b28a4f5e4b0469d416bff36be272e"
    )


def test_download_files():
    files = ["LiFePO4_supercell.cif", "h2o.xyz"]
    sha256 = {
        "LiFePO4_supercell.cif": "ea9a538dde5bb84b92e9478dbcc078bb560b28a4f5e4b0469d416bff36be272e",
        "h2o.xyz": "522ab1d36d213e48ab6e08517ec3f648c378d4b9efd257feadc64a1d8f3e66d6",
    }
    get_data(filename=files, folder="data-test")
    for f in files:
        with open(Path("data-test") / f, "rb") as fd:
            try:
                h = hashlib.file_digest(fd, "sha256")
            except AttributeError:
                h = hashlib.sha256()
                h.update(fd.read())
        assert h.hexdigest() == sha256[f]
