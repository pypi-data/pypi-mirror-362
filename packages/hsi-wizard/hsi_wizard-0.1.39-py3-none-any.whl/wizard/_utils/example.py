import numpy as np


def _draw_circle(mask, center, radius):
    """
    Draws a filled circle on the given binary mask.

    Sets the values inside the circle defined by the center and radius to 1.

    Parameters
    ----------
    mask : ndarray
        A 2D NumPy array where the circle will be drawn (modified in-place).
    center : tuple of int
        Coordinates (y, x) for the center of the circle.
    radius : int
        Radius of the circle.

    Returns
    -------
    None

    Raises
    ------
    None

    Examples
    --------
    >>> _draw_circle(mask, (50, 50), 10)
    """
    H, W = mask.shape
    yy, xx = np.ogrid[:H, :W]
    cy, cx = center
    circle = (yy - cy)**2 + (xx - cx)**2 <= radius**2
    mask[circle] = 1


def _draw_rectangle(mask, top_left, size):
    """
    Draws a filled rectangle on the given binary mask.

    Sets the values inside the rectangle defined by the top-left corner and size to 1.

    Parameters
    ----------
    mask : ndarray
        A 2D NumPy array where the rectangle will be drawn (modified in-place).
    top_left : tuple of int
        Coordinates (y, x) for the top-left corner of the rectangle.
    size : tuple of int
        Height and width (h, w) of the rectangle.

    Returns
    -------
    None

    Raises
    ------
    None

    Examples
    --------
    >>> _draw_rectangle(mask, (10, 10), (20, 30))
    """
    H, W = mask.shape
    y0, x0 = top_left
    h, w = size
    y1 = min(H, y0 + h)
    x1 = min(W, x0 + w)
    mask[y0:y1, x0:x1] = 1


def _draw_triangle(mask, vertices):
    """
    Draws a filled triangle on the given binary mask.

    Sets the values inside the triangle defined by the given vertices to 1 using barycentric coordinates.

    Parameters
    ----------
    mask : ndarray
        A 2D NumPy array where the triangle will be drawn (modified in-place).
    vertices : list of tuple of int
        Three vertices (each as a tuple of y, x coordinates) defining the triangle.

    Returns
    -------
    None

    Raises
    ------
    None

    Examples
    --------
    >>> _draw_triangle(mask, [(10, 10), (20, 15), (15, 25)])
    """
    H, W = mask.shape
    yy, xx = np.mgrid[:H, :W]
    v0, v1, v2 = [np.array(v) for v in vertices]
    denom = ((v1[1] - v2[1]) * (v0[0] - v2[0]) + (v2[0] - v1[0]) * (v0[1] - v2[1]))
    a = ((v1[1] - v2[1]) * (yy - v2[0]) + (v2[0] - v1[0]) * (xx - v2[1])) / denom
    b = ((v2[1] - v0[1]) * (yy - v2[0]) + (v0[0] - v2[0]) * (xx - v2[1])) / denom
    c = 1 - a - b
    tri = (a >= 0) & (b >= 0) & (c >= 0)
    mask[tri] = 1


def generate_pattern_stack(v, height, width, n_circles=10, n_triangles=8, n_rects=6, circle_base=0.4, tri_base=0.2, rect_base=0.6, variation=0.05, noise_std=0.05, seed=None):
    """
    Generates a synthetic image stack of geometric patterns with noise.

    Creates a (v, height, width) stack of grayscale images with random circles, triangles, and rectangles
    drawn on a black background. Each shape type has a base intensity with per-instance variation.
    Independent Gaussian noise is added to each layer. Overlapping shapes are combined using maximum intensity.

    Parameters
    ----------
    v : int
        Number of spectral layers to generate.
    height : int
        Height of each image layer.
    width : int
        Width of each image layer.
    n_circles : int, optional
        Number of circles to draw (default is 10).
    n_triangles : int, optional
        Number of triangles to draw (default is 8).
    n_rects : int, optional
        Number of rectangles to draw (default is 6).
    circle_base : float, optional
        Base intensity for circles (default is 0.4).
    tri_base : float, optional
        Base intensity for triangles (default is 0.2).
    rect_base : float, optional
        Base intensity for rectangles (default is 0.6).
    variation : float, optional
        Maximum uniform variation added/subtracted to base intensity (default is 0.05).
    noise_std : float, optional
        Standard deviation of Gaussian noise (default is 0.05).
    seed : int or None, optional
        Seed for reproducibility (default is None).

    Returns
    -------
    ndarray
        A (v, height, width) NumPy array representing the synthetic image stack.

    Raises
    ------
    None

    Examples
    --------
    >>> stack = generate_pattern_stack(5, 64, 64)
    """

    if seed is not None:
        np.random.seed(seed)
    else:
        np.random.seed(42)

    # create shape masks and random intensities
    masks = []
    intensities = []

    def rand_pt(margin=0):
        return (np.random.randint(margin, height - margin),
                np.random.randint(margin, width - margin))

    # circles
    for _ in range(n_circles):
        m = np.zeros((height, width), bool)
        r = np.random.randint(min(height, width) * 5 // 100,
                              min(height, width) * 15 // 100)
        center = rand_pt(margin=r + 1)
        _draw_circle(m, center, r)
        masks.append(m)
        val = np.clip(circle_base + np.random.uniform(-variation, variation), 0, 1)
        intensities.append(val)

    # triangles
    for _ in range(n_triangles):
        m = np.zeros((height, width), bool)
        r = np.random.randint(min(height, width) * 5 // 100,
                              min(height, width) * 15 // 100)
        cy, cx = rand_pt(margin=r + 1)
        v0 = (cy - r, cx)
        v1 = (cy + r // 2, cx - int(r * .866))
        v2 = (cy + r // 2, cx + int(r * .866))
        _draw_triangle(m, [v0, v1, v2])
        masks.append(m)
        val = np.clip(tri_base + np.random.uniform(-variation, variation), 0, 1)
        intensities.append(val)

    # rectangles
    for _ in range(n_rects):
        m = np.zeros((height, width), bool)
        h = np.random.randint(height * 5 // 100, height * 20 // 100)
        w = np.random.randint(width * 5 // 100, width * 20 // 100)
        top_left = rand_pt(margin=max(h, w) + 1)
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
