.. _datacube_ops:

DataCube Operations
===================

.. module:: wizard._core.datacube_ops
    :platform: Unix
    :synopsis: DataCube Operations.

Module Overview
---------------

This module contains functions for processing datacubes. The methods are dynamically added to the DataCube class in its __init__ method. Therefore, they can be used as standalone functions or as methods of the DataCube class.

Functions
---------

.. _remove_spikes:
.. autofunction:: remove_spikes

.. _remove_background:
.. autofunction:: remove_background

.. _resize:
.. autofunction:: resize

.. _baseline_als:
.. autofunction:: baseline_als

.. _merge_cubes:
.. autofunction:: merge_cubes

.. _inverse:
.. autofunction:: inverse

.. _register_layers_simple:
.. autofunction:: register_layers_simple

.. _register_layers_best:
.. autofunction:: register_layers_best

.. _remove_vignetting_poly:
.. autofunction:: remove_vignetting_poly

.. _remove_vignetting:
.. autofunction:: remove_vignetting

.. _upscale_datacube_edsr:
.. autofunction:: upscale_datacube_edsr

.. _upscale_datacube_espcn:
.. autofunction:: upscale_datacube_espcn



