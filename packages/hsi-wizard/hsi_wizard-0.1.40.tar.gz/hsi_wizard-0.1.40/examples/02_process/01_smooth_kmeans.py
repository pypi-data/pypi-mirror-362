import wizard
from wizard._utils.example import generate_pattern_stack
from wizard import smooth_kmeans
import matplotlib.pyplot as plt

# generate synthetic data with spatial patterns
data = generate_pattern_stack(10, 600, 400, n_circles=3, n_rects=3, n_triangles=3)

# create a DataCube
dc = wizard.DataCube(data)

# apply hybrid segmentation
segmentation = smooth_kmeans(dc, n_clusters=4, mrf_iterations=5, kernel_size=12, sigma=1.0)

# visualize a wavelength slice and the segmentation
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(dc[5])
axes[0].set_title("Original Slice (λ index 5)")
axes[0].set_axis_off()

axes[1].imshow(segmentation)
axes[1].set_title("Segmented (KMeans + MRF)")
axes[1].set_axis_off()

plt.tight_layout()
plt.show()
