.. _read_write_example:


Read & Write a DataCube
=======================


The `hsi-wizard` module provides basic functions for reading and writing a DataCube. For more information visit :ref:`loader <loader>` chapter.

.. list-table:: Supported DataCube File Formats
   :header-rows: 1
   :widths: 10 12 14

   * - Extension
     - Read Supported
     - Write Supported
   * - .csv
     - ✅
     - ✅
   * - .xlsx
     - ✅
     - ✅
   * - .tdms
     - ✅
     - ❌
   * - .fsm
     - ✅
     - ❌
   * - .folder
     - ✅
     - ❌
   * - .nrrd
     - ✅
     - ❌
   * - .image
     - ✅
     - ❌
   * - .hdr
     - ✅
     - ✅


.. note::
  The :meth:`wizard.read()` function serves as the main entry point for users. It abstracts the file handling process and automatically determines the appropriate handler based on the file type.

Writing a DataCube
------------------

csv
~~~~
This snippet shows how to generate a random DataCube, write it to a `.csv` file using the :ref:`wizard._utils._loader.csv <csv>` module, and read it back into a new DataCube,
preserving the original data shape and structure.

.. literalinclude:: ../../../../examples/00_first_steps/01_read_write_dc_csv.py

xlsx
~~~~
Similar to the snippet above, this example shows how to generate a random DataCube, write it to a .xlsx file using the :ref:`wizard._utils._loader.xlsx <xlsx>` module, and read it back into a new DataCube.

.. literalinclude:: ../../../../examples/00_first_steps/01_read_write_dc_xlsx.py


