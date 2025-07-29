.. _create_dc_example:

Create a DataCube
=================

A :ref:`DataCube <DataCube>` is a specialized class for hyperspectral data, combining spectral and spatial information into a single object. Internally, it stores your measurements as a NumPy array of shape (`v`, `x`, `y`), where:

   * `v` is the number of spectral channels (e.g., different wavelengths),
   * `x and `y` are the spatial dimensions (e.g., image width and height).

The optinonal accompanying attribute wavelength is a list of length v, in which the wavelength corresponding to the individual spectral slices is specified. If no wavelengths are passed, a wavelength attribute from 0 to `v` is automatically set.

In many workflows, your data may already reside in a NumPy array. This example demonstrates how to wrap an existing array in a DataCube, making it easy to integrate with analysis routines without first writing out to a file. Simply pass your array and the matching wavelength list directly to the constructor.


.. warning::
   Warning: DataCube does not perform automatic validation of the array’s shape or check that you’ve used the correct (`v`, `x`, `y`) ordering. It assumes you know your data structure and provides no spectral/spatial checks under the hood. Incorrectly ordered or shaped arrays may lead to unexpected results.


Example
-------

   .. literalinclude:: ../../../../examples/00_first_steps/00_array_to_dc.py




