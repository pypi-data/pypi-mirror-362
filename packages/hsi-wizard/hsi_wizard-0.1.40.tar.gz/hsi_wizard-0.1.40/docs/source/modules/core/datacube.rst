.. _datacube:

DataCube
========
.. module:: datacube
   :platform: Unix
   :synopsis: DataCube class for storing hyperspectral imaging (HSI) data.

Module Overview
---------------
This module provides the `DataCube` class, which is used to store hyperspectral imaging (HSI) data. The `DataCube` is a 3D array where the x and y axes represent pixels, and the v axis stores measured values like counts or wavelengths.

Class DataCube
--------------
.. class:: DataCube(cube=None, wavelengths=None, name=None, notation=None, record=False)

   The `DataCube` class stores hyperspectral imaging (HSI) data as a 3D array.

   :param cube: 3D numpy array representing the data cube. Default is None.
   :type cube: np.ndarray, optional
   :param wavelengths: List of wavelengths corresponding to the `v` axis of the data cube.
   :type wavelengths: list | np.ndarray, optional
   :param name: Name of the data cube. Default is None.
   :type name: str, optional
   :param notation: Specifies whether the wavelength data is in nm or cm⁻¹. Default is None.
   :type notation: str, optional
   :param record: If True, execution of the methods will be recorded. Default is False.
   :type record: bool, optional


.. warning::
   Warning: DataCube does not perform automatic validation of the array’s shape or check that you’ve used the correct (`v`, `x`, `y`) ordering. It assumes you know your data structure and provides no spectral/spatial checks under the hood. Incorrectly ordered or shaped arrays may lead to unexpected results.


Methods
-------

.. method:: __add__(other)

   Add two `DataCube` instances along the `v` axis.

   :param other: Another `DataCube` instance to add.
   :type other: DataCube
   :raises ValueError: If dimensions do not match or data is None.
   :return: New `DataCube` instance with combined data.
   :rtype: DataCube

.. method:: __len__()

   Return the number of layers (v dimension) in the data cube.

   :return: Number of layers in the data cube.
   :rtype: int

.. method:: __getitem__(idx)

   Retrieve an item from the data cube.

   :param idx: Index of the item to retrieve.
   :type idx: int
   :return: Selected item from the data cube.
   :rtype: np.ndarray

.. method:: __setitem__(idx, value)

   Set an item in the data cube.

   :param idx: Index where the value should be set.
   :type idx: int
   :param value: Value to be set at the given index.
   :type value: np.ndarray

.. method:: __str__()

   Return a string representation of the `DataCube`.

   :return: String containing information about the data cube.
   :rtype: str

.. method:: set_name(name)

   Set a name for the DataCube.

   :param name: Name as a string.
   :type name: str
   :raises AttributeError: If the input is not a string.

.. method:: set_wavelengths(wavelengths)

   Set wavelength data for the `DataCube`.

   :param wavelengths: 1D numpy array or list of wavelength data.
   :type wavelengths: list | np.ndarray
   :raises AttributeError: If the input is not a 1D array or list.

.. method:: set_cube(cube)

   Set data for the `DataCube`.

   :param cube: 2D, 3D, or 4D numpy array of data.
   :type cube: np.ndarray
   :raises AttributeError: If the input cube is not valid.

.. method:: set_notation(notation)

   Update the notation for the DataCube.

   :param notation: Notation describing wavelength units, such as 'nm' or 'cm⁻¹'.
   :type notation: str

.. method:: start_recording()

   Start recording method execution for the `DataCube`.

.. method:: stop_recording()

   Stop recording method execution for the `DataCube`.

.. method:: save_template(filename)

   Save a template of recorded methods to a YAML file.

   :param filename: Name of the YAML file where the template will be saved.
   :type filename: str
   :raises AttributeError: If filename is invalid.

.. method:: execute_template(filename)

   Load a template and execute the corresponding methods.

   :param filename: Name of the YAML file containing the template.
   :type filename: str
