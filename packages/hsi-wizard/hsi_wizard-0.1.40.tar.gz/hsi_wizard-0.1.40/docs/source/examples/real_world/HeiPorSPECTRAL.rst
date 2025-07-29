.. _HeiPorSPECTRAL:

HeiPorSPECTRAL
==============

This example demonstrates the use of the `hsi-wizard` package to process and visualize biomedical hyperspectral data from the `HeiPorSPECTRAL dataset <https://heiporspectral.org>`_.

The focus is on a spleen tissue scan (sample ID: P086#2021_04_15_09_22_02), part of a collection of annotated hyperspectral scans of human organs.
`hsi-wizard` manages the complete pipeline: reading the raw `.dat` hyperspectral cube, handling metadata like wavelength calibration, and applying clustering to segment different tissue types based on spectral signatures.

.. note::

   This example uses data from the `HeiPorSPECTRAL dataset <https://heiporspectral.org>`_, published by Studier-Fischer et al. (2023)

Example
-------

The following script demonstrates how to load and analyze a spleen sample from the HeiPorSPECTRAL dataset using `hsi-wizard`.

.. literalinclude:: ../../../../examples/04_real_word_examples/HeiPorSpectral.py
   :language: python
   :linenos:

.. figure:: ../../../../resources/imgs/examples/wizard_output.png
   :alt: ROI-based spectral analysis with the interactive plotting interface of hsi-wizard.
   :align: center
   :width: 100%

   ROI-based spectral analysis using the interactive plotting interface of `hsi-wizard`.
   The left panel displays selected tissue regions at 696 nm, while the right panel shows the corresponding normalized spectral profiles.

.. figure:: ../../../../resources/imgs/examples/Example_output.png
   :alt: Comparison of manual vs automated segmentation.
   :align: center
   :width: 100%

   Comparison of manual annotation (top-right) from Studier-Fischer et al. (2023) with automated segmentation (bottom-left) using spatial agglomerative clustering (k = 5).
   The RGB image (top-left) and the cluster map (bottom-right) offer context and visual feedback for the clustering result.

