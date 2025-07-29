.. _smooth_kmeans:


Smooth Kmeans
=============

The :meth:`smooth_kmeans()` function performs a hybrid segmentation on a DataCube using KMeans clustering followed by spatial smoothing via Markov Random Field (MRF) regularization.

Example
-------

This examples shows the clustering of a syntic generated DataCube.

.. literalinclude:: ../../../../examples/02_process/01_smooth_kmeans.py
   :language: python
   :linenos:


.. figure:: ../../../../resources/imgs/examples/smooth_kmeans.png
   :align: center
   :alt: Cluster DataCube with smooth_kmeans().

   The output demonstrates how spectral features and spatial structure are simultaneously captured in the segmentation result.


