.. _wizard:

Overview
========

The core functionality of `hsi-wizard` includes:

- **DataCube Class**: Manage, track, and process HSI data using a powerful object-oriented model
- **Spectral Visualization**: Plot and explore spectral data through interactive and static visualizations
- **Clustering and Analytics**: Apply clustering techniques and perform exploratory data analysis
- **File Format Support**: Seamless integration with various formats, including `.nrrd`, `.pickle`, `.csv`, and `.xlsx`

For a detailed breakdown of each module, refer to the :ref:`Modules <Modules>` section below.

Installation
============

You can install `hsi-wizard` via pip or compile it from source.

Install via pip
---------------
To install the latest release using pip:

.. code-block:: console

   pip install hsi-wizard

Install from Source
-------------------
To install from source:

.. code-block:: console

   python -m pip install -U pip setuptools wheel             # Install/update build tools
   git clone https://github.com/BlueSpacePotato/hsi-wizard   # Clone the repository
   cd hsi-wizard                                             # Navigate into the project directory
   python -m venv .venv                                      # Create a virtual environment
   source .venv/bin/activate                                 # Activate the environment
   pip install -e .                                          # Install in editable mode


Comparison with with Existing Tools
===================================

.. list-table:: Comparison of Hyperspectral Imaging (HSI) Tools
   :header-rows: 1

   * - Attribute
     - HSI-Wizard
     - PySptools
     - HyDe
     - Spectral Python (SPy)
     - ENVI
   * - Category
     - Medical Imaging
     - Geospatial & Research
       Spectral Analysis
     - Preprocessing & Denoising
     - General-Purpose Data
       I/O & Basic Handling
     - Commercial All-rounder
   * - Key Features
     - End-to-end medical pipeline,
       DataCube support, merging & analytics
     - Endmember extraction,
       spectral unmixing,
       wavelet & DNN denoising,
       energy-efficient implementations
     - Read/display/manipulate HSI files,
       BIP/BIL/BSQ formats,
       basic classification tools
     - Advanced spectral
       processing & classification,
       full GUI & Python API,
       ArcGIS integration
     - ENVI (.hdr/.img), GeoTIFF, HDF,
       ASCII – extensive commercial support
   * - File Support
     - ENVI (.hdr/.img), images, CSV, FSM,
       NRRD, Pickle (.pkl), TDMS, XLSX
     - ENVI (.hdr/.img)
     - None built-in (requires user-defined NumPy loaders)
     - ENVI (.hdr/.img), BIL, BIP, BSQ
     - ENVI (.hdr/.img), GeoTIFF,
       HDF, ASCII – broad support
   * - Licensing / Cost
     - Open-source (MIT)
     - Open-source (MIT)
     - Open-source (BSD-3-Clause)
     - Open-source (BSD-3)
     - Proprietary, paid

Geospatial limitation
=====================

This package does not support geospatial tracking or coordinate processing. If you require GIS integration or full remote-sensing capabilities, consider complementary tools.

Contributing
============

We welcome contributions from the medical imaging and bioinformatics communities! Please follow these guidelines to help streamline collaboration.

Reporting Issues
----------------
To report bugs, unexpected behavior, or feature requests:

1. Search existing issues to check for duplicates
2. Open a new issue with:
   - Clear title and description
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Version details (hsi-wizard, Python, OS)
3. Add appropriate labels (e.g., bug, enhancement, documentation)

Getting Help
------------
For help with examples, usage questions, or general discussion:

- GitHub Discussions: Post under the Support category in our `Discussions <https://github.com/BlueSpacePotato/hsi-wizard/discussions>`_ board.

Contributing Code
-----------------
If you want to contribute code:

1. Fork the repository and create a new branch
2. Make your changes with clear commits
3. Push your branch and open a Pull Request against `main`
4. We'll review your contribution and provide feedback or merge

