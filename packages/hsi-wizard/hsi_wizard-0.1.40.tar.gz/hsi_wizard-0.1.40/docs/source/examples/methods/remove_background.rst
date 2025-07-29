.. _remove_background_example:

Remove Background
=================

The :meth:`.remove_background` method subtracts the spatially varying background signal from each spectral slice.


.. note::
   Apart from :meth:`remove_background`, the :class:`DataCube` class provides many other operations.  See :ref:`DataCube Operations <DataCube_Ops>` for details.

Example
-------

Below is a demonstration of loading a data cube, removing its background, and plotting a selected wavelength slice:

.. literalinclude:: ../../../../examples/01_dc_methods/01_remove_background.py
   :language: python
   :linenos:

.. figure:: ../../../../resources/imgs/remove_background.png
   :align: center
   :alt: DataCube slice after background removal at the central wavelength showing enhanced signal features.
