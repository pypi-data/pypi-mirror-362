import wizard
import numpy as np
from matplotlib import pyplot as plt

dc = wizard.DataCube(cube=np.random.rand(12, 100, 120))

kmeans = wizard._processing.cluster.segment_cube(dc)
# kmeans = wizard._processing.cluster.isodata(dc)

plt.imshow(kmeans)
plt.show()
