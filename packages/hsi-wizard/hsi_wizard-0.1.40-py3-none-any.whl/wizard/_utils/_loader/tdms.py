"""
_utils/_loader/tdms.py
========================

.. module:: tdms
   :platform: Unix
   :synopsis: Provides functions to read and write .tdms files.

Module Overview
---------------

This module includes functions for reading .tdms files, specifically designed to extract spectral data
and organize it into a DataCube format.

Functions
---------

.. autofunction:: _read_tdms

"""
import re
from nptdms import TdmsFile

from ._helper import to_cube
from ..._core import DataCube


# Precompile regex for length extraction
def _extract_dims(col_name):
    nums = re.findall(r"\d+", col_name)
    return int(nums[0]) + 1, int(nums[1]) + 1


def _read_tdms(path: str) -> DataCube:
    """
    Optimized TDMS reader: reads the file, cleans and filters columns,
    vectorizes operations, and builds DataCube efficiently.
    """
    # Load and convert to DataFrame
    tdms = TdmsFile(path)
    df = tdms.as_dataframe()

    # Clean column names in-place
    cols = df.columns.str.replace(' ', '', regex=False).str.replace("'", '', regex=False)
    df.columns = cols

    # Identify columns by mask
    is_raw = cols.str.contains('RAW')
    is_drop = cols.str.contains('DarkCurrent') | cols.str.contains('cm|nm')
    is_sample = ~(is_raw | is_drop)

    # Determine data type and wavelength column offset
    if cols.str.contains('RAMAN').any():
        data_type, wave_col = 'raman', 1
    elif cols.str.contains('NIR|KNIR').any():
        data_type, wave_col = 'nir', 1
    elif cols.str.contains('VIS|KVIS').any():
        data_type, wave_col = 'vis', 2
    else:
        data_type, wave_col = '', 1

    # Extract wavelength array
    wave = df.iloc[:, -wave_col].to_numpy(dtype=int)

    # Compute spatial dimensions from last sample column
    sample_cols = cols[is_sample]
    if sample_cols.size:
        len_x, len_y = _extract_dims(sample_cols[-1])
    else:
        # fallback to raw if no sample columns
        raw_cols = cols[is_raw]
        len_x, len_y = _extract_dims(raw_cols[-1])

    # Filter out drop columns
    df = df.loc[:, ~is_drop]

    # Select data array
    data_cols = cols[is_sample] if is_sample.any() else cols[is_raw]
    data_arr = df[data_cols].to_numpy()

    # Build cube and return
    cube = to_cube(data=data_arr, len_x=len_x, len_y=len_y)
    return DataCube(cube=cube, wavelengths=wave, name=data_type)
