.. _smooth:


Smooth
======

The :meth:`smooth()` function refines a label map (e.g., output of a clustering algorithm) by applying Gaussian filtering iteratively.

Example
-------

The following example shows smoothing of cluster labels on a synthetically generated :class:`DataCube` segmentation.

.. literalinclude:: ../../../../examples/02_process/06_smooth.py
   :language: python
   :linenos:


.. figure:: ../../../../resources/imgs/examples/smooth.png
   :align: center
   :alt: Cluster DataCube with smooth_kmeans().

   The output demonstrates how Gaussian filtering with multiple iterations produces cleaner, more spatially coherent segment boundaries.

