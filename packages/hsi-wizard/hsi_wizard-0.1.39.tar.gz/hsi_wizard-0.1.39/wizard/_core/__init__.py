"""
_core/__init__.py
<<<<<<< HEAD
=================

.. module:: __init__
   :platform: Unix
   :synopsis: Initialization of the core package for `hsi-wizard`.

Module Overview
---------------

This module initializes the core functionality of the `hsi-wizard` package, including attaching
dynamic methods from `datacube_ops` to the `DataCube` class. It ensures that operations are
dynamically bound to `DataCube` during runtime, and tracks execution using the `TrackExecutionMeta`
class from the `wizard._utils.tracker` module.

Functions
---------

.. autofunction:: attach_datacube_operations
.. autofunction:: func_as_method

"""

import multiprocessing
from functools import wraps

from .datacube import DataCube
from wizard._utils.tracker import TrackExecutionMeta

__all__ = ['DataCube']


def func_as_method(func):
    """
    Converts a standalone function into a method that can be dynamically attached to a class.

    This function ensures that the method retains the original function's name and signature
    by using the `wraps` decorator.

    Parameters
    ----------
    func : function
        The standalone function to be converted into a method.

    Returns
    -------
    function
        The wrapped function as a method, with a flag indicating it is dynamic.
    """
    @wraps(func)
    def method(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    # Mark the function as dynamic for tracking purposes
    method.__is_dynamic__ = True
    return method


_dynamic_methods_attached = False  # Global flag to prevent repeated attachments


def attach_datacube_operations():
    """
    Dynamically attach functions from `datacube_ops` to the `DataCube` class as methods.

    This function imports `datacube_ops` and attaches all callable operations as methods to
    the `DataCube` class. Each method is wrapped with the `TrackExecutionMeta.record_method`
    decorator to enable execution tracking.

    This operation is only performed once, controlled by the `_dynamic_methods_attached` flag,
    and only in the main process to avoid issues in multiprocessing contexts.

    Notes
    -----
    - Functions from `datacube_ops` are converted into methods using `func_as_method`.
    - Execution tracking is applied to all dynamic methods using `TrackExecutionMeta`.

    Returns
    -------
    None
    """
    from . import datacube_ops  # prevent circular import errors
    global _dynamic_methods_attached
    if not _dynamic_methods_attached:
        # Ensure we're in the main process, not a child process
        if multiprocessing.current_process().name == "MainProcess":
            for name in dir(datacube_ops):
                func = getattr(datacube_ops, name)
                if callable(func):
                    # Wrap the method with the tracking decorator before attaching
                    wrapped_func = TrackExecutionMeta.record_method(func_as_method(func))
                    setattr(DataCube, name, wrapped_func)  # Attach the wrapped function
            _dynamic_methods_attached = True  # Set flag after the first call


# Attach methods to the DataCube class on import
attach_datacube_operations()
