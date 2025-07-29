.. _isodata:


Isodata
=======

The :meth:`isodata()` function segments a :class:DataCube using the ISODATA algorithm—a variant of KMeans that iteratively splits and merges clusters based on spectral variance and cluster population.


Example
-------

The following example illustrates the use of :meth:`isodata()` on a synthetically generated :class:`DataCube`.

.. literalinclude:: ../../../../examples/02_process/02_isodata.py
   :language: python
   :linenos:


.. figure:: ../../../../resources/imgs/examples/isodata.png
   :align: center
   :alt:  Result of isodata() on a DataCube.

   The output shows how ISODATA adaptively determines cluster counts and captures both subtle and broad spectral patterns within spatially coherent regions.

