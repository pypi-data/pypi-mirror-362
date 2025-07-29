import os
import wizard
from matplotlib import pyplot as plt
from mpmath.libmp import normalize
from rich.progress import track
from pathlib import Path

import numpy as np


fl = '/Users/flx/Documents/Mulitscanner/Data/Images/Mice_Brain/FL_Imager_gold/BrainGold1'
print('FL-Imager:')
fl_dc = wizard.read(fl, normalize=True)
# fl_dc.register_layers()
# fl_dc.inverse()

print('\t- remove vingetting')
fl_dc.remove_vignetting(sigma=100)

print('\t- remove Background')
fl_dc.remove_background()

print('\t- normalize')
fl_dc.normalize()

# print('\tresize')
# fl_dc.resize(x_new=mir_dc.shape[2], y_new=mir_dc.shape[1])
wizard.plotter(fl_dc)

mir = '/Users/flx/Documents/Mulitscanner/Data/Images/Mice_Brain/MIR_gold/Mice Brain gold 2'
print('mir')
mir_dc = wizard.read(mir)
mir_dc.remove_background(style='bright')
# mir_dc.register_layers()
mir_dc.normalize()
mir_dc.set_cube(np.flip(mir_dc.cube, axis=(1, 2)))
# print(mir_dc.shape)
# wizard.plotter(mir_dc)

mir_dc.resize(x_new=fl_dc.shape[2], y_new=fl_dc.shape[1])
mir_dc.set_cube(1-mir_dc.cube)
print(mir_dc.cube.max(), mir_dc.cube.min())
mir_dc.normalize()
wizard.plotter(mir_dc)

print('merge')
fl_dc.merge_cubes(mir_dc)
fl_dc.normalize()
fl_dc.register_layers_best(max_features=10000, scale_thresh=3.)
print(fl_dc.shape)

wizard.plotter(fl_dc)

print('Done')
