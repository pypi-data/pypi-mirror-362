"""
_utils/_loader/pickle.py
==========================

.. module:: pickle
   :platform: Unix
   :synopsis: Provides functions to read and write pickle files.

Module Overview
---------------

This module includes functions for reading pickle files that store serialized Python objects,
specifically NumPy arrays. It converts the loaded data into a DataCube format for further processing.

Functions
---------

.. autofunction:: _read_pickle

"""

import pickle

import wizard
from ..._core import DataCube


def _read_pickle(path: str) -> DataCube:
    """
    Load a pickled NumPy array and convert it into a DataCube.

    :param path: The file path to the pickle file.
    :type path: str
    :return: A DataCube containing the loaded NumPy array.
    :rtype: DataCube

    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the loaded data is not in the expected format.

    """
    file = open(path,'rb')
    data = pickle.load(file)

    if not isinstance(data, wizard.DataCube):
        raise ValueError("Loaded data is not a DataCube")

    # Create and return the DataCube
    return DataCube(data)


def _write_pickle(data: DataCube, path: str) -> None:
    """
    Save a DataCube object to a pickle file.

    :param data: The DataCube object to be saved.
    :type data: DataCube
    :param path: The file path where the DataCube will be saved.
    :type path: str
    :return: None

    :raises TypeError: If the data cannot be pickled.
    :raises IOError: If there is an error writing to the file.

    """

    try:
        with open(path, 'wb') as file:
            pickle.dump(data, file)
    except TypeError as e:
        raise TypeError(f"Data cannot be pickled: {e}")
    except IOError as e:
        raise IOError(f"Error writing file: {e}")
