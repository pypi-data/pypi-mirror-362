"""Tools to download files from a link

typical usage

>>> from data_tutorials.data import get_data
>>> get_data(url="my_file_url", filename="mycif", folder="data")

"""

from importlib.metadata import version

__version__ = version("data-tutorials")
