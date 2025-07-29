from wizard import DataCube
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


def plot_datacube_faces(datacube: DataCube, wl_indices: tuple = None, x_indices: tuple = None, y_indices: tuple = None, vmin: float = None, vmax: float = None, cmap: str = 'cool'):
    """
    Plot all six faces of a DataCube as colored surfaces.

    This function renders the six boundary faces of the 3D data cube:
      - Two XY planes at the minimum and maximum wavelengths.
      - Two XW planes at the minimum and maximum Y indices.
      - Two YW planes at the minimum and maximum X indices.

    Parameters
    ----------
    datacube : DataCube
        A `wizard.DataCube` with `cube` (numpy.ndarray of shape (v, x, y))
        and `wavelengths` (sequence of length v).
    wl_indices : tuple of int, optional
        (min_wl_idx, max_wl_idx) for the bottom and top XY faces.
        Defaults to (0, v-1).
    x_indices : tuple of int, optional
        (min_x_idx, max_x_idx) for the left and right YW faces.
        Defaults to (0, x_dim-1).
    y_indices : tuple of int, optional
        (min_y_idx, max_y_idx) for the front and back XW faces.
        Defaults to (0, y_dim-1).
    vmin : float, optional
        Minimum intensity for colormap. Defaults to global minimum.
    vmax : float, optional
        Maximum intensity for colormap. Defaults to global maximum.
    cmap : str or Colormap, optional
        Matplotlib colormap name or instance. Default is 'viridis'.

    Returns
    -------
    None
        Displays a 3D plot of the six faces of the DataCube.
    """
    # Validate inputs
    if not hasattr(datacube, 'cube') or not hasattr(datacube, 'wavelengths'):
        raise TypeError("datacube must have 'cube' and 'wavelengths' attributes")
    cube = np.asarray(datacube.cube)
    wl = np.asarray(datacube.wavelengths)
    if cube.ndim != 3 or cube.shape[0] != wl.shape[0]:
        raise ValueError("cube must be shape (v, x, y) and len(wavelengths) == v")

    v, x_dim, y_dim = cube.shape
    # Default index tuples
    min_wl, max_wl = (0, v - 1) if wl_indices is None else wl_indices
    min_x, max_x = (0, x_dim - 1) if x_indices is None else x_indices
    min_y, max_y = (0, y_dim - 1) if y_indices is None else y_indices

    # Check validity
    for name, idx, limit in (('min_wl', min_wl, v), ('max_wl', max_wl, v),
                             ('min_x', min_x, x_dim), ('max_x', max_x, x_dim),
                             ('min_y', min_y, y_dim), ('max_y', max_y, y_dim)):
        if not (0 <= idx < limit):
            raise ValueError(f"{name}={idx} out of range [0, {limit})")

    # Colormap normalization
    if vmin is None:
        vmin = float(cube.min())
    if vmax is None:
        vmax = float(cube.max())
    norm = Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.get_cmap(cmap)

    # Prepare coordinate vectors
    x = np.arange(x_dim)
    y = np.arange(y_dim)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 1 & 2: XY faces at min_wl and max_wl
    for wl_idx in (min_wl, max_wl):
        X_xy, Y_xy = np.meshgrid(x, y, indexing='ij')
        Z_xy = np.full_like(X_xy, wl[wl_idx], dtype=float)
        C_xy = cube[wl_idx, :, :]
        ax.plot_surface(
            X_xy, Y_xy, Z_xy,
            facecolors=cmap(norm(C_xy)),
            rstride=1, cstride=1, shade=False
        )

    # 3 & 4: XW faces at min_y and max_y
    for y_idx in (min_y, max_y):
        W_xw, X_xw = np.meshgrid(wl, x, indexing='ij')
        Y_xw = np.full_like(W_xw, y_idx, dtype=float)
        C_xw = cube[:, :, y_idx]
        ax.plot_surface(
            X_xw, Y_xw, W_xw,
            facecolors=cmap(norm(C_xw)),
            rstride=1, cstride=1, shade=False
        )

    # 5 & 6: YW faces at min_x and max_x
    for x_idx in (min_x, max_x):
        W_yw, Y_yw = np.meshgrid(wl, y, indexing='ij')
        X_yw = np.full_like(W_yw, x_idx, dtype=float)
        C_yw = cube[:, x_idx, :]
        ax.plot_surface(
            X_yw, Y_yw, W_yw,
            facecolors=cmap(norm(C_yw)),
            rstride=1, cstride=1, shade=False
        )

    # Labels and colorbar
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Wavelength')
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, label='Intensity')

    plt.tight_layout()
    plt.show()
