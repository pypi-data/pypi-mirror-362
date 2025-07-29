"""
_utils/_loader/csv.py
=======================

.. module:: csv
   :platform: Unix
   :synopsis: Provides reader and writer functions for CSV files.

Module Overview
---------------

This module includes functions for reading and writing `.csv` files.

Functions
---------

.. autofunction:: _read_csv

"""

import pandas as pd
import numpy as np

from ..._core import DataCube


def _read_csv(filepath: str) -> DataCube:
    """
    Read a CSV file and convert it into a DataCube.

    The CSV file should have:
    - 'x' and 'y' as the first two columns (integer values representing spatial coordinates).
    - The remaining columns as spectral data with corresponding wavelengths in the header.

    :param filepath: Path to the CSV file.
    :type filepath: str
    :return: A DataCube containing the parsed data.
    :rtype: DataCube
    """
    df = pd.read_csv(filepath, delimiter=';')

    x = df['x'].values.astype('int32')
    y = df['y'].values.astype('int32')
    spectral_data = df.iloc[:, 2:].values  # Extract spectral values
    wavelengths = list(df.columns[2:].astype('int32'))

    max_x = x.max() + 1
    max_y = y.max() + 1

    cube = np.zeros((len(wavelengths), max_x, max_y))
    for i in range(len(x)):
        cube[:, x[i], y[i]] = spectral_data[i]

    return DataCube(cube, wavelengths=wavelengths)


def _write_csv(dc: DataCube, filename: str) -> None:
    """
    Write a DataCube to a CSV file.

    The output CSV file will have:
    - 'x' and 'y' as the first two columns.
    - The remaining columns containing spectral data.

    :param dc: The DataCube to be written.
    :type dc: DataCube
    :param filename: Name of the output CSV file.
    :type filename: str
    """
    shape = dc.shape
    df = pd.DataFrame()

    cols = [str(wavelength) for wavelength in dc.wavelengths]
    y = []
    x = []

    for _x in range(shape[1]):
        for _y in range(shape[2]):
            spec_ = dc.cube[:, _x, _y]
            df_tmp = pd.DataFrame(spec_).T
            df = pd.concat([df, df_tmp])
            y.append(_y)
            x.append(_x)

    df.columns = cols
    df.insert(0, column='y', value=y)
    df.insert(0, column='x', value=x)

    df.to_csv(filename, index=False, sep=';')
