.. _resize_example:

Resize
======

The :meth:`resize` method adjusts the spatial dimensions of a `DataCube` to a new width and height by interpolating each spectral layer.  It preserves the original spectral resolution (the wavelength axis) while changing the pixel grid to the user-specified size.

.. note::
   Apart from :meth:`resize`, the :class:`DataCube` class provides many other operations.  See :ref:`DataCube Operations <DataCube_Ops>` for details.

Example
-------

Below is an example that loads a sample data cube, resizes it to half its original width and height, and then displays one of the wavelength slices.

.. literalinclude:: ../../../../examples/01_dc_methods/00_resize.py
   :language: python
   :linenos:

.. figure:: ../../../../resources/imgs/resize.png
   :align: center
   :alt: Resized data cube slice at the central wavelength showing half the original spatial resolution.
