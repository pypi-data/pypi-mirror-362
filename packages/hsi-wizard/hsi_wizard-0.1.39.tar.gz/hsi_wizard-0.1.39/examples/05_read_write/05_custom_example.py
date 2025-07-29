import wizard
import os
import numpy as np
import re
from matplotlib import pyplot as plt
from natsort import natsorted

# Define the folder path
folder = 'hsi-open-dataset/data/coffee'

# Check if the folder exists and otherwise download datset
if  os.path.exists(folder) and any(f.endswith(('.png')) for f in os.listdir(folder)):
    print("Folder exists and contains images. Skipping download.")
else:
    print("Folder does not exist or contains no images. Downloading...")
    os.system("git clone --depth 1 --filter=blob:none --sparse https://github.com/hacarus/hsi-open-dataset.git && cd hsi-open-dataset && git sparse-checkout set data/coffee")


# creating a loading function
def custom_reader(path:str) -> wizard.DataCube:

    _cube = None
    _wavelengths = None
    _name = '05_example'
    _notation = None
    match = None

    # list files
    files = natsorted(os.listdir(path))

    # get shape of images
    img_shape = np.array(plt.imread(os.path.join(path, files[0]))).shape

    # creat cube data
    _cube = np.zeros(shape=(len(files), img_shape[0], img_shape[1]))

    # create wavelengths
    _wavelengths = []

    # loop data
    for idx, file in enumerate(files):
        _cube[idx] = plt.imread(os.path.join(path, file))
        match = re.search(r'_(\d+)([a-zA-Z]+)', file)
        _wavelengths.append(int(match.group(1)))

    if match.group(2):
        _notation = match.group(2)

    return wizard.DataCube(cube=_cube, wavelengths=_wavelengths, name=_name, notation=_notation)


dc = wizard.DataCube()
dc.set_custom_reader(custom_reader)

dc.custom_read(path='hsi-open-dataset/data/coffee')
print(dc)
wizard.plotter(dc)
