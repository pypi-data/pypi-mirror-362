import wizard
from wizard._utils.example import generate_pattern_stack
import matplotlib.pyplot as plt

# Prepare plot
fig, axes = plt.subplots(1, 2, figsize=(10, 8))

# Create synthetic data and initialize DataCube
data1 = generate_pattern_stack(20, 300, 300, n_circles=10, n_rects=0, n_triangles=0, seed=42)
dc1 = wizard.DataCube(data1)

# Plot before processing
axes[0].imshow(dc1.cube[10], cmap='viridis', aspect='auto')
axes[0].set_title("Before Processing DC1")

# Record and apply processing
dc1.start_recording()
dc1.resize(x_new=500, y_new=300)
dc1.remove_background()

# Plot after processing
axes[1].imshow(dc1.cube[10], cmap='viridis', aspect='auto')
axes[1].set_title("After Processing DC1")

# Save template for reuse
dc1.save_template("template.yml")

# show data
plt.tight_layout()
plt.show()
