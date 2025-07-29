.. _plot_dc_example:

Plot DataCube
=============

`hsi-wiard` ships with an interactive viewer for `DataCube` objects, allowing you to scroll through spectral layers, define ROIs, and overlay mean spectra.

Actions
-------

- **← / →** : Step through wavelength layers
- **Click (image panel)** : Select single-pixel ROI
- **Drag (image panel)** : Draw rectangular ROI
- **Click (spectrum panel)** : Jump to nearest wavelength
- **Save Plot** : Overlay and save current ROI mean spectrum
- **Remove Plot** : Remove last saved spectrum and ROI overlay
- **Normalize Y (0–1)** : Toggle y-axis normalization of all spectra

Example
-------

.. literalinclude:: ../../../../examples/00_first_steps/02_plot_dc.py


.. figure:: ../../../../resources/imgs/plot_dc.png
   :align: center
   :alt: Example of the plotter function in action.
