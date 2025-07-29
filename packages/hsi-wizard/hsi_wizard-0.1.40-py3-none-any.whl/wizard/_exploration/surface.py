"""
surface.py
==========

.. module:: surface
:platform: Unix
:synopsis: Surface plotting and manipulation module for the hsi-wizard package.

Module Overview
--------------

This module provides functionalities for manipulating and visualizing data cubes.
It includes utilities for slicing, cutting, and plotting 3D surfaces interactively
using sliders.

"""

from wizard import DataCube
import numpy as np
import copy
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider


def dc_cut_by_value(z: np.array, val: int, type: str) -> np.array:
    """
    Threshold a 2D data slice by a normalized cut-off value.

    This function normalizes the input array to its maximum value, applies a threshold
    such that all values less than or equal to the cut-off are replaced with the array's minimum,
    and preserves values above the threshold. Use this to mask out low-intensity regions
    in a hyperspectral data slice.

    Parameters
    ----------
    z : np.ndarray
        2D array (spatial slice) extracted from a DataCube (shape: (x, y)).
    val : float
        Normalized threshold between 0.0 and 1.0. Values less than or equal to this threshold
        are set to the minimum value of the normalized slice.
    type : str, optional
        Label for the type of cut applied; currently unused but reserved for future modes.

    Returns
    -------
    np.ndarray
        A copy of the input array after normalization and threshold cut.


    Notes
    -----
    - The input array is deeply copied to avoid modifying original data.
    - Thresholding is performed after normalizing by the array's maximum.

    Examples
    --------
    >>> slice2D = np.array([[0, 5], [10, 15]])
    >>> dc_cut_by_value(slice2D, 0.5)
    array([[0. , 0. ], [0.66666667, 1. ]])
    """
    new_z = copy.deepcopy(z)
    new_z /= new_z.max()
    new_z[new_z <= val] = new_z.min()
    return new_z


def get_z_surface(cube: np.array, v: int) -> np.array:
    """
    Extract the positive-valued surface from a spectral slice of a data cube.

    This function selects the v-th spectral band from a 3D hyperspectral cube,
    masks out non-positive values, and constructs a 2D surface array for plotting.
    Use this to visualize spatial distribution at a given wavelength index.

    Parameters
    ----------
    cube : np.ndarray
        3D data cube with shape (v, x, y), where v is the number of spectral bands.
    v : int
        Index of the spectral band to extract (0 <= v < cube.shape[0]).

    Returns
    -------
    np.ndarray
        2D array (shape: (x, y)) containing only the positive values from the slice;
        non-positive entries are left at zero.


    Examples
    --------
    >>> cube = np.zeros((3, 2, 2))
    >>> cube[1] = [[1, -1], [0, 2]]
    >>> get_z_surface(cube, 1)
    array([[1., 0.], [0., 2.]])
    """
    z = np.zeros((cube.shape[1], cube.shape[2]))
    slice_v = cube[v, :, :]
    mask = slice_v > 0
    z[mask] = slice_v[mask]
    return z


def plot_surface(dc: DataCube, index: int = 0):
    """
    Create an interactive 3D surface plot from a DataCube slice.

    This function visualizes a DataCube by plotting a 3D surface of a selected spectral band.
    Users can manipulate two sliders: one to change the wavelength index (spectral band) and
    another to adjust the normalized cut-off threshold, updating the plot in real time.

    Parameters
    ----------
    dc : DataCube
        DataCube instance
    index : int, optional
        Initial spectral index to display (default is 0).

    Returns
    -------
    None

    Notes
    -----
    - The wavelength slider is labeled with actual wavelength values at evenly
    spaced ticks.
    - The cut-off slider normalizes data slices between 0 and 1 before thresholding.
    - Use the sliders to explore spectral variation and mask out low-intensity regions.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.DataCube(np.random.rand(10, 100, 100), wavelengths=list(np.linspace(400, 700, 10)))
    >>> wizard.plot_surface(dc, index=5)
    """
    def update(val):
        idx = int(slider.val)  # Ensure integer values
        cut_val = slider_cut.val  # Get cut value

        ax.clear()
        z = get_z_surface(dc, idx)

        # Apply the cut before getting the surface data
        z = dc_cut_by_value(z, cut_val, type="")

        x, y = np.meshgrid(range(dc.shape[1]), range(dc.shape[2]))
        ax.plot_surface(x, y, z.T, cmap=cm.coolwarm)
        ax.set_title(f'{dc.name if dc.name else ""} @{dc.wavelengths[idx]:.2f} {dc.notation if dc.notation else ""}')
        ax.set(xlabel='x', ylabel='y', zlabel='counts')
        fig.canvas.draw_idle()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Wavelength slider
    slider_ax = fig.add_axes([0.2, 0.02, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    tick_positions = np.linspace(0, len(dc.wavelengths) - 1, min(5, len(dc.wavelengths))).astype(int)
    slider = Slider(slider_ax, 'Wavelength', 0, dc.shape[0] - 1, valinit=index, valstep=1)
    slider.ax.set_xticks(tick_positions)
    slider.ax.set_xticklabels([f'{dc.wavelengths[i]:.2f}' for i in tick_positions])
    slider.on_changed(update)

    # Cut value slider
    slider_cut_ax = fig.add_axes([0.2, 0.06, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    slider_cut = Slider(slider_cut_ax, 'Cut Value', 0, 1, valinit=0, valstep=0.01)  # Cut value from 0 to 1
    slider_cut.on_changed(update)

    update(index)  # Initial plot
    plt.show()
