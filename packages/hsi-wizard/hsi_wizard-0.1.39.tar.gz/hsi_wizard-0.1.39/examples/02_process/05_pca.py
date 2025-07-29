import wizard
from wizard._processing.cluster import pca
from wizard._utils.example import generate_pattern_stack

data = generate_pattern_stack(50, 200, 200, n_circles=2, n_rects=2, n_triangles=2)
dc = wizard.DataCube(data)

# reduce to 10 components
dc_reduced = pca(dc, n_components=10)
print("Reduced cube shape:", dc_reduced.cube.shape)
