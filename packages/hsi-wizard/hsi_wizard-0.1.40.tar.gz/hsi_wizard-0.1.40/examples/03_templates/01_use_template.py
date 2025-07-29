import wizard
from wizard._utils.example import generate_pattern_stack
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(10, 8))

# Apply template to new DataCube
# Create synthetic data and initialize DataCube
data2 = generate_pattern_stack(20, 300, 300, n_circles=10, n_rects=0, n_triangles=0, seed=43)
dc2 = wizard.DataCube(data2)

# Plot before processing
axes[0].imshow(dc2.cube[10], cmap='viridis', aspect='auto')
axes[0].set_title("Before Processing DC2")

dc2.execute_template("template.yml")

# Plot after processing
axes[1].imshow(dc2.cube[10], cmap='viridis', aspect='auto')
axes[1].set_title("After Processing DC2")

# Show final plot
plt.tight_layout()
plt.show()