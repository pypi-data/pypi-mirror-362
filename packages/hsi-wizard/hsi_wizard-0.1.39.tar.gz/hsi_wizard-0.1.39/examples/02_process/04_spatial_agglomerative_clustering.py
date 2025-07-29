import wizard
from wizard._utils.example import generate_pattern_stack
from wizard._processing.cluster import spatial_agglomerative_clustering, pca
import matplotlib.pyplot as plt

# generate synthetic data with spatial patterns
data = generate_pattern_stack(8, 150, 150, n_circles=2, n_rects=4, n_triangles=3)

# create a DataCube
dc = wizard.DataCube(data)

# visualize a wavelength slice and the segmentation
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(dc[4])
axes[0].set_title("Original Slice (λ index 4)")
axes[0].set_axis_off()

# pca, because agglomerative donst scale well
dc_reduced = pca(dc, n_components=2)

# apply spatially-constrained agglomerative clustering
labels_agg = spatial_agglomerative_clustering(dc_reduced, n_clusters=7)

axes[1].imshow(labels_agg)
axes[1].set_title("Segmented (Agglomerative + Spatial)")
axes[1].set_axis_off()

plt.tight_layout()
plt.show()
