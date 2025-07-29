[![Documentation Status](https://readthedocs.org/projects/hsi-wizard/badge/?version=latest)](https://hsi-wizard.readthedocs.io)
[![codecov](https://codecov.io/gh/BlueSpacePotato/hsi-wizard/graph/badge.svg?token=85ASSSF2ZN)](https://codecov.io/gh/BlueSpacePotato/hsi-wizard)
[![Socket Badge](https://socket.dev/api/badge/pypi/package/hsi-wizard/0.1.13?artifact_id=tar-gz)](https://socket.dev/pypi/package/hsi-wizard/overview/0.1.13/tar-gz)
![PyPI - Downloads](https://img.shields.io/pypi/dm/hsi-wizard)
[![PyPI Downloads](https://static.pepy.tech/badge/hsi-wizard)](https://pepy.tech/projects/hsi-wizard)
[![status](https://joss.theoj.org/papers/b79920c171c93c833323cc3e55e56962/status.svg)](https://joss.theoj.org/papers/b79920c171c93c833323cc3e55e56962)

# HSI Wizard

See Beyond the Visible: The Magic of Hyperspectral Imaging for Medical & Bioinformatics Applications

<img src="./resources/imgs/hsi_wizard_logo.svg" alt="hsi_wizard_logo" style="width: 100%">



## Introduction

Welcome to the `hsi-wizard` package! Designed primarily for **medical hyperspectral imaging** and **bioinformatics workflows**, this Python package provides a straightforward environment for hyperspectral imaging (HSI) analysis, supporting everything from basic spectral analysis to advanced machine learning and AI methods. Whether you're working with raw sensor data or pre-processed datasets, `hsi-wizard` offers a suite of tools to simplify and enhance your analysis workflow.

If you're new here, the best place to start is the [documentation](https://hsi-wizard.readthedocs.io), where you'll find detailed instructions on how to begin.

## Features
- DataCube Class for managing and processing HSI data
- Spectral plotting and visualization
- Clustering and spectral analytics
- Tools for merging and processing HSI data
- Data loaders for various file formats (e.g., NRRD, Pickle, TDMS, and XLSX)
- Decorators for method tracking, input validation, and execution time logging

## Geospatial Limitations
This package does not track or process geographical coordinates. If you require full remote-sensing or GIS integration, you may need complementary tools. hsi-wizard focuses on medical and lab-based spectral analysis, so spatial georeferencing is restricted.



## Comparison with Existing Tools
| **Attribute**        | **HSI-Wizard**                                             | **PySptools**                                                                                                 | **HyDe**                                                                                  | **Spectral Python (SPy)**                                                                | **ENVI**                                                         |
| -------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Category**         | Medical Imaging                                            | Geospatial & Research Spectral Analysis                                                                       | Preprocessing & Denoising                                                                 | General-Purpose Data I/O & Basic Handling                                                | Commercial All-rounder                                           |
| **Key Features**     | End-to-end medical pipeline,  DataCube,  Merge & analytics | Endmember extraction, Spectral unmixing,  Low-rank wavelet & DNN denoising,  Energy-efficient implementations | Read/display/manipulate HSI files, Bip/Bil/Bsq interleaves, Basic classification routines | Advanced spectral processing & classification, Full GUI & Python API, ArcGIS integration |                                                                  |
| **File Support**     | ENVI (.hdr/.img), Images, CSV, FSM, NRRD, Pickle (.pkl), TDMS, XLSX          | ENVI (.hdr/.img) via Spectral Python integration                                                              | None built-in (operates on NumPy arrays from user’s loader)                               | ENVI (.hdr/.img), BIL, BIP, BSQ interleaves                                              | ENVI (.hdr/.img), GeoTIFF, HDF, ASCII – broad commercial support |
| **Licensing / Cost** | Open-source (MIT)                                          | Open-source (MIT)                                                                                             | Open-source (BSD-3-Clause)                                                                | Open-source (BSD-3)                                                                      | Proprietary, paid                                                |



---

# Installation

### Requirements
- [Python](https://www.python.org) >3.10

### Via pip

You can install the package via pip:

```bash
pip install hsi-wizard
```

### Compile from Source

Alternatively, you can compile HSI Wizard from source:

```bash
python -m pip install -U pip setuptools wheel            # Install/update build tools
git clone https://github.com/BlueSpacePotato/hsi-wizard   # Clone the repository
cd hsi-wizard                                             # Navigate into the directory
python -m venv .env                                       # Create a virtual environment
source .env/bin/activate                                  # Activate the environment
pip install -e .                                          # Install in editable mode
pip install wheel                                         # Install wheel
pip install --no-build-isolation --editable .             # Compile and install hsi-wizard
```

---

# Usage

After installing the package, you can import the DataCube, read function, and plotter for quick HSI data analysis:

```python3
import wizard

# Load an HSI datacube from a file
dc = wizard.read('path_to_file')

# process DataCube
dc.resize(x_new=500, y_new=500)
dc.remove_background()

# Visualize the datacube
wizard.plotter(dc)
```

For more [examples](https://hsi-wizard.readthedocs.io/examples/index.html) visist the [documentation](https://hsi-wizard.readthedocs.io).

---

# Contributing

We welcome contributions from the medical imaging and bioinformatics communities! To make the collaboration smooth and efficient, please follow the guidelines below:

## Reporting Issues
If you encounter bugs, unexpected behavior, or have feature requests, please:

  1. Search existing issues to see if your problem or idea has already been reported.
  2. Open a new issue with a clear title and description:
     1. Steps to reproduce the problem
     2. Expected vs. actual behavior
     3. Version of hsi-wizard, Python, and operating system
  3. Label the issue appropriately (e.g., bug, feature request, documentation).

## Seeking Support
For usage questions, help with examples, or general discussion:
- GitHub Discussions: Post your questions under the Support category in our Discussions board.

## Contributing Code
If you have ideas or fixes, we’d love your help! Just fork the repo, create your branch, and make your changes. When you’re ready, push your branch up and open a Pull Request against main. We’ll review it and merge it in!


