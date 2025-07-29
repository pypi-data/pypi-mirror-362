"""
_utils/tracker.py
=================

.. module:: tracker
   :platform: Unix
   :synopsis: Tracker functions for monitoring DataCube changes.

Module Overview
---------------

This module contains functions to track changes made to DataCube instances.

Classes
-------

.. autoclass:: TrackExecutionMeta
   :members:
   :undoc-members:
   :show-inheritance:
"""

excluded = ['stop_recording', 'save_template', '_clean_data', '_map_args_to_kwargs', 'execute_template']


class TrackExecutionMeta(type):
    """
    Metaclass for tracking method executions in classes that use it.

    Automatically wraps dynamic methods (marked with `__is_dynamic__ = True`)
    to log their calls when tracking is enabled. Used for debugging, auditing,
    or analyzing usage patterns of dynamic methods.

    Attributes
    ----------
    recording : bool
        Indicates whether method tracking is currently active.

    recorded_methods : list of tuple
        Stores a list of tuples (method_name, args, kwargs) representing
        recorded method calls.

    Methods
    -------
    start_recording()
        Enables method tracking and clears previously recorded data.

    stop_recording()
        Disables method tracking.

    record_method(func)
        Decorator to wrap and conditionally record dynamic method calls.
    """

    recording = False
    recorded_methods = []

    def __new__(cls, name, bases, dct):
        """
        Creates a new class, wrapping its methods for tracking if applicable.

        Wraps all callable attributes except those explicitly excluded or not marked dynamic.

        Parameters
        ----------
        name : str
            Name of the class being created.

        bases : tuple
            Base classes of the new class.

        dct : dict
            Dictionary of the class's attributes and methods.

        Returns
        -------
        type
            A new class with method execution tracking wrappers.
        """
        for key, value in dct.items():
            if callable(value) and key != 'execute_template':
                dct[key] = cls.record_method(value)
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def record_method(func):
        """
        Wraps a method to record its execution if tracking is enabled.

        Only records calls to methods explicitly marked as dynamic
        using the `__is_dynamic__ = True` attribute.

        Parameters
        ----------
        func : callable
            The method to be wrapped.

        Returns
        -------
        callable
            The wrapped method that conditionally records executions.

        Notes
        -----
        This does not alter the method's original behavior, only adds tracking.
        """
        def wrapper(*args, **kwargs):
            if TrackExecutionMeta.recording:
                if getattr(func, '__is_dynamic__', False):
                    print(f"Tracking dynamic method: {func.__name__}")
                    TrackExecutionMeta.recorded_methods.append(
                        (func.__name__, args, kwargs))
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def start_recording():
        """
        Enables method tracking and resets previously recorded calls.

        Notes
        -----
            Use this before any tracked operation to capture method calls.
        """
        TrackExecutionMeta.recording = True
        TrackExecutionMeta.recorded_methods = []

    @staticmethod
    def stop_recording():
        """
        Disables method tracking.

        Notes
        -----
            Use this to halt tracking when the desired operations are complete.
        """
        TrackExecutionMeta.recording = False
