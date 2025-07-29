import wizard
from wizard._utils.example import generate_pattern_stack
from matplotlib import pyplot as plt

# generate random data
data = generate_pattern_stack(20, 600, 400, seed=123)

# build two cubes: one original, one to resize
dc = wizard.DataCube(data)

# plot them side by side
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# original
axes[0].imshow(dc[10])
axes[0].set_title("Original (600×400)")

dc.resize(500, 500)

# resized
axes[1].imshow(dc[10])
axes[1].set_title("Resized (500×500)")

plt.tight_layout()
plt.show()
