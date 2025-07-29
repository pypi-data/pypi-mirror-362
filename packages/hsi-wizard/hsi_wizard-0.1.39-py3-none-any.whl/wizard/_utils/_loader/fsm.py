"""
_utils/_loader/fsm.py
=======================

.. module:: fsm
   :platform: Unix
   :synopsis: Provides reader and writer functions for FSM files.

Module Overview
---------------

This module includes functions for reading `.fsm` files, typically from Perkin Elmer instruments.
It processes various blocks of data contained within FSM files to extract relevant spectral information.

Functions
---------

.. autofunction:: _block_info
.. autofunction:: _decode_5100
.. autofunction:: _decode_5104
.. autofunction:: _decode_5105
.. autofunction:: _parse_fsm_file
.. autofunction:: _read_fsm

Credits
-------
This code was inspired by:
- Repository: specio
- Author/Organization: paris-saclay-cds
- Original repository: https://github.com/paris-saclay-cds/specio

"""

import struct
import numpy as np

from ._helper import to_cube
from ..._core import DataCube


def _block_info(data):
    """Retrieve the information of the next block."""
    if len(data) != 6:
        raise ValueError(f"'data' should be 6 bytes. Got {len(data)} instead.")
    return struct.unpack('<Hi', data)


def _decode_5100(data):
    """Read the block of data with ID 5100."""
    name_size = struct.unpack('<h', data[:2])[0]
    name = data[2:name_size + 2].decode('utf8')
    header_format = '<ddddddddddiiihBhBhBhB'
    header_data = struct.unpack(header_format, data[name_size + 2:name_size + 106])
    return {
        'name': name,
        'x_delta': header_data[0],
        'y_delta': header_data[1],
        'z_delta': header_data[2],
        'z_start': header_data[3],
        'z_end': header_data[4],
        'z_4d_start': header_data[5],
        'z_4d_end': header_data[6],
        'x_init': header_data[7],
        'y_init': header_data[8],
        'z_init': header_data[9],
        'n_x': header_data[10],
        'n_y': header_data[11],
        'n_z': header_data[12],
        'resolution': header_data[17],
        'transmission': header_data[19]
    }


def _decode_5104(data):
    """Read the block of data with ID 5104."""
    text = []
    start_byte = 0
    data_length = len(data)

    while start_byte + 2 <= data_length:
        tag = data[start_byte:start_byte + 2]
        start_byte += 2

        if tag == b'#u':
            text_size = struct.unpack('<h', data[start_byte:start_byte + 2])[0]
            start_byte += 2
            text.append(data[start_byte:start_byte + text_size].decode('utf8'))
            start_byte += text_size + 6  # Skip over text and padding
        elif tag == b'$u' or tag == b',u':
            text_size = struct.unpack('<h', data[start_byte:start_byte + 2])[0]
            start_byte += 2
            text.append(text_size)  # Assuming it's an integer, as in the original code
            start_byte += 6 if tag == b'$u' else 0
        else:
            start_byte -= 1  # Step back if the tag is not recognized

    # Map extracted texts to their corresponding keys
    keys = [
        'analyst', 'date', 'image_name', 'instrument_model',
        'instrument_serial_number', 'instrument_software_version',
        'accumulations', 'detector', 'source', 'beam_splitter',
        'apodization', 'spectrum_type', 'beam_type', 'phase_correction',
        'ir_accessory', 'igram_type', 'scan_direction', 'background_scans',
        'ir_laser_wave_number_unit'
    ]
    
    return {key: (text[i] if i < len(text) else None) for i, key in enumerate(keys)}


def _decode_5105(data):
    """Read the block of data with ID 5105."""
    return np.frombuffer(data, dtype=np.float32)


FUNC_DECODE = {5100: _decode_5100, 5104: _decode_5104, 5105: _decode_5105}


def _parse_fsm_file(fsm_file):
    """Read the FSM file and extract spectrum data."""
    with open(fsm_file, "rb") as file:
        content = file.read()

    start_byte = 44
    meta = {
        'signature': content[:4],
        'description': content[4:44].decode('utf-8'),
        'filename': fsm_file
    }
    spectrum = []

    while start_byte < len(content):
        block_id, block_size = _block_info(content[start_byte:start_byte + 6])
        start_byte += 6
        if block_size == 0:
            continue
        block_data = content[start_byte:start_byte + block_size]
        if block_id not in FUNC_DECODE:
            print(f"Found block ID: {block_id} (size {block_size})")
            raise ValueError(f"Unexpected block ID {block_id}, possible write error")

        data_extracted = FUNC_DECODE[block_id](block_data)
        start_byte += block_size
        if isinstance(data_extracted, dict):
            meta.update(data_extracted)
        else:
            spectrum.append(data_extracted)

    wavelength = np.arange(meta['z_start'], meta['z_end'] + meta['z_delta'], meta['z_delta'])
    return np.squeeze(spectrum), wavelength, meta


def _read_fsm(path: str) -> DataCube:
    """
    Read function for FSM files from Perkin Elmer. Tested with FTIR data.

    :param path: Path to the FSM file.
    :type path: str
    :return: DataCube containing the spectral data and wavelengths.
    :rtype: DataCube
    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the file format is incorrect.
    """
    fsm_spectra, fsm_wave, fsm_meta = _parse_fsm_file(path)

    # Load dimensions from metadata
    fsm_len_x = fsm_meta['n_x']
    fsm_len_y = fsm_meta['n_y']

    # Convert wavelength to integer type
    fsm_wave = fsm_wave.astype('int')

    # Transform 2D array into a 3D data cube
    fsm_data_cube = to_cube(data=fsm_spectra.T, len_x=fsm_len_x, len_y=fsm_len_y)

    return DataCube(fsm_data_cube, wavelengths=fsm_wave, name='.fsm', notation='cm-1', registered=True)


"""
In Progress
def _write_fsm(data_cube, path):
    # Extract metadata
    fsm_data = data_cube.cube.T  # Convert back to original shape
    fsm_wave = data_cube.wavelengths.astype(float)  # Ensure proper dtype
    fsm_meta = {
        'signature': b'FSM\x00',
        'description': b'Generated FSM file' + b' ' * 23,  # Pad to 40 bytes
        'n_x': fsm_data.shape[1],
        'n_y': fsm_data.shape[2],
        'z_start': fsm_wave[0],
        'z_end': fsm_wave[-1],
        'z_delta': fsm_wave[1] - fsm_wave[0],
    }

    with open(path, "wb") as file:
        # Write file header
        file.write(fsm_meta['signature'])  # 4 bytes
        file.write(fsm_meta['description'])  # 40 bytes
        print("Writing File Header (44 bytes)")

        # ✅ Block 5100: Metadata
        name = b"Generated"
        block_5100_data = struct.pack(
            '<h dddddddddd iiih BhBhBhB',
            len(name),  # Name length
            fsm_meta['z_delta'], fsm_meta['z_delta'], fsm_meta['z_delta'],
            fsm_meta['z_start'], fsm_meta['z_end'], 0, 0,
            0, 0, 0,
            fsm_meta['n_x'], fsm_meta['n_y'], fsm_data.shape[0],
            0, 0, 0, 0, 0, 0, 0, 0  # Placeholder values
        )

        block_size_5100 = len(name) + len(block_5100_data)
        print(f"Writing Block 5100 (size {block_size_5100})")
        file.write(struct.pack('<Hi', 5100, block_size_5100))  # Write Block Header
        file.write(name)  # Write name
        file.write(block_5100_data)  # Write metadata

        # ✅ Block 5105: Spectral data
        spectrum_data = fsm_data.astype(np.float32).tobytes()
        block_size_5105 = len(spectrum_data)
        print(f"Writing Block 5105 (size {block_size_5105})")
        file.write(struct.pack('<Hi', 5105, block_size_5105))  # Write Block Header
        file.write(spectrum_data)  # Write spectral data

    print(f"FSM file written to {path}")

"""
