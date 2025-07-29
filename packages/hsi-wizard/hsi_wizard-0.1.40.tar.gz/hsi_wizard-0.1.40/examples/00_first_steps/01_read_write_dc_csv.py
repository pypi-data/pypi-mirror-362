"""
Demonstrate DataCube CSV serialization and deserialization.
"""

import wizard
import numpy as np
from wizard._utils._loader import csv

# generate a random DataCube with 22 spectral bands and a 10×8 spatial grid
dc = wizard.DataCube(np.random.rand(22, 10, 8))

# write the DataCube to 'test.csv'
csv._write_csv(dc, filename='test.csv')

# load DataCube directly using wizard.read
new_dc = wizard.read('test.csv')
# csv._read_csv also works
# new_dc = csv._read_csv('test.csv')

# confirm that the read-back DataCube matches the original shape
print(new_dc.shape)
