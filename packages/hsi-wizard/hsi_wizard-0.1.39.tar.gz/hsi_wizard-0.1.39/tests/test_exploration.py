import numpy as np
import matplotlib
import pytest
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import wizard
from wizard import plotter
from wizard._exploration import plotter
from wizard import plot_datacube_faces
from wizard import DataCube

matplotlib.use("Agg")


def create_test_cube(shape=(3, 4, 4)):
    cube = np.random.rand(*shape)  # Generate a random cube
    return DataCube(cube=cube, wavelengths=np.arange(shape[0]))


def setup_plot(dc):
    # reset global state and any saved lists
    plotter.state['layer_id'] = 0
    plotter.state['normalize_flag'] = False
    plotter.saved_plots.clear()
    plotter.saved_lines.clear()
    plotter.saved_rois.clear()

    # launch headless plotter
    wizard.plotter(dc)
    return plt.gcf()


def get_key_callbacks(fig):
    """
    Return only the user-registered on_key callbacks.
    """
    refs = fig.canvas.callbacks.callbacks.get('key_press_event', {}).values()
    cbs = []
    for ref in refs:
        func = ref()
        if func and func.__name__ == 'on_key':
            cbs.append(func)
    if not cbs:
        raise RuntimeError("on_key callback not found")
    return cbs


def get_button_press_callbacks(fig):
    refs = fig.canvas.callbacks.callbacks.get('button_press_event', {}).values()
    cbs = []
    for ref in refs:
        func = ref()
        if func is not None:
            cbs.append(func)
    return cbs


def get_onclick_select_callback(fig):
    for cb in get_button_press_callbacks(fig):
        if cb.__name__ == 'onclick_select':
            return cb
    raise RuntimeError("onclick_select callback not found")


class TestPlotterExtra:

    def test_on_key_navigation_bounds(self):
        dc = create_test_cube((3, 2, 2))
        fig = setup_plot(dc)
        key_cbs = get_key_callbacks(fig)

        # initial state
        assert plotter.state['layer_id'] == 0

        # press right twice: should move to last index
        evt = type("E", (), {"key": "right"})
        for _ in range(2):
            for cb in key_cbs:
                cb(evt)
        assert plotter.state['layer_id'] == 2

        # pressing right again stays at upper bound
        for cb in key_cbs:
            cb(evt)
        assert plotter.state['layer_id'] == 2

        # press left thrice: should move back to 0
        evt.key = "left"
        for _ in range(3):
            for cb in key_cbs:
                cb(evt)
        assert plotter.state['layer_id'] == 0

    def test_update_plot_title_and_vertical_line(self):
        cube = np.random.rand(4, 2, 2)
        dc = DataCube(cube=cube, wavelengths=np.array([5, 15, 25, 35]), notation="nm")
        fig = setup_plot(dc)

        # verify initial title and vline
        assert fig.axes[0].get_title() == 'Image @nm5'

        # simulate right arrow press
        key_cbs = get_key_callbacks(fig)
        evt = type("E", (), {"key": "right"})
        for cb in key_cbs:
            cb(evt)

        assert fig.axes[0].get_title() == 'Image @nm15'
        vline = fig.axes[1].lines[0]
        assert np.allclose(vline.get_xdata(), [15])

    def test_roi_mean_normalization(self):
        arr = np.arange(4).reshape(4, 1, 1) * np.ones((4, 1, 4))
        dc = DataCube(cube=arr, wavelengths=np.array([10, 20, 30, 40]))
        fig = setup_plot(dc)

        # enable normalization and update
        plotter.state['normalize_flag'] = True
        key_cbs = get_key_callbacks(fig)
        evt = type("E", (), {"key": "left"})
        for cb in key_cbs:
            cb(evt)

        roi_line = fig.axes[1].lines[1]
        ydata = roi_line.get_ydata()

        spec = arr.mean(axis=(1, 2))
        expected = (spec - spec.min()) / (spec.max() - spec.min())
        np.testing.assert_allclose(ydata, expected)

    def test_onclick_select_spectrum(self):
        dc = create_test_cube((3, 1, 1))
        dc.wavelengths = np.array([100, 200, 300])
        fig = setup_plot(dc)

        assert plotter.state['layer_id'] == 0
        onclk = get_onclick_select_callback(fig)

        evt = type("E", (), {"inaxes": fig.axes[1], "xdata": 250.0})
        onclk(evt)
        assert plotter.state['layer_id'] == 0

        prev = plotter.state['layer_id']
        evt.xdata = 1000.0
        onclk(evt)
        assert plotter.state['layer_id'] == prev

    def test_onclick_select_image_updates_roi_mean(self):
        arr = np.arange(2*3*4).reshape(2, 3, 4)
        dc = DataCube(cube=arr, wavelengths=np.array([1, 2]))
        fig = setup_plot(dc)

        onclk = get_onclick_select_callback(fig)
        evt = type("E", (), {"inaxes": fig.axes[0], "xdata": 2.4, "ydata": 1.6})
        onclk(evt)

        roi_line = fig.axes[1].lines[1]
        ydata = roi_line.get_ydata()

        expected = arr[:, 1, 2]
        np.testing.assert_allclose(ydata, expected)


class TestSurcefacePlot:

    def test_surface_function_runs(self):
        dc = wizard.DataCube(cube=np.random.rand(20, 8, 9))
        wizard.plot_surface(dc)

    def test_dc_cut_by_value(self):
        # Create a random DataCube
        dc = wizard.DataCube(cube=np.random.rand(20, 8, 9))

        # Extract a random slice
        z = dc.cube[5, :, :]
        val = 0.5  # Example cut value

        # Apply function
        modified_z = wizard._exploration.surface.dc_cut_by_value(z, val, type="")

        # Check modifications
        assert modified_z.shape == z.shape, "Shape should remain unchanged"
        assert np.all(modified_z[modified_z <= val] == modified_z.min()), "Values below threshold should be set to min"

    def test_get_z_surface(self):
        # Create a random DataCube
        dc = wizard.DataCube(cube=np.random.rand(20, 8, 9))

        # Select a slice index
        v = 5

        # Compute surface
        z_surface = wizard._exploration.surface.get_z_surface(dc.cube, v)

        # Check shape
        assert z_surface.shape == (dc.shape[1], dc.shape[2]), "Surface shape mismatch"

    def test_plot_surface(self):
        # Create a random DataCube
        dc = wizard.DataCube(cube=np.random.rand(20, 8, 9))

        # Run plot function (not testing output, only checking for errors)
        try:
            wizard._exploration.surface.plot_surface(dc, index=0)
        except Exception as e:
            pytest.fail(f"plot_surface raised an exception: {e}")


class TestPlotDatacubeFaces:
    def setup_method(self):
        # prevent the GUI window from blocking tests
        plt.show = lambda *args, **kwargs: None
        plt.close('all')

    def teardown_method(self):
        # restore and close all figures
        plt.close('all')

    def test_missing_attributes_raises_type_error(self):
        class Dummy: pass
        dummy = Dummy()
        with pytest.raises(TypeError) as exc:
            plot_datacube_faces(dummy)
        assert "datacube must have 'cube' and 'wavelengths'" in str(exc.value)

    def test_shape_mismatch_raises_value_error(self):
        # wavelengths length != cube.shape[0]
        bad = DataCube(cube=np.zeros((4, 2, 2)), wavelengths=np.arange(3))
        with pytest.raises(ValueError) as exc:
            plot_datacube_faces(bad)
        assert "cube must be shape (v, x, y) and len(wavelengths) == v" in str(exc.value)

    @pytest.mark.parametrize("idxs, name", [
        ({"wl_indices": (-1, 2)}, "min_wl"),
        ({"wl_indices": (0, 5)}, "max_wl"),
        ({"x_indices": (0, 4)}, "max_x"),
        ({"y_indices": (3, -1)}, "min_y"),
    ])
    def test_index_out_of_range_raises_value_error(self, idxs, name):
        dc = create_test_cube((3, 3, 3))
        with pytest.raises(ValueError) as exc:
            plot_datacube_faces(dc, **idxs)
        assert f"{name}=" in str(exc.value)

    def test_default_plot_draws_six_faces(self):
        dc = create_test_cube((2, 3, 4))
        # call with defaults
        plot_datacube_faces(dc)
        fig = plt.gcf()
        # The 3d Axes is the first axes
        ax = fig.axes[0]
        # Each plot_surface adds one Poly3DCollection => 6 faces
        n_surfaces = sum(1 for col in ax.collections
                         if isinstance(col, mplot3d.art3d.Poly3DCollection))
        assert n_surfaces == 6

    def test_custom_indices_and_vmin_vmax_and_cmap(self):
        shape = (5, 4, 3)
        dc = create_test_cube(shape)
        # choose non-default slices
        wl_indices = (1, 3)
        x_indices = (2, 2)
        y_indices = (0, 1)
        vmin, vmax = 0.2, 0.8
        cmap = 'plasma'
        plot_datacube_faces(dc,
                            wl_indices=wl_indices,
                            x_indices=x_indices,
                            y_indices=y_indices,
                            vmin=vmin,
                            vmax=vmax,
                            cmap=cmap)
        fig = plt.gcf()
        ax = fig.axes[0]
        # verify surfaces count
        n_surfaces = sum(1 for col in ax.collections
                         if isinstance(col, mplot3d.art3d.Poly3DCollection))
        assert n_surfaces == 6

        # verify colormap instance
        # grab one surface facecolors to check colormap mapping
        sample = ax.collections[0].get_facecolors()
        # there should be RGBA values in [0,1]
        assert np.all((sample >= 0) & (sample <= 1))

