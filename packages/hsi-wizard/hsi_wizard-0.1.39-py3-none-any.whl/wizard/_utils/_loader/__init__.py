"""
_utils/_loader/__init__.py
============================

.. module:: __init__.py
   :platform: Unix
   :synopsis: Initialization for the loader functions in the _utils._loader package.

Module Overview
---------------

This module initializes loader and writer functions for various file types. It allows dynamic registration of loaders based on file extensions.

Functions
---------
.. autofunction:: register_loader
.. autofunction:: read
.. autofunction:: load_all_loaders

"""

import pathlib
import importlib
import os

# Dictionary to register loaders based on file extensions
LOADER_REGISTRY = {}

# Populate __all__ to control the public API
__all__ = ['read']


def register_loader(extension, function_name):
    """
    Register a new loader for a specific file extension.

    :param extension: File extension (e.g., '.csv').
    :type extension: str
    :param function_name: Loader function to be registered (e.g., read_csv).
    :type function_name: callable
    """
    LOADER_REGISTRY[extension] = function_name


def read(path: str, datatype: str = 'auto', **kwargs):
    """
    Read data from files of various types and return a DataCube object.

    :param path: Path to the data file.
    :type path: str
    :param datatype: Data type of the file (e.g., '.csv', '.xlsx'). If 'auto', the file extension is inferred from the path.
    :type datatype: str
    :param kwargs: Additional keyword arguments passed to the loader function.
    :return: DataCube object containing the imported data.
    :rtype: DataCube
    :raises NotImplementedError: If no loader is registered for the specified file type.
    """
    if datatype == 'auto':
        if os.path.isdir(path):
            suffix = '.folder'
        elif path.endswith('tiff') or path.endswith('jpg') or path.endswith('png'):
            suffix = '.image'
        else:
            suffix = pathlib.Path(path).suffix
    else:
        suffix = datatype

    # Get the loader function based on the file extension
    loader_function = LOADER_REGISTRY.get(suffix)

    if loader_function:
        return loader_function(path, **kwargs)
    else:
        raise NotImplementedError(f'No loader for {suffix} files; please use the custom loader class of the DataCube.')


def load_all_loaders():
    """
    Automatically discover and import loaders from the wizard._utils._loader package.

    This function imports modules corresponding to known file types and registers their associated loading functions.
    """
    loader_modules = [
        "csv",
        "xlsx",
        "tdms",
        "fsm",
        "folder",
        "nrrd",
        "image",
        "hdr",
    ]

    for module_name in loader_modules:
        module = importlib.import_module(f'wizard._utils._loader.{module_name}')
        for attr_name in dir(module):
            if attr_name.startswith('_read_'):
                # Assuming the function name is read_csv, read_xlsx, etc.
                extension = '.' + attr_name.split('_')[-1]  # e.g., 'read_csv' -> '.csv'
                loader_function = getattr(module, attr_name)
                register_loader(extension, loader_function)


# Load all loaders dynamically
load_all_loaders()
