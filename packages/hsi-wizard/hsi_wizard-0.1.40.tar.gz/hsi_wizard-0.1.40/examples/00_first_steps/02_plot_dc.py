import wizard
from wizard._utils.example import generate_pattern_stack

# generate randome data
data = generate_pattern_stack(20, 600, 400)

# creating some radnome data
dc = wizard.DataCube(data)

# plot data
wizard.plotter(dc)