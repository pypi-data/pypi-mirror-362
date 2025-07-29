"""
Demonstrate DataCube XLSX serialization and deserialization.
"""

import os
import wizard
import numpy as np
from wizard._utils._loader import xlsx

# generate a random DataCube with 22 spectral bands and a 10×8 spatial grid
dc = wizard.DataCube(np.random.rand(22, 10, 8))

# write the DataCube to 'test.xlsx'
xlsx._write_xlsx(dc, filename='test.xlsx')

# load DataCube directly from the xlsx file
new_dc = xlsx._read_xlsx('test.xlsx')

# confirm that the read-back DataCube matches the original shape
print(new_dc.shape)