"""
_utils/_loader/xlsx.py
========================

.. module:: xlsx
   :platform: Unix
   :synopsis: Provides functions to read and write .xlsx files.

Module Overview
---------------

This module includes functions for reading from and writing to .xlsx files, facilitating the
import and export of spectral data organized in a DataCube format.

Functions
---------

.. autofunction:: _read_xlsx
.. autofunction:: _write_xlsx

"""

import numpy as np
import pandas as pd

import wizard
from ..._core import DataCube


def _read_xlsx(filepath: str) -> DataCube:
    """
    Read a .xlsx file and convert its contents into a DataCube.

    This function extracts spectral data from the specified Excel file,
    organizing it into a structured DataCube format. It expects the first
    two columns to contain 'x' and 'y' coordinates, with the remaining
    columns representing spectral data.

    :param filepath: The path to the .xlsx file to be read.
    :type filepath: str
    :return: A DataCube containing the parsed data from the Excel file.
    :rtype: DataCube

    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the data cannot be parsed correctly.

    """
    # Read the Excel file into a DataFrame
    df = pd.read_excel(filepath)
    
    # Extract x, y coordinates
    x = df['x'].astype('int32')
    y = df['y'].astype('int32')
    
    # Extract spectral data
    spectral_data = df.iloc[:, 2:].values  # All columns after 'x' and 'y'
    wavelengths = list(df.columns[2:].astype('int32'))  # Get wavelength labels

    # Determine the dimensions of the data cube
    max_x = x.max() + 1
    max_y = y.max() + 1

    # Reshape spectral data into (wavelengths, x, y)
    cube = np.zeros((len(wavelengths), max_x, max_y))

    for i in range(len(x)):
        cube[:, x[i], y[i]] = spectral_data[i]

    return DataCube(cube, wavelengths=wavelengths)


def _write_xlsx(dc: wizard.DataCube, filename: str) -> None:
    """
    Write a DataCube to a .xlsx file.

    This function exports the provided DataCube and its associated wavelengths
    to an Excel file.

    :param datacube: The data to be written, structured as a 3D NumPy array.
    :type datacube: wizard.DataCube
    :param filename: The name of the file to which the data will be saved (without extension).
    :type filename: str

    :raises ValueError: If the dimensions of the datacube and wavelengths do not match.

    """
    shape = dc.shape

    # Create a DataFrame to hold the data
    df = pd.DataFrame()

    # Prepare columns
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

    # Write the DataFrame to an Excel file
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'
    df.to_excel(filename, index=False)
