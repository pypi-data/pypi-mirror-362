# data-tutorials

Simple utility to download data from a url into a folder.
It is a simple helper for cases when one needs to download data in systems like google colab to do a tutorial for example.

```python

  from data_tutorials.data import get_data
  get_data(url="https://raw.githubusercontent.com/ddmms/data-tutorials/main/data/", filename="LiFePO4_supercell.cif", folder="data")
