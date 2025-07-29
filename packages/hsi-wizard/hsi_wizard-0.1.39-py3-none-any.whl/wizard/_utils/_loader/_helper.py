"""
_utils/_loader/_helper.py
===========================

.. module:: _helper
   :platform: Unix
   :synopsis: Utility functions for file operations and data transformations.

Module Overview
---------------

This module provides helper functions for various file operations, including transforming data arrays,
retrieving files by extension, and converting paths to absolute form.

Functions
---------

.. autofunction:: to_cube
.. autofunction:: get_files_by_extension
.. autofunction:: make_path_absolute

"""

import os
import glob
import numpy as np


def to_cube(data: np.array, len_x: int, len_y: int) -> np.array:
    """
    Transform a 1D numpy array into a 3D data cube-like array.

    The transformation uses Fortran-like index ordering, which means the
    data is reshaped according to Fortran order.

    :param data: 1D array of data in Fortran order.
    :type data: np.ndarray
    :param len_x: The length of the data cube along the x-axis (pixel size x).
    :type len_x: int
    :param len_y: The length of the data cube along the y-axis (pixel size y).
    :type len_y: int
    :return: Transformed 3D data cube.
    :rtype: np.ndarray
    """
    return data.reshape(-1, len_x, len_y, order='F')


def get_files_by_extension(path: str, extension: str) -> list:
    """
    Retrieve a sorted list of filenames with a specified extension from a directory.

    :param path: Directory path to search for files.
    :type path: str
    :param extension: File extension to filter by (e.g., `.csv`).
    :type extension: str
    :return: Sorted list of filenames with the specified extension.
    :rtype: list
    """
    if not extension:
        return []

    if not os.path.isdir(path):
        return []

    if not extension.startswith('.'):
        extension = '.' + extension

    return sorted(glob.glob(os.path.join(path, '*' + extension.lower())))


def make_path_absolute(path: str) -> str:
    """
    Convert a relative path to an absolute path if it is not already absolute.

    :param path: Path to the file or directory.
    :type path: str
    :return: Absolute path to the file or directory.
    :rtype: str
    :raises ValueError: If the input path is not a string or is invalid.
    """
    if isinstance(path, str) and path:
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        return path.lower()
    else:
        raise ValueError("Input path must be a non-empty string.")
