import wizard
from wizard._utils.example import generate_pattern_stack
from wizard._processing.cluster import kmeans
import matplotlib.pyplot as plt

# generate synthetic data with spatial patterns
data = generate_pattern_stack(20, 250, 350, n_circles=3, n_rects=3, n_triangles=2)

# create a DataCube
dc = wizard.DataCube(data)

# apply plain KMeans clustering
labels_km = kmeans(dc, n_clusters=4, n_init=25)

# visualize a wavelength slice and the segmentation
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(dc[12])
axes[0].set_title("Original Slice (λ index 12)")
axes[0].set_axis_off()

axes[1].imshow(labels_km)
axes[1].set_title("Segmented (KMeans)")
axes[1].set_axis_off()

plt.tight_layout()
plt.show()
