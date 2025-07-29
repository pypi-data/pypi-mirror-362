"""
plotter.py
==========

.. module:: plotter
:platform: Unix
:synopsis: Interactive plotting module for the hsi-wizard package.

Module Overview
--------------

This module provides an interactive plotting interface to explore and analyze
DataCube objects. Users can visualize spectral image slices, define regions of
interest (ROIs), inspect mean spectral data, normalize spectra, and save or
remove ROI-based plots. Interaction includes keyboard navigation, mouse-based
ROI selection, and GUI controls (buttons and checkboxes).

Usage
-----
Import and call the `plotter` function with a DataCube instance::

from hsi_wizard.plotter import plotter
plotter(my_datacube)

Interactive Controls
--------------------
- **Left/Right arrow keys**: Step through wavelength layers.
- **Mouse click on image**: Select a single-pixel ROI at cursor.
- **Rectangle drag on image**: Define a custom ROI region.
- **Click on spectrum plot**: Jump to closest wavelength layer.
- **Save Plot button**: Save current ROI spectrum and overlay on plot.
- **Remove Plot button**: Remove the last saved ROI and its spectrum.
- **Normalize Y checkbox**: Toggle Y-axis normalization (0–1 range).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons, RectangleSelector
from matplotlib.gridspec import GridSpec
import random

from .._utils.helper import find_nex_smaller_wave, normalize_spec

# State dictionary to manage the global variables locally
state = {
    'layer_id': 0,
    'normalize_flag': False
}

saved_plots = []  # To hold saved plot data (wave, spec, ROI info, color)
saved_lines = []  # To hold the actual line objects for plotting
saved_rois = []  # To hold ROI rectangles for display


def plotter(dc):
    """
    Launch an interactive plotting interface for a DataCube.

    This function creates a Matplotlib window with two panels: an image view of
    a single spectral layer and a spectral plot of a selected ROI. Users can
    navigate layers, draw or click ROIs, and manage saved spectra with GUI controls.

    Parameters
    ----------
    dc : DataCube
        A DataCube object with attributes:
        - `cube`: numpy array of shape (v, y, x) representing spectral data.
        - `wavelengths`: sequence of length `v` with corresponding wavelengths.
        - `notation`: string to annotate wavelength axis labels.

    Returns
    -------
    None
        The function displays an interactive Matplotlib window and does not
        return a value. All interactions modify the displayed figure directly.

    Notes
    -----
    Keyboard and mouse interactions are captured via Matplotlib event handlers.
    ROI mean spectra are recalculated on-the-fly when ROI or normalization
    changes.

    Examples
    --------
    >>> import wizard
    >>> import numpy as np
    >>> dc = wizard.DataCube(np.random.rand(20, 8, 9))
    >>> wizard.plotter(dc)
    """
    state['layer_id'] = 0  # Initialize layer ID

    # Initialize ROI coordinates
    roi_x_start, roi_x_end = 0, dc.cube.shape[2]
    roi_y_start, roi_y_end = 0, dc.cube.shape[1]

    def on_key(event):
        """
        Respond to left/right arrow key presses to change spectral layer.

        Parameters
        ----------
        event : matplotlib.backend_bases.KeyEvent
            The key press event.

        Raises
        ------
        None
        """
        if event.key == 'left':
            # step down, but not below 0
            state['layer_id'] = max(0, state['layer_id'] - 1)
            update_plot()
        elif event.key == 'right':
            # step up, but not beyond last index
            max_idx = dc.cube.shape[0] - 1
            state['layer_id'] = min(max_idx, state['layer_id'] + 1)
            update_plot()

    def update_plot(_=None):
        """
        Refresh the image slice, ROI mean spectrum, and saved plots.

        Parameters
        ----------
        _ : ignored
            Placeholder for event argument when used as callback.

        Notes
        -----
        Updates color limi
        """
        layer_index = state['layer_id']
        layer = dc.cube[layer_index]
        imshow.set_data(layer)
        imshow.set_clim(vmin=layer.min(), vmax=layer.max())
        layer_id = dc.wavelengths[state["layer_id"]]
        notation = dc.notation or ""
        ax[0].set_title(f'Image @{notation}{layer_id}')

        # Update the vertical line to the current wavelength layer
        line.set_xdata([dc.wavelengths[state['layer_id']]])

        # Update ROI mean plot
        update_roi_mean()

        # Update saved plots without re-adding lines
        for i, sp in enumerate(saved_plots):
            saved_spec = sp['spec']
            if state['normalize_flag']:
                saved_spec = normalize_spec(saved_spec)
            saved_lines[i].set_data(sp['wave'], saved_spec)
            saved_lines[i].set_color(sp['color'])  # Use saved color

        fig.canvas.draw_idle()

    def save_plot(_):
        """
        Save current ROI mean spectrum and overlay it with a random color.

        Parameters
        ----------
        _ : ignored
            Placeholder for event argument when used as callback.

        Notes
        -----
        Stores ROI bounds, computed mean spectrum, and a graphic rectangle.
        """
        roi_data = dc.cube[:, roi_y_start:roi_y_end, roi_x_start:roi_x_end]
        mean_spec = np.mean(roi_data, axis=(1, 2))
        if state['normalize_flag']:
            mean_spec = normalize_spec(mean_spec)

        # Generate a random color for this ROI and save it with the plot
        color = (random.random(), random.random(), random.random())  # Random RGB color
        saved_plots.append({
            'wave': dc.wavelengths,
            'spec': mean_spec,
            'roi': (roi_x_start, roi_x_end, roi_y_start, roi_y_end),  # Save ROI coordinates
            'color': color
        })

        # Plot with the specific color for the saved ROI
        saved_line, = ax[1].plot(saved_plots[-1]['wave'], saved_plots[-1]['spec'], color=color, alpha=0.4)
        saved_lines.append(saved_line)

        # Draw the rectangle on the image to represent the ROI and save it
        roi_rect = plt.Rectangle((roi_x_start, roi_y_start), roi_x_end - roi_x_start, roi_y_end - roi_y_start,
                                 linewidth=2, edgecolor=color, facecolor=color, alpha=0.4)
        ax[0].add_patch(roi_rect)
        saved_rois.append(roi_rect)  # Store the rectangle so we can manage it later

        update_plot()

    def remove_last_plot(_):
        """
        Remove the most recently saved ROI spectrum and rectangle.

        Parameters
        ----------
        _ : ignored
            Placeholder for event argument when used as callback.

        Notes
        -----
        Pops entries from saved_plots, saved_lines, and saved_rois.
        """
        if saved_plots:
            saved_plots.pop()
            saved_lines.pop().remove()

            # Remove the corresponding ROI rectangle
            if saved_rois:
                roi_rect = saved_rois.pop()
                roi_rect.remove()

            update_plot()

    def toggle_normalization(_):
        """
        Toggle normalization flag for Y-axis and refresh plots.

        Parameters
        ----------
        _ : ignored
            Placeholder for event argument when used as callback.
        """
        state['normalize_flag'] = not state['normalize_flag']
        update_plot()

    def update_roi_mean():
        """
        Recompute and update the mean spectrum for the current ROI.

        Notes
        -----
        Adjusts Y-limits based on normalization state.
        """
        roi_data = dc.cube[:, roi_y_start:roi_y_end, roi_x_start:roi_x_end]
        mean_spec = np.mean(roi_data, axis=(1, 2))
        if state['normalize_flag']:
            mean_spec = normalize_spec(mean_spec)

        # Define range padding
        r = (mean_spec.max() - mean_spec.min()) * 0.1
        ax[1].set_ylim(0 if state['normalize_flag'] else mean_spec.min() - r,
                       1 if state['normalize_flag'] else mean_spec.max() + r)
        roi_line.set_data(dc.wavelengths, mean_spec)

    def on_roi_change(eclick, erelease):
        """
        Update ROI bounds from rectangle selection events.

        Parameters
        ----------
        eclick : matplotlib.backend_bases.MouseEvent
            Mouse press event.
        erelease : matplotlib.backend_bases.MouseEvent
            Mouse release event.
        """
        nonlocal roi_x_start, roi_x_end, roi_y_start, roi_y_end

        roi_x_start, roi_y_start = int(eclick.xdata), int(eclick.ydata)
        roi_x_end, roi_y_end = int(erelease.xdata), int(erelease.ydata)

        if roi_x_start - roi_x_end == 0:
            roi_x_end += 1
        if roi_y_start - roi_y_end == 0:
            roi_y_end += 1

        update_plot()

    def onclick_select(event):
        """
        Handle clicks to select single-pixel ROI or jump wavelength layer.

        Parameters
        ----------
        event : matplotlib.backend_bases.MouseEvent
            Mouse click event.

        Raises
        ------
        IndexError
            If no smaller wavelength is found for clicked X coordinate.
        """
        nonlocal roi_x_start, roi_x_end, roi_y_start, roi_y_end
        if event.inaxes == ax[0]:
            roi_x, roi_y = int(event.xdata), int(event.ydata)
            roi_x_start, roi_x_end = roi_x, roi_x + 1
            roi_y_start, roi_y_end = roi_y, roi_y + 1
            update_plot()
        elif event.inaxes == ax[1]:
            try:
                state['layer_id'] = np.where(dc.wavelengths == find_nex_smaller_wave(dc.wavelengths, int(event.xdata), 10))[0][0]
            except IndexError:
                return
            update_plot()

    # Create main figure and layout with GridSpec
    fig = plt.figure(figsize=(14, 8))
    gs = GridSpec(2, 2, width_ratios=[4, 4], height_ratios=[4, 1])

    # Main plotting area (image and spectrum)
    ax_image = fig.add_subplot(gs[0, 0])
    ax_spectrum = fig.add_subplot(gs[0, 1])
    ax_spectrum.set_title('Spectrum')
    ax = [ax_image, ax_spectrum]

    # Control panel for buttons and checkbox
    ax_control = fig.add_subplot(gs[1, :])
    ax_control.axis("off")

    # Set up the initial plots
    layer = dc.cube[0]
    imshow = ax[0].imshow(layer)
    spec = dc.cube[:, 0, 0]
    line = ax[1].axvline(x=state['layer_id'], color='lightgrey', linestyle='dashed')

    # ROI mean line
    roi_line, = ax[1].plot(dc.wavelengths, spec, label="ROI Mean", color='red')
    ax[1].set_xlabel(f'{dc.notation}')
    ax[1].set_ylabel('Counts')
    ax[1].set_xlim(dc.wavelengths.min(), dc.wavelengths.max())

    # Buttons and checkbox in the control panel, centered horizontally
    button_w = 0.15
    button_h = 0.075
    gap = 0.05

    # total width of 3 buttons + 2 gaps
    total_w = 3 * button_w + 2 * gap
    start_x = (1.0 - total_w) / 2.0

    ax_save = fig.add_axes([start_x, 0.1, button_w, button_h])
    btn_save = Button(ax_save, 'Save Plot')
    btn_save.on_clicked(save_plot)

    ax_remove = fig.add_axes([start_x + (button_w + gap), 0.1, button_w, button_h])
    btn_remove = Button(ax_remove, 'Remove Plot')
    btn_remove.on_clicked(remove_last_plot)

    ax_checkbox = fig.add_axes([start_x + 2 * (button_w + gap), 0.1, button_w, button_h])
    check = CheckButtons(ax_checkbox, ['Normalize Y (0-1)'], [False])
    check.on_clicked(toggle_normalization)

    # ROI selection
    _ = RectangleSelector(ax[0], on_roi_change, useblit=True, button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    fig.canvas.mpl_connect("button_press_event", onclick_select)
    
    fig.canvas.mpl_connect("key_press_event", on_key)

    update_plot()

    fig.subplots_adjust(
        left=0.05, right=0.95,
        top=0.95, bottom=0.05,
        wspace=0.3, hspace=0.3
    )
    plt.show()
