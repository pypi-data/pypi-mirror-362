"""
__init__.py
============

.. module:: __init__
   :platform: Unix
   :synopsis: Initialization module for the hsi-wizard package.

Module Overview
---------------

This module initializes the `hsi-wizard` package, making key components
accessible for users.

Importing
---------

This module imports essential submodules and classes/functions, including:

- `DataCube` from the `_core.datacube` module
- `plotter` from the `_exploration.plotter` module
- `read` from the `_utils._loader` module

:no-index:
"""

# Import necessary submodules and classes/functions from them
from ._core.datacube import DataCube
from ._exploration.plotter import plotter
from ._exploration.surface import plot_surface
from ._exploration.faces import plot_datacube_faces
from ._utils._loader import read
from ._processing.cluster import isodata, smooth_kmeans

#  Define what should be accessible when using 'from wizard import *'
# __all__ = [
#     'DataCube',
#     'read',
#     'plotter'
# ]


# Meta Data
__version__ = "0.1.0"
__author__ = 'flx'
