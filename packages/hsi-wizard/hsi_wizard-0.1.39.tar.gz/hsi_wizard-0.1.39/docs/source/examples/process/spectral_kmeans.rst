.. _spectral_kmeans:


Spectral Spatial Kmeans
=======================

The :meth:`spectral_spatial_kmeans()` function performs a hybrid segmentation on a :class:`DataCube` by first clustering spectral signatures with standard KMeans
and then enforcing spatial coherence through Markov Random Field (MRF) regularization. Initially, each pixel’s spectrum is assigned to one of K clusters based
solely on spectral distance. Subsequently, a smoothing step refines labels to encourage neighboring pixels to share the same cluster, reducing salt-and-pepper
noise and emphasizing spatially contiguous regions.

Example
-------

The following example demonstrates spectral–spatial KMeans on a synthetically generated :class:`DataCube`.

.. literalinclude:: ../../../../examples/02_process/03_spectral_spatial_kmeans.py
   :language: python
   :linenos:


.. figure:: ../../../../resources/imgs/examples/spectral_sapital_kmeans.png
   :align: center
   :alt: Cluster DataCube with smooth_kmeans().

   The result highlights how pure spectral clustering followed by spatial smoothing yields segments that honor both spectral similarity and contiguous spatial patterns.

