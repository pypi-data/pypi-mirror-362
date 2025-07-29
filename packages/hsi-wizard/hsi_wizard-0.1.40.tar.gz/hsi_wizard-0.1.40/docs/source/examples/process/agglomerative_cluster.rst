.. _agglomerative_cluster:


Spatial Agglomerative Cluster
=============================

The :meth:`spatial_agglomerative_clustering()` function segments a :class:DataCube by performing hierarchical agglomerative clustering on its spectral signatures with spatial connectivity constraints.

.. warning::
   Agglomerative clustering with spatial connectivity is conceptually elegant, but it doesn’t scale well to large 2D grids, and processing very large datasets can lead to high computing time.


Example
-------

The following example demonstrates spatial agglomerative clustering on a synthetically generated :class:`DataCube`.

.. literalinclude:: ../../../../examples/02_process/04_spatial_agglomerative_clustering.py
   :language: python
   :linenos:


.. figure:: ../../../../resources/imgs/examples/agglomerative.png
   :align: center
   :alt: Result of spatial_agglomerative_clustering on a DataCube.

   The output illustrates how the algorithm merges spectrally similar and spatially adjacent regions, yielding a smooth and interpretable segmentation reflecting both spectral and spatial continuity.

