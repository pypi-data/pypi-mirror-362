"""
_utils/_loader/envi.py
=======================

.. module:: envi
   :platform: Unix
   :synopsis: Provides reader and writer functions for ENVI files.

Module Overview
---------------

This module includes functions for reading and writing ENVI `.hdr` and `.img` files.

Functions
---------

.. autofunction:: _read_envi
.. autofunction:: _write_envi
"""

import numpy as np
from spectral.io import envi

from ..._core import DataCube


def _read_hdr(path: str, image_path: str = None) -> DataCube:
    """
    Read an ENVI file and convert it into a DataCube.

    This function supports both standard and custom ENVI setups:
    - If only the header file is provided, the associated binary file is inferred from the metadata.
    - If both header and binary paths are provided, they are used explicitly.

    Parameters
    ----------
    path : str
        Path to the ENVI header (.hdr) file.
    image_path : str, optional
        Path to the binary image file, if different or located elsewhere.

    Returns
    -------
    DataCube
        A DataCube containing the spectral image data and wavelengths.

    Raises
    ------
    FileNotFoundError
        If the header or associated image file is not found.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read("/path/to/image.hdr")
    >>> dc = wizard.read(path='/path/to/image.hdr', image_path='/path/to/image.img')
    """
    img = envi.open(path, image_path) if image_path else envi.open(path)
    cube = img.load().transpose((2, 0, 1))

    wavelengths = img.metadata.get('wavelength')
    if wavelengths is not None:
        wavelengths = [int(float(w)) for w in wavelengths]
    else:
        wavelengths = list(range(cube.shape[0]))

    dc = DataCube(np.array(cube), wavelengths=wavelengths)

    notation = img.metadata.get('wavelength units')

    if notation is not None:
        dc.set_notation(notation)

    return dc


def _write_hdr(dc: DataCube, file_path: str) -> None:
    """
    Write a DataCube to an ENVI file.

    The function exports the DataCube into ENVI format with a header and binary file.
    Wavelengths are stored in the header metadata.

    Parameters
    ----------
    dc : DataCube
        The DataCube to be written to disk.
    file_path : str
        Path to the ENVI header (.hdr) file (without extension or with .hdr).

    Returns
    -------
    None

    Examples
    --------
    >>> import wizard
    >>> wizard._utils._loader.hdr._write_hdr("/path/to/output")
    """
    shape = dc.shape
    image = dc.cube.transpose((1, 2, 0))

    metadata = {
        'interleave': 'bsq',
        'bands': shape[0],
        'lines': shape[1],
        'samples': shape[2],
        'wavelength': [str(w) for w in dc.wavelengths],
        'wavelength units': 'none' if dc.notation is None else dc.notation
    }

    envi.save_image(file_path if file_path.endswith('.hdr') else file_path + '.hdr',
                    image, metadata=metadata, force=True)
