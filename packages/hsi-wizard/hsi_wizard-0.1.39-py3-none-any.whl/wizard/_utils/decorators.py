"""
_utils/decorator.py
====================

.. module:: decorator
   :platform: Unix
   :synopsis: Decorator functions for processing wave and cube values.

Module Overview
---------------

This module contains decorator functions to validate inputs and
enhance functionality for processing wave and cube values.

Functions
---------

.. autofunction:: check_load_dc
.. autofunction:: check_path
.. autofunction:: add_method
.. autofunction:: track_execution_time
.. autofunction:: add_to_workflow
.. autofunction:: check_limits

"""

import os
import time
from functools import wraps
import numpy as np

import wizard
import warnings


def check_load_dc(func) -> np.array:
    """
    Check if the loading function is correctly defined.

    :param func: The loading function to be decorated.
    :return: The wrapped function.
    :rtype: method
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        dc = func(*args, **kwargs)

        if dc != 'no implementation':
            if not isinstance(dc, wizard.DataCube):
                raise ValueError('Loading function should return a DataCube')

            if not (2 < len(dc.cube.shape) <= 3):
                raise ValueError('The return shape should be (v|x|y).')
        else:
            dc = None
        return dc
    return wrapper


def check_path(func):
    """
    Check if the provided data path is valid.

    :param func: The function to be decorated.
    :return: The wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not kwargs.get('path', None):
            path = args[0] if len(args) > 0 else None
        else:
            path = kwargs.get('path')

        if not path:
            raise ValueError('No path provided.')

        if not os.path.exists(path):
            raise FileNotFoundError(f'Invalid path: {path}')

        return func(*args, **kwargs)

    return wrapper


def add_method(cls):
    """
    Decorator to add a method to a class.

    :param cls: The class to which the method will be added.
    :return: The decorator function.

    Source: Michael Garod @ Medium
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator


def track_execution_time(func):
    """
    Decorator to track the execution time of a function in milliseconds.

    :param func: The function to be decorated.
    :return: The wrapped function that prints execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} ms")
        return result
    return wrapper


def add_to_workflow(func):
    """
    Add a function to a template workflow.

    :param func: The function to be added.
    :return: The wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper()


def check_limits(func) -> np.array:
    """
    Clip limits of an image or array.

    :param func: The function to be decorated.
    :return: The wrapped function with clipped image.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        dtype = args[0].dtype
        image = func(*args, **kwargs)

        if dtype in ['float32', 'float64']:
            _max, _min = image.max(), image.min()
            warnings.warn(f'Image values needs to be between 0 and 1. The provided data with min `{_min}` and max `{_max}` gets clipped to 0 an 1. You lose some informations.')
            image = np.clip(image, 0, 1).astype(dtype)
        return image
    return wrapper
