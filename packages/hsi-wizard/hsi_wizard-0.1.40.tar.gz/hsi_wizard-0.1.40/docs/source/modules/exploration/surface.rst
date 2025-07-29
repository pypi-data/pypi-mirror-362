.. _surface:

Surface Plotter
===============

Overview
--------

The Surface Plotter module offers an interactive 3D visualization interface for DataCube objects. By combining slicing, threshold-based opacity control, and real-time rotation, it enables in-depth exploration of spatial and spectral features in chemical imaging datasets. This tool is particularly useful for applications such as mapping molecule concentration gradients in engineering processes.

Function: wizard.plot_surface(dc)
---------------------------------

.. autofunction:: wizard._exploration.surface.plot_surface

Paper Reference
---------------

The Surface Plotter was employed in the study `Three-Dimensional, Molecule-Sensitive Mapping of Structured Falling Liquid Films Using Raman Scanning <https://doi.org/10.1002/cite.202300048>`_. Below is the graphical abstract linked to the full paper:

.. figure:: https://onlinelibrary.wiley.com/cms/asset/82d41b4e-e935-4bc0-af07-07623713e130/cite202300048-fig-0002-m.jpg
   :target: https://doi.org/10.1002/cite.202300048
   :align: center
   :alt: Graphical abstract of "Three-Dimensional, Molecule-Sensitive Mapping of Structured Falling Liquid Films Using Raman Scanning"

   Three-Dimensional, Molecule-Sensitive Mapping of Structured Falling Liquid Films Using Raman Scanning, by `Nachtmann et al. <https://doi.org/10.1002/cite.202300048>`_


Example Usage
-------------

.. literalinclude:: ../../../../examples/06_plot_surface/06_example.py
   :language: python
   :linenos:

.. figure:: ../../../../resources/imgs/surface_example.png
   :align: center
   :alt: Example of the surface plotter function in action.

   Example of the surface plotter function in action.

