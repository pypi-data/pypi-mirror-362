import wizard
from wizard._utils.example import generate_pattern_stack
from wizard._processing.cluster import isodata
import matplotlib.pyplot as plt

# generate synthetic data with spatial patterns
data = generate_pattern_stack(15, 300, 300, n_circles=4, n_rects=2, n_triangles=2)

# create a DataCube
dc = wizard.DataCube(data)

# apply ISODATA clustering
labels_iso = isodata(dc, k=5, it=25, p=4)

# visualize a wavelength slice and the segmentation
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(dc[10])
axes[0].set_title("Original Slice (λ index 10)")
axes[0].set_axis_off()

axes[1].imshow(labels_iso)
axes[1].set_title("Segmented (ISODATA)")
axes[1].set_axis_off()

plt.tight_layout()
plt.show()
