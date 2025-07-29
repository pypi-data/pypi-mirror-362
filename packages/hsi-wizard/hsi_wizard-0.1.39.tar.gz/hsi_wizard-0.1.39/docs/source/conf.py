# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the path to the parent directory of 'wizard'
sys.path.insert(0, os.path.abspath('../../'))
print(f"Using Python interpreter: {sys.executable}")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'hsi-wizard'
copyright = '2024, Felix Wuehler'
author = 'Felix Wuehler'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # For Google and NumPy style docstrings
    'sphinx.ext.autodoc.typehints',  # For type hints in function signatures
    'sphinx.ext.viewcode',  # To link to source code
    'sphinx_exec_code'
]

templates_path = ['_templates']
exclude_patterns = []

# Include type hints in parameter descriptions
autodoc_typehints = "description"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

#  Explicitly set the problematic options in conf.py to their default or desired values
html_permalinks_icon = "¶"  # Default value
jquery_use_sri = False  # Disable SRI for jQuery

# Mock imports for unavailable or optional dependencies
autodoc_mock_imports = ['nrrd', 'rich'] 