import wizard
from wizard._utils.example import generate_pattern_stack
from matplotlib import pyplot as plt

# generate random data
data = generate_pattern_stack(20, 600, 400, n_circles=10, n_rects=0, n_triangles=0)

# build two cubes: one original, one to resize
dc = wizard.DataCube(data)

# plot them side by side
fig, axes = plt.subplots(1, 3, figsize=(12, 6))

# original
axes[0].imshow(dc[10])
axes[0].set_title("Original")

dc.remove_background(style='dark')

# resized
axes[1].imshow(dc[10])
axes[1].set_title("Removed Background `dark`")

dc.remove_background(style='bright')

axes[2].imshow(dc[10])
axes[2].set_title("Removed Background `bright`")

plt.tight_layout()
plt.show()
