import wizard
from wizard._utils.example import generate_pattern_stack
from wizard._processing.cluster import spectral_spatial_kmeans
import matplotlib.pyplot as plt

# generate synthetic data with spatial patterns
data = generate_pattern_stack(12, 400, 400, n_circles=5, n_rects=3, n_triangles=1)

# create a DataCube
dc = wizard.DataCube(data)

# apply spectral–spatial KMeans clustering
labels = spectral_spatial_kmeans(dc, n_clusters=4, spatial_radius=2)

# visualize a wavelength slice and the segmentation
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(dc[7])
axes[0].set_title("Original Slice (λ index 7)")
axes[0].set_axis_off()

axes[1].imshow(labels)
axes[1].set_title("Segmented (Spectral–Spatial KMeans)")
axes[1].set_axis_off()

plt.tight_layout()
plt.show()
