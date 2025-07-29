.. _plotter:

Plotter
-------

.. module:: wizard._exploration.plotter
   :platform: Unix
   :synopsis: Interactive plotting interface for hyperspectral DataCube objects.

Module Overview
===============

The `plotter` module provides an interactive visualization interface for `DataCube` objects
in the HSI Wizard package. Users can step through wavelength layers, define regions of
interest (ROIs), compute mean spectra, normalize data, and save or remove ROI-based
spectral plots.

Interactive Controls
====================

- **Left/Right arrow keys**: Step through wavelength layers.
- **Mouse click on image panel**: Select a single-pixel ROI at the cursor location.
- **Rectangle drag on image panel**: Define a custom ROI region.
- **Click on spectrum panel**: Jump to the nearest wavelength layer based on clicked wavelength.
- **Save Plot button**: Save the current ROI mean spectrum, overlaid with a unique semi-transparent color.
- **Remove Plot button**: Remove the most recently saved ROI spectrum and its rectangle overlay.
- **Normalize Y (0–1) checkbox**: Toggle normalization of all spectra on the Y-axis between 0 and 1.

Function: wizard.plotter(dc)
============================

.. autofunction:: wizard._exploration.plotter.plotter


Example Usage
=============

The following example demonstrates how to use the `plotter` function:

.. literalinclude:: ../../../../examples/00_first_steps/02_plot_dc.py
   :language: python
   :linenos:

.. figure:: ../../../../resources/imgs/plot_dc.png
   :align: center
   :alt: Example of the plotter function in action.

   Interactive example of hyperspectral data visualization using the `plotter` function.
