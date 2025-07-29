import os

import wizard
import numpy as np
from wizard._utils._loader import csv

# define dc
dc = wizard.DataCube(np.random.rand(22, 10,8))

# wrtie dc to xlsx csv
csv._write_csv(dc, filename='test.csv')

# read dc from csv
new_dc = csv._read_csv('test.csv')

# compare data
print(dc.shape)
print(new_dc.shape)

# delete files
os.remove('test.csv')

