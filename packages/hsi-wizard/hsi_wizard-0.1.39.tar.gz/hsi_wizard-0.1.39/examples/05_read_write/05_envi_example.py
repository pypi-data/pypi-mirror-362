import wizard
from wizard._utils._loader import hdr
from wizard._utils.example import generate_pattern_stack

# define dc
data = generate_pattern_stack(20, 300, 300, n_circles=10, n_rects=0, n_triangles=0, seed=42)
dc = wizard.DataCube(data)

# wrtie dc to envi
hdr._write_hdr(dc, 'test.hdr')

# read envi back in
dc = wizard.read(path='test.hdr', image_path='test.img')

# plot data
wizard.plotter(dc)


