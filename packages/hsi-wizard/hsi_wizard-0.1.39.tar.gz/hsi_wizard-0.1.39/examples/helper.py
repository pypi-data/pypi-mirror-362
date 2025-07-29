import numpy as np

def _draw_circle(mask, center, radius):
    """Set mask[y,x] = 1 inside the given circle."""
    H, W = mask.shape
    yy, xx = np.ogrid[:H, :W]
    cy, cx = center
    circle = (yy - cy)**2 + (xx - cx)**2 <= radius**2
    mask[circle] = 1


def _draw_rectangle(mask, top_left, size):
    """Set mask[y,x] = 1 inside the given rectangle."""
    H, W = mask.shape
    y0, x0 = top_left
    h, w = size
    y1 = min(H, y0 + h)
    x1 = min(W, x0 + w)
    mask[y0:y1, x0:x1] = 1


def _draw_triangle(mask, vertices):
    """Set mask[y,x] = 1 inside the triangle defined by 3 (y,x) verts."""
    H, W = mask.shape
    yy, xx = np.mgrid[:H, :W]
    v0, v1, v2 = [np.array(v) for v in vertices]
    denom = ((v1[1]-v2[1])*(v0[0]-v2[0]) + (v2[0]-v1[0])*(v0[1]-v2[1]))
    a = ((v1[1]-v2[1])*(yy-v2[0]) + (v2[0]-v1[0])*(xx-v2[1])) / denom
    b = ((v2[1]-v0[1])*(yy-v2[0]) + (v0[0]-v2[0])*(xx-v2[1])) / denom
    c = 1 - a - b
    tri = (a>=0)&(b>=0)&(c>=0)
    mask[tri] = 1


def generate_pattern_stack(v, height, width,
                           n_circles=10, n_triangles=8, n_rects=6,
                           circle_base=0.4, tri_base=0.2, rect_base=0.6,
                           variation=0.05, noise_std=0.05,
                           seed=None):
    """
    Returns a (v, height, width) stack of grayscale images with:
    • a black background
    • random circles, triangles & rectangles of varying sizes
    • each shape family using its base intensity (circle_base, tri_base, rect_base)
      plus a small random ±variation per shape
    • Gaussian noise added independently to each layer
    • if shapes overlap, final pixel takes the maximum intensity (no additive overlap)
    """
    if seed is not None:
        np.random.seed(seed)

    # create shape masks and random intensities
    masks = []
    intensities = []

    def rand_pt(margin=0):
        return (np.random.randint(margin, height-margin),
                np.random.randint(margin, width-margin))

    # circles
    for _ in range(n_circles):
        m = np.zeros((height, width), bool)
        r = np.random.randint(min(height, width)*5//100,
                              min(height, width)*15//100)
        center = rand_pt(margin=r+1)
        _draw_circle(m, center, r)
        masks.append(m)
        val = np.clip(circle_base + np.random.uniform(-variation, variation), 0, 1)
        intensities.append(val)

    # triangles
    for _ in range(n_triangles):
        m = np.zeros((height, width), bool)
        r = np.random.randint(min(height, width)*5//100,
                              min(height, width)*15//100)
        cy, cx = rand_pt(margin=r+1)
        v0 = (cy - r, cx)
        v1 = (cy + r//2, cx - int(r*0.866))
        v2 = (cy + r//2, cx + int(r*0.866))
        _draw_triangle(m, [v0, v1, v2])
        masks.append(m)
        val = np.clip(tri_base + np.random.uniform(-variation, variation), 0, 1)
        intensities.append(val)

    # rectangles
    for _ in range(n_rects):
        m = np.zeros((height, width), bool)
        h = np.random.randint(height*5//100, height*20//100)
        w = np.random.randint(width*5//100, width*20//100)
        top_left = rand_pt(margin=max(h, w)+1)
        _draw_rectangle(m, top_left, (h, w))
        masks.append(m)
        val = np.clip(rect_base + np.random.uniform(-variation, variation), 0, 1)
        intensities.append(val)

    # compute base layer using maximum overlap
    base_layer = np.zeros((height, width), float)
    for m, I in zip(masks, intensities):
        base_layer = np.maximum(base_layer, m * I)

    # build stack with independent noise per layer (no gradient)
    stack = np.zeros((v, height, width), float)
    for i in range(v):
        noise = np.random.normal(0, noise_std, size=base_layer.shape)
        stack[i] = np.clip(base_layer + noise, 0, 1)

    return stack


if __name__ == "__main__":
    import wizard

    v, H, W = 20, 400, 600
    stack = generate_pattern_stack(v, H, W,
                                   n_circles=12,
                                   n_triangles=10,
                                   n_rects=8,
                                   seed=42)

    dc = wizard.DataCube(stack)
    wizard.plotter(dc)
