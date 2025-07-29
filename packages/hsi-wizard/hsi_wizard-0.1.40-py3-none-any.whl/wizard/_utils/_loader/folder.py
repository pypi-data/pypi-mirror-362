"""
_utils/_loader/folder.py
==========================

.. module:: images
   :platform: Unix
   :synopsis: Provides functions to read and write image files.

Module Overview
---------------

This module includes functions for reading images from files and converting them into a `DataCube`.
It supports various image formats and allows for batch processing of images from a folder.

Functions
---------

.. autofunction:: filter_image_files
.. autofunction:: load_image
.. autofunction:: image_to_dc
.. autofunction:: _read_folder

"""

import os
import numpy as np
from matplotlib import pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from ..decorators import check_path
from ..._core import DataCube


def filter_image_files(files):
    """
    Filters a list of filenames, returning only those that have image file extensions.

    The function checks for the following image file extensions (case-insensitive):
    - .jpg
    - .jpeg
    - .png
    - .gif
    - .bmp
    - .tiff

    :param files: A list of filenames to be filtered for image file extensions.
    :type files: list[str]
    :returns: A list of filenames that have image file extensions.
    :rtype: list[str]

    :Example:

    >>> files = ["image.jpg", "document.pdf", "photo.png", "archive.zip"]
    >>> image_files = filter_image_files(files)
    >>> print(image_files)  # Output: ['image.jpg', 'photo.png']
    """
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    return [file for file in files if any(file.lower().endswith(ext) for ext in image_extensions)]


@check_path
def _read_folder(path: str, **kwargs) -> DataCube:
    """
    Load a folder of images into a DataCube.

    This function reads all images in the specified folder, filters them by type, and loads them into a DataCube.

    :param path: Path to the directory containing image files.
    :type path: str
    :return: A DataCube containing the loaded images.
    :rtype: DataCube

    :raises FileNotFoundError: If the specified directory does not exist.
    :raises ValueError: If no valid image files are found in the directory.
    """
    _files = [os.path.join(path, f) for f in os.listdir(path)]
    _files_filtered = filter_image_files(_files)

    if not _files_filtered:
        raise ValueError("No valid image files found in the directory.")

    _dc = image_to_dc(_files_filtered, **kwargs)

    return _dc


def load_image(path):
    """
    Load an image from a specified file path.

    :param path: The file path to the image to be loaded.
    :type path: str
    :return: The image read from the file, represented as a NumPy array.
    :rtype: ndarray

    :Example:

    >>> img = load_image('path/to/image.png')
    >>> plt.imshow(img)
    >>> plt.show()
    """
    return plt.imread(path)


def image_to_dc(path: str | list, **kwargs) -> DataCube:
    """
    Load image(s) into a DataCube.

    This function supports both a single image file path or a list of image file paths.
    Images are processed based on the specified type, which determines the transpose operation applied to the data.

    :param path: Path to an image file or a list of image file paths.
                 If a list is provided, images are loaded concurrently.
    :type path: str or list[str]
    :param kwargs: Optional keyword arguments.
        - type: Specifies the transpose operation to apply to the data.
                Can be 'default' (default behavior) or 'pushbroom' (for pushbroom images).
        - Other keyword arguments may be accepted depending on the implementation of `load_image`.

    :returns: A DataCube object containing the image data.
    :rtype: DataCube

    :raises TypeError: If `path` is neither a string nor a list of strings.
    """
    type = kwargs.get('type', 'default')
    name = kwargs.get('name', None)

    if isinstance(path, str):
        img = load_image(path)
        data = np.array(img)

    elif isinstance(path, list):
        def process_image(idx_file):
            idx, file = idx_file
            _img = load_image(file)
            return _img

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_image, enumerate(path)))

        data = np.dstack(results)
    else:
        raise TypeError('Path must be a string to a file or a list of files')

    if data.ndim == 2:
        data = np.expand_dims(data, axis=2)

    if type == 'pushbroom':
        data = np.transpose(data, (1, 2, 0))
    else:
        data = np.transpose(data, (2, 0, 1))

    return DataCube(data, name=name)
