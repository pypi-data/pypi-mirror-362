import wizard
from wizard._utils.example import generate_pattern_stack
from wizard._processing.cluster import kmeans, smooth_cluster
import matplotlib.pyplot as plt

# generate synthetic data with spatial patterns
data = generate_pattern_stack(20, 250, 350, n_circles=3, n_rects=3, n_triangles=2)

# create a DataCube
dc = wizard.DataCube(data)

# apply plain KMeans clustering
labels = kmeans(dc, n_clusters=4, n_init=25)

# apply Gaussian smoothing to the raw label map
smoothed_labels = smooth_cluster(labels, sigma=.6, n_iter=2)

# visualize a wavelength slice, raw labels, and smoothed labels
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(dc[5])
axes[0].set_title("Original Slice (λ index 5)")
axes[0].axis("off")

axes[1].imshow(labels)
axes[1].set_title("Raw KMeans Labels")
axes[1].axis("off")

axes[2].imshow(smoothed_labels)
axes[2].set_title("Smoothed Labels")
axes[2].axis("off")

plt.tight_layout()
plt.show()
