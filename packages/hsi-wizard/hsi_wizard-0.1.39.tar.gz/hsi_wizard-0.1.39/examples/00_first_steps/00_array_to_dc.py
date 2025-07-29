"""
Create and demonstrate DataCube creation and indexing.

This example shows how to wrap an existing NumPy array in a DataCube,
inspect its core attributes, specify custom wavelength values, and
extract spatial slices at a given wavelength index using two indexing methods.
"""
import wizard
import numpy as np

# Generate a dummy hyperspectral dataset with 20 bands and 8×9 pixels
data = np.zeros(shape=(20, 8, 9))

# Create a DataCube with default wavelengths (0–19)
dc = wizard.DataCube(data, name='Hello DataCube')
print(dc)

# Inspect core attributes
print("Wavelength values:", dc.wavelengths)

# Create a DataCube with custom wavelength assignments (400–700 nm)
custom_wls = np.linspace(400, 700, data.shape[0], dtype='int').tolist()
dc_vis = wizard.DataCube(data, name='Visible Spectrum Cube', wavelengths=custom_wls)
print("\n", dc_vis)
print("Wavelength values:", dc_vis.wavelengths)
