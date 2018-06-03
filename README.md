# GeoHam: Location-based Amateur Radio Repeater tools

This library aims to provide tools to manipulate and use (fetch, map, output
CHIRP configuration, filter, ...) various data sources about Amateur Radio
repeaters around the world.

This early version only works with data from the Wireless Institute of
Australia, but the objective is to handle other data sources by adding a single
subclass of a parser object.

The library also comes with a simple command-line tool, `geoham` offering entry
point into the library's functions.

The main building blocks are the [Pandas](https://pandas.pydata.org/) and
[folium](https://python-visualization.github.io/folium/) libraries.

## Installation

    pip install -r requirements.txt
    python setup.py

See the [Python Notebook](README.ipynb) for the rest of the documentation and
full wow. You can run it locally in a Jupyter Notebook.

    jupyter-notebook

## Author

* Olivier Mehani <shtrom+geoham@ssji.net>, VK2SHM
