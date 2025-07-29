"""
_core/datacube_ops.py

.. module:: datacube_ops
   :platform: Unix
   :synopsis: DataCube Operations.

## Module Overview
This module contains operation function for processing datacubes.

## Functions
.. autofunction:: remove_spikes
.. autofunction:: resize
"""
import os
import cv2
import copy
import rembg
import random
import numpy as np
from PIL import Image
from joblib import Parallel, delayed
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter, uniform_filter
from skimage.transform import warp


from . import DataCube 
from .._processing.spectral import calculate_modified_z_score, spec_baseline_als
from .._utils.helper import _process_slice, feature_registration, RegistrationError, auto_canny, decompose_homography, normalize_polarity


def remove_spikes(dc: DataCube, threshold: int = 6500, window: int = 5) -> DataCube:
    """
    Remove cosmic spikes from each pixel's spectral data.

    This function computes the modified z-score for each pixel's spectral vector,
    identifies spikes where the score exceeds the threshold, and replaces spike
    values with the local mean within a sliding window along the spectrum.

    Parameters
    ----------
    dc : DataCube
        The input DataCube with shape (v, x, y), where v is the number of spectral bands.
    threshold : int, optional
        Threshold for spike detection via modified z-score, defaults to 6500.
    window : int, optional
        Window size (in spectral channels) for mean replacement of spikes, defaults to 5.

    Returns
    -------
    DataCube
        A new DataCube instance with spikes removed per-pixel.

    Raises
    ------
    ValueError
        If `window` is not in the range [1, number of spectral bands].

    Notes
    -----
    - The original DataCube is not modified in place; es wird eine Kopie zurückgegeben.
    - Die Modifizierte z-Score-Berechnung erwartet Input mit Form (n_samples, n_features).
    - Parallelisierung beschleunigt die Einzelpixel-Bearbeitung.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read("example.fsm")
    >>> dc.remove_spikes(threshold=6500, window=5)
    """
    v, x, y = dc.cube.shape
    if not (1 <= window <= v):
        raise ValueError(f"window must be between 1 and {v}, got {window}")

    # reshape to (n_pixels, v)
    n_pixels = x * y
    flat_cube = dc.cube.reshape(v, n_pixels).T  # shape: (n_pixels, v)

    # Berechne pro-pixel modifizierten z-score
    z_scores = calculate_modified_z_score(flat_cube)  # (n_pixels, v)
    spikes = np.abs(z_scores) > threshold
    flat_out = flat_cube.copy()

    # Parallel auf jedes Pixel anwenden
    results = Parallel(n_jobs=-1)(
        delayed(_process_slice)(flat_out, spikes, idx, window)
        for idx in range(n_pixels)
    )
    for idx, spec in results:
        flat_out[idx] = spec

    # zurück in (v, x, y) formen
    clean_cube = flat_out.T.reshape(v, x, y)

    # Kopie des DataCube mit dem bereinigten Cube

    dc.set_cube(clean_cube)
    return dc


def remove_background(dc: DataCube, threshold: int = 50, style: str = 'dark') -> DataCube:
    """
    Remove background from images in a DataCube.

    Uses an external algorithm (rembg). The first image in the DataCube
    is processed to generate a mask, which is then applied to all images
    to remove the background.

    Parameters
    ----------
    dc : DataCube
        DataCube containing the image stack.
    threshold : int, optional
        Threshold value to define the background from the alpha mask,
        defaults to 50. Pixels with alpha < threshold are considered background.
    style : str, optional
        Style of background removal, 'dark' or 'bright', defaults to 'dark'.
        If 'dark', background pixels are set to 0.
        If 'bright', background pixels are set to the max value of the cube.y

    Returns
    -------
    DataCube
        DataCube with the background removed.

    Raises
    ------
    ValueError
        If style is not 'dark' or 'bright'.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read("example.fsm")
    >>> dc.remove_background(threshold=50, style='bright') # or style 'dark'
    """
    img = dc.cube[0]
    img = ((img - img.min()) / (img.max() - img.min()) * 255).astype('uint8')
    img = Image.fromarray(img)
    img_removed_bg = rembg.remove(img)
    mask = np.array(img_removed_bg.getchannel('A'))

    cube = dc.cube.copy()
    if style == 'dark':
        cube[:, mask < threshold] = 0
    elif style == 'bright':
        cube[:, mask < threshold] = dc.cube.max()
    else:
        raise ValueError("Type must be 'dark' or 'bright'")
    dc.set_cube(cube)
    return dc


def resize(dc: DataCube, x_new: int, y_new: int, interpolation: str = 'linear') -> None:
    """
    Resize the DataCube to new x and y dimensions.
    dc.shape is v,x,y

    Resizes each 2D slice (x, y) of the DataCube using the specified
    interpolation method.

    Interpolation methods:
        * ``linear``: Bilinear interpolation (ideal for enlarging).
        * ``nearest``: Nearest neighbor interpolation (fast but blocky).
        * ``area``: Pixel area interpolation (ideal for downscaling).
        * ``cubic``: Bicubic interpolation (high quality, slower).
        * ``lanczos``: Lanczos interpolation (highest quality, slowest).

    Parameters
    ----------
    dc : DataCube
        The DataCube instance to be resized.
    x_new : int
        The new width (x-dimension).
    y_new : int
        The new height (y-dimension).
    interpolation : str, optional
        Interpolation method, defaults to 'linear'.
        Options: 'linear', 'nearest', 'area', 'cubic', 'lanczos'.

    Returns
    -------
    None
        The DataCube is modified in-place.

    Raises
    ------
    ValueError
        If the interpolation method is not recognized.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read("example.fsm")
    >>> dc.resize(x_new=500, y_new=500)
    """
    mode = None
    shape = dc.cube.shape
    if shape[1] > x_new:
        print('\033[93mx_new is smaller than the existing cube, you will lose information\033[0m')
    if shape[2] > y_new:
        print('\033[93my_new is smaller than the existing cube, you will lose information\033[0m')

    if interpolation == 'linear':
        mode = cv2.INTER_LINEAR
    elif interpolation == 'nearest':
        mode = cv2.INTER_NEAREST
    elif interpolation == 'area':
        mode = cv2.INTER_AREA
    elif interpolation == 'cubic':
        mode = cv2.INTER_CUBIC
    elif interpolation == 'lanczos':
        mode = cv2.INTER_LANCZOS4
    else:
        raise ValueError(f'Interpolation method `{interpolation}` not recognized.')

    _cube = np.empty(shape=(shape[0], x_new, y_new))
    for idx, layer in enumerate(dc.cube):
        _cube[idx] = cv2.resize(layer, (y_new, x_new), interpolation=mode)
    dc.cube = _cube
    dc._set_cube_shape()


def baseline_als(dc: DataCube, lam: float = 1000000, p: float = 0.01, niter: int = 10) -> DataCube:
    """
    Apply Adaptive Smoothness (ALS) baseline correction.

    Iterates through each pixel (spectrum) in the DataCube and subtracts
    the baseline calculated by the `spec_baseline_als` function.

    Parameters
    ----------
    dc : DataCube
        The input DataCube.
    lam : float, optional
        The smoothness parameter for ALS, defaults to 1000000.
        Larger lambda makes the baseline smoother.
    p : float, optional
        The asymmetry parameter for ALS, defaults to 0.01.
        Value between 0 and 1. Controls how much the baseline is pushed
        towards the data (0 for minimal, 1 for maximal).
    niter : int, optional
        The number of iterations for the ALS algorithm, defaults to 10.

    Returns
    -------
    DataCube
        The DataCube with baseline correction applied.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read("example.fsm")
    >>> dc.baseline_als(lam=1e6, p=.001, niter=10)
    """
    for x in range(dc.shape[1]):
        for y in range(dc.shape[2]):
            dc.cube[:, x, y] -= spec_baseline_als(
                spectrum=dc.cube[:, x, y],
                lam=lam,
                p=p,
                niter=niter
            )
    return dc


def merge_cubes(dc1: DataCube, dc2: DataCube, register: bool = False) -> DataCube:
    """
    Merge two DataCubes into a single DataCube, with optional registration.

    If both datacubes are already registered and the `register` flag is True,
    the function will sample up to 10 random spectral layers from dc2, attempt to
    register each to the first layer of dc1, choose the transform with the lowest
    mean-squared-error alignment, then apply that best transform to all layers of dc2
    before merging.

    Parameters
    ----------
    dc1 : DataCube
        The first DataCube (used as reference).
    dc2 : DataCube
        The second DataCube to be merged into the first.
    register : bool, optional
        If True (default), registration will be attempted if both cubes are marked as registered.

    Returns
    -------
    DataCube
        A new DataCube containing merged spatial and spectral data.

    Raises
    ------
    NotImplementedError
        If the cubes have mismatched spatial dimensions and cannot be merged,
        or if wavelengths overlap without being purely indices.

    Examples
    --------
    >>> import wizard
    >>> dc_a = wizard.read('example.fsm')
    >>> dc_b = wizard.read('another_file.csv')
    >>> dc_a.merge_cubes(dc_b)
    """
    c1 = dc1.cube
    c2 = dc2.cube
    wave1 = dc1.wavelengths
    wave2 = dc2.wavelengths

    # Optional registration step with sampling
    if register and getattr(dc1, 'registered', False) and getattr(dc2, 'registered', False):
        print("Both datacubes registered. Sampling layers for alignment...")
        ref_img = c1[0]
        num_layers = c2.shape[0]
        sample_indices = random.sample(range(num_layers), min(10, num_layers))

        best_score = np.inf
        best_transform = None
        # Try to register sampled layers and pick best
        for idx in sample_indices:
            try:
                aligned_slice, transform = feature_registration(ref_img, c2[idx])
                # Compute alignment quality (mean squared error)
                mse = np.mean((ref_img - aligned_slice)**2)
                if mse < best_score:
                    best_score = mse
                    best_transform = transform
            except RegistrationError as e:
                print(f"Registration of sampled layer {idx} failed: {e}")

        if best_transform is not None:
            # Apply best transform to all layers of dc2
            for i in range(num_layers):
                try:
                    c2[i] = warp(c2[i], inverse_map=best_transform.inverse, preserve_range=True)
                except Exception as e:
                    print(f"Failed to apply best transform to layer {i}: {e}")
        else:
            print("No successful sampled registration. Skipping registration.")

    # Spatial size check
    if c1.shape[1:] == c2.shape[1:]:
        c3 = np.concatenate([c1, c2], axis=0)
    else:
        raise NotImplementedError(
            'Sorry - this function can only merge cubes with the same spatial dimensions.'
        )

    # Handle wavelength merge
    if set(wave1) & set(wave2):
        # If wavelengths are index-based, just concatenate indices
        if set(wave1) <= set(range(c1.shape[0])) and set(wave2) <= set(range(c2.shape[0])):
            wave3 = list(range(c1.shape[0] + c2.shape[0]))
        else:
            raise NotImplementedError(
                'Sorry - your wavelengths overlap and are not purely index-based.'
            )
    else:
        wave3 = np.concatenate((wave1, wave2))

    # Create new merged DataCube (modify dc1 in-place)
    dc1.set_cube(c3)
    dc1.set_wavelengths(wave3)

    return dc1


def inverse(dc: DataCube) -> DataCube:
    """
    Invert the DataCube values.

    This operation is useful for converting between transmission and
    reflectance data, or similar inversions. The formula applied is:
    `tmp = cube * -1`
    `tmp += -tmp.min()`
    The data type of the cube is preserved if it's 'uint16' or 'uint8'
    after temporary conversion to 'float16' for calculation.

    Parameters
    ----------
    dc : DataCube
        The DataCube to invert.

    Returns
    -------
    DataCube
        The DataCube with inverted values.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read('example.fsm')
    >>> dc.inverse()
    """
    dtype = dc.cube.dtype
    if dtype == np.uint16 or dtype == np.uint8:  # Use np types for comparison
        cube = dc.cube.astype(np.float32)
    else:
        cube = dc.cube.copy()

    tmp = cube
    tmp *= -1
    tmp += -tmp.min()

    dc.set_cube(tmp.astype(dtype))
    return dc


def register_layers_simple(dc: DataCube, max_features: int = 5000, match_percent: float = 0.1) -> DataCube:
    """
    Align images within a DataCube using simple feature-based registration.

    Each layer in the DataCube is aligned to the first layer (index 0)
    using ORB feature detection and homography estimation via `_feature_registration`.

    Parameters
    ----------
    dc : DataCube
        The DataCube whose layers are to be registered.
    max_features : int, optional
        Maximum number of keypoint regions to detect, defaults to 5000.
    match_percent : float, optional
        Percentage of keypoint matches to consider for homography,
        defaults to 0.1 (10%).

    Returns
    -------
    DataCube
        The DataCube with layers registered.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read('example.fsm')
    >>> dc.register_layers_simple()
    """
    o_img = dc.cube[0, :, :]
    for i in range(dc.cube.shape[0]):
        if i > 0:
            a_img = copy.deepcopy(dc.cube[i, :, :])
            try:
                _, h = feature_registration(
                    o_img=o_img, a_img=a_img,
                    max_features=max_features, match_percent=match_percent
                )
                height, width = o_img.shape
                aligned_img = cv2.warpPerspective(a_img, h, (width, height))
                dc.cube[i, :, :] = aligned_img
            except RegistrationError as e:
                print(f"Warning: Could not register layer {i} in simple registration: {e}")
                pass
    dc.registered = True
    return dc


def remove_vignetting_poly(dc: DataCube, axis: int = 1, slice_params: dict = None) -> DataCube:
    """
    Remove vignetting using polynomial fitting along a specified axis.

    Calculates the mean along the specified axis (1 for rows, 2 for columns)
    for each spectral layer, fits a polynomial to this mean profile
    (after Savitzky-Golay smoothing), and subtracts this fitted profile
    from the corresponding rows/columns of the layer to correct for vignetting.

    Parameters
    ----------
    dc : DataCube
        The DataCube instance to process.
    axis : int, optional
        The axis along which to calculate the mean and apply correction.
        1 for correcting along rows (profile used for columns),
        2 for correcting along columns (profile used for rows). Defaults to 1.
    slice_params : dict, optional
        Dictionary for slicing behavior before mean calculation.
        Keys: ``"start"`` (int), ``"end"`` (int), ``"step"`` (int).
        Defaults to full slice with step 1.

    Returns
    -------
    DataCube
        The processed DataCube with vignetting removed.

    Raises
    ------
    ValueError
        If the DataCube is empty or axis is not 1 or 2.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read('example.fsm')
    >>> params = {"start":25, "end":50}
    >>> dc.remove_vignetting_poly(slice_params=params, axis=2)
    """
    if dc.cube is None:
        raise ValueError("The DataCube is empty. Please provide a valid cube.")

    if slice_params is None:
        slice_params = {"start": None, "end": None, "step": 1}
    start = slice_params.get("start", None)
    end = slice_params.get("end", None)
    step = slice_params.get("step", 1)

    if axis == 1:
        summed_data = np.mean(dc.cube[:, :, start:end:step], axis=2)
    elif axis == 2:
        summed_data = np.mean(dc.cube[:, start:end:step, :], axis=1)
    else:
        raise ValueError('Axis can only be 1 or 2.')

    corrected_cube = dc.cube.copy().astype(np.float32)

    for i, layer_profile in enumerate(summed_data):
        smoothed_layer_profile = savgol_filter(layer_profile, window_length=71, polyorder=1)
        if axis == 1:
            for j_col in range(dc.cube.shape[2]):
                corrected_cube[i, :, j_col] -= smoothed_layer_profile
        elif axis == 2:
            for j_row in range(dc.cube.shape[1]):
                corrected_cube[i, j_row, :] -= smoothed_layer_profile

    dc.set_cube(corrected_cube)
    return dc


def normalize(dc: DataCube) -> DataCube:
    """
    Normalize spectral information in the data cube to the range [0, 1].

    For each 2D spatial layer in the DataCube, the normalization is performed by:
    `layer = (layer - min_in_layer) / (max_in_layer - min_in_layer)`
    This scales the intensity values of each layer independently across its
    spatial dimensions.

    Parameters
    ----------
    dc : DataCube
        The DataCube instance to normalize.

    Returns
    -------
    DataCube
        The normalized DataCube.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read('example.fsm')
    >>> dc.normalize()
    """
    cube = dc.cube.astype(np.float32)
    min_vals = cube.min(axis=(1, 2), keepdims=True)
    max_vals = cube.max(axis=(1, 2), keepdims=True)

    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1

    cube = (cube - min_vals) / range_vals
    dc.set_cube(cube)
    return dc


def register_layers_best(
        dc: DataCube,
        ref_layer: int = 0,
        max_features: int = 5000,
        match_percent: float = 0.1,
        rot_thresh: float = 20.0,
        scale_thresh: float = 1.1
) -> DataCube:
    """
    Align DataCube layers with robust registration.

    Aligns each slice of `dc.cube` to a reference layer. It uses
    feature-based registration primarily. If feature-based registration
    yields a degenerate homography (based on rotation and scale thresholds)
    or fails, it falls back to Canny-based edge registration.
    Failed alignments are retried once.

    Parameters
    ----------
    dc : DataCube
        The DataCube to process.
    ref_layer : int, optional
        Index of the reference layer, defaults to 0.
    max_features : int, optional
        Maximum features for ORB, defaults to 5000.
    match_percent : float, optional
        Match percentage for ORB, defaults to 0.1.
    rot_thresh : float, optional
        Rotation threshold (degrees) for homography validation,
        defaults to 20.0.
    scale_thresh : float, optional
        Scale threshold for homography validation, defaults to 1.1.
        Checks if max_scale <= scale_thresh and min_scale >= 1/scale_thresh.

    Returns
    -------
    DataCube
        The DataCube with aligned layers.

    Raises
    ------
    RuntimeError
        If alignment fails for a layer after retry.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read('example.fsm')
    >>> dc.register_layers_best()
    """
    aligned_indices = {ref_layer}
    waitlist = set()
    n_layers, H_dim, W_dim = dc.cube.shape

    def try_align(layer_idx: int, current_aligned_indices: set) -> bool:
        # nonlocal dc
        a_img = dc.cube[layer_idx]
        best_alignment_img = None

        for ref_idx in current_aligned_indices:
            try:
                o_img = dc.cube[ref_idx]
                aligned_img_feat, H_ij = feature_registration(
                    o_img, a_img, max_features, match_percent
                )
                angle, S = decompose_homography(H_ij)
                s_ok = (S.max() <= scale_thresh and S.min() >= 1 / scale_thresh)
                if abs(angle) <= rot_thresh and s_ok:
                    print(f"[Layer {layer_idx}] aligned to {ref_idx}: θ={angle:.1f}°, S={S.round(3)}")
                    best_alignment_img = aligned_img_feat
                    break
                else:
                    print(f"[Layer {layer_idx}] reject vs {ref_idx}: θ={angle:.1f}°, S={S.round(3)}")
            except RegistrationError as e:
                print(f"[Layer {layer_idx}] registration to {ref_idx} failed: {e}")

        if best_alignment_img is None:
            print(f"[Layer {layer_idx}] edge-map fallback to reference layer {ref_layer}")
            try:
                ref_img_for_edge = normalize_polarity(dc.cube[ref_layer])
                tgt_img_for_edge = normalize_polarity(a_img)
                edges_ref = auto_canny(ref_img_for_edge)
                edges_tgt = auto_canny(tgt_img_for_edge)
                aligned_img_edge, H_e = feature_registration(
                    edges_ref.astype(float), edges_tgt.astype(float),
                    max_features, match_percent
                )
                h_orig, w_orig = a_img.shape
                best_alignment_img = cv2.warpPerspective(a_img, H_e, (w_orig, h_orig), flags=cv2.INTER_LINEAR)
                angle_e, S_e = decompose_homography(H_e)
                print(f"[Layer {layer_idx}] edges (vs layer {ref_layer}): θ={angle_e:.1f}°, S={S_e.round(3)}")
            except RegistrationError as e:
                print(f"[Layer {layer_idx}] edge registration failed: {e}")
            except Exception as e:
                print(f"[Layer {layer_idx}] unexpected error in edge registration: {e}")

        if best_alignment_img is not None:
            dc.cube[layer_idx] = best_alignment_img
            return True
        return False

    for i in range(n_layers):
        if i == ref_layer:
            continue
        if try_align(i, aligned_indices.copy()):
            aligned_indices.add(i)
        else:
            waitlist.add(i)

    if waitlist:
        print(f"\nRetrying layers: {list(waitlist)}\n")
        for i in list(waitlist):
            if try_align(i, aligned_indices.copy()):
                aligned_indices.add(i)
                waitlist.remove(i)
            else:
                raise RuntimeError(f"Layer {i}: alignment failed after retry.")
    dc.registered = True
    return dc


def remove_vignetting(dc: DataCube, sigma: float = 50, clip: bool = True, epsilon: float = 1e-6) -> DataCube:
    """
    Remove vignetting from a hyperspectral DataCube.

    Corrects vignetting in each spectral band by estimating a smooth
    background using Gaussian blur and then performing flat-field correction.
    The background is normalized by its mean before correction.

    Parameters
    ----------
    dc : DataCube
        The input DataCube (bands, height, width).
    sigma : float, optional
        Standard deviation for Gaussian blur, controlling smoothness.
        Larger sigma means coarser background estimation. Defaults to 50.
    clip : bool, optional
        If True and the original DataCube dtype is integer,
        clip output values to the valid range of that integer type.
        Defaults to True.
    epsilon : float, optional
        A small constant to add to the background before division
        to prevent division by zero errors. Defaults to 1e-6.

    Returns
    -------
    DataCube
        The DataCube with vignetting corrected. The output cube has the
        same shape and dtype as the input.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read('example.fsm')
    >>> dc.remove_vignetting()
    """
    corrected_cube = np.empty_like(dc.cube)
    orig_dtype = dc.cube.dtype
    is_int = np.issubdtype(orig_dtype, np.integer)

    for i in range(dc.cube.shape[0]):
        band = dc.cube[i].astype(np.float64)
        background = gaussian_filter(band, sigma=sigma)
        background = np.maximum(background, epsilon)
        background_mean = background.mean()
        if background_mean > epsilon:
            background /= background_mean
        else:
            background = np.ones_like(background, dtype=np.float64)
        corrected_band = band / background
        if is_int:
            info = np.iinfo(orig_dtype)
            corrected_band = np.round(corrected_band)
            corrected_band = np.clip(corrected_band, info.min, info.max)
        corrected_cube[i] = corrected_band.astype(orig_dtype)
    dc.set_cube(corrected_cube)
    return dc


def upscale_datacube_edsr(dc: DataCube, scale: int, model_path: str):
    """
    Upscale the spatial dimensions of a DataCube using the EDSR super-resolution model.

    This function applies the EDSR (Enhanced Deep Super-Resolution) model from OpenCV’s
    dnn_superres module to each spectral slice of the given DataCube. Since EDSR
    expects a 3-channel input, each single-band slice is duplicated across three
    channels before processing. The output slices are then reassembled into a new
    DataCube with upscaled spatial dimensions.

    Parameters
    ----------
    dc : DataCube
        An instance of the DataCube class. Must have attributes:
        - datacube.cube: numpy array of shape (v, x, y)
        - datacube.wavelength: list of length v
    scale : int
        The upscaling factor (e.g., 2, 3, or 4) supported by the EDSR model.
    model_path : str
        Filesystem path to the pretrained EDSR `.pb` model file
        (e.g., `"EDSR_x4.pb"`).

    Returns
    -------
    DataCube
        A new DataCube instance whose `.cube` has shape
        (v, x * scale, y * scale) and the same `.wavelength` list.

    Raises
    ------
    FileNotFoundError
        If the specified `model_path` does not exist or is unreadable.
    cv2.error
        If OpenCV fails to load the model or perform upsampling.
    ValueError
        If the `scale` is not one of the factors supported by the loaded model.

    Notes
    -----
    - Requires `opencv-contrib-python>=4.3.0`.
    - Processing is done slice-by-slice and may be slow for large cubes.
    - Memory usage grows by approximately `scale^2`.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read("hyperspectral.fsm")
    >>> dc.upscale_datacube_edsr(scale=4, model_path="EDSR_x4.pb")
    >>> print(dc.cube.shape)
    (v, x*4, y*4)
    """
    # Create EDSR super-res object
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("edsr", scale)

    v, x, y = dc.shape
    new_x, new_y = x * scale, y * scale
    up_cube = np.empty((v, new_x, new_y), dtype=dc.cube.dtype)

    for i in range(v):
        # Extract single-band slice
        band = dc.cube[i, :, :]

        # Convert to 3-channel BGR by stacking
        bgr = cv2.merge([band, band, band])

        # Upsample
        up_bgr = sr.upsample(bgr)

        # Take one channel (all channels are identical)
        up_band = up_bgr[:, :, 0]

        up_cube[i, :, :] = up_band

    # Build new DataCube
    dc.set_cube(up_cube)
    return dc


def upscale_datacube_espcn(dc: DataCube, scale: int, model_path: str):
    """
    Upscale the spatial dimensions of a DataCube using the ESPCN super-resolution model.

    This function applies the ESPCN (Efficient Sub-Pixel Convolutional Neural Network)
    model from OpenCV’s dnn_superres module to each spectral slice of the given DataCube.
    Since ESPCN expects a 3-channel input, each single-band slice is duplicated across
    three channels before processing. The output slices are then reassembled into a new
    DataCube with upscaled spatial dimensions.

    Parameters
    ----------
    dc : DataCube
        An instance of the DataCube class. Must have attributes:
        - .cube: numpy array of shape (v, x, y)
        - .wavelength: list of length v
    scale : int
        The upscaling factor (2, 3, or 4) supported by the ESPCN model.
    model_path : str
        Filesystem path to the pretrained ESPCN `.pb` model file
        (e.g., "ESPCN_x3.pb").

    Returns
    -------
    DataCube
        A new DataCube instance whose `.cube` has shape
        (v, x * scale, y * scale) and the same `.wavelength` list.

    Raises
    ------
    FileNotFoundError
        If the specified `model_path` does not exist.
    ValueError
        If `scale` is not in {2, 3, 4}.
    cv2.error
        If OpenCV fails to load the model or perform upsampling.

    Notes
    -----
    - Requires `opencv-contrib-python>=4.3.0`.
    - Processing is done slice-by-slice and may be slow for large cubes.
    - Memory usage grows by approximately `scale**2`.

    Examples
    --------
    >>> import wizard
    >>> dc = wizard.read("test.fsm")
    >>> dc.upscale_datacube_espcn(scale=3, model_path="ESPCN_x3.pb")
    >>> print(dc.cube.shape)
    (v, x*3, y*3)
    """
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if scale not in (2, 3, 4):
        raise ValueError(f"ESPCN only supports scale factors 2, 3, or 4, got {scale}")

    # Initialize ESPCN super-resolver
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("espcn", scale)

    v, x, y = dc.shape
    new_x, new_y = x * scale, y * scale
    up_cube = np.empty((v, new_x, new_y), dtype=dc.cube.dtype)

    for i in range(v):
        # extract single-band slice
        band = dc.cube[i, :, :]

        # create 3-channel image
        bgr = cv2.merge([band, band, band])

        # run ESPCN upsampling
        up_bgr = sr.upsample(bgr)

        # channels are identical: pick one
        up_band = up_bgr[:, :, 0]
        up_cube[i, :, :] = up_band

    # assemble new DataCube
    dc.set_cube(up_cube)
    return dc


def upscale_datacube_with_reference(dc: DataCube, reference_image: np.ndarray) -> 'DataCube':
    """
    Upscales a DataCube to match the spatial resolution of a reference image using ESRGAN.

    Each spectral band of the DataCube is individually upscaled using the ESRGAN model
    by treating the single band as a pseudo-grayscale image. The resulting DataCube has
    the same spatial resolution as the reference image.

    Parameters
    ----------
    dc : DataCube
        The input DataCube to be upscaled. Expected shape (v, x, y).

    reference_image : np.ndarray
        A high-resolution reference image (e.g., RGB) that defines the target (x, y) resolution.

    Returns
    -------
    DataCube
    A new DataCube with the same number of bands, but upscaled to match the reference image's spatial resolution.

    Raises
    ------
    ValueError
    If the reference image resolution is smaller than the datacube resolution.

    Notes
    -----
    This method uses the ESRGAN model via TensorFlow Hub. The model is applied to each spectral band independently.

    Examples
    --------
    >>> upscaled_cube = upscale_datacube_with_reference(cube, ref_image)
    """
    import tensorflow as tf
    import tensorflow_hub as hub

    # Load ESRGAN model
    model_url = "https://tfhub.dev/captain-pool/esrgan-tf2/1"
    model = hub.load(model_url)

    # Target resolution from reference image
    target_x, target_y = reference_image.shape[:2]

    v, x, y = dc.shape

    if x >= target_x or y >= target_y:
        raise ValueError("Reference image must be larger than the DataCube in spatial dimensions.")

    upscaled_bands = []

    for i in range(v):
        band = dc.cube[i, :, :]

        # Normalize and expand dims for ESRGAN
        img = (band / band.max() * 255).astype(np.uint8)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img_rgb = tf.convert_to_tensor(img_rgb, dtype=tf.float32)

        # Ensure divisible by 4
        imageSize = (tf.convert_to_tensor(img_rgb.shape[:-1]) // 4) * 4
        cropped_image = tf.image.crop_to_bounding_box(
            img_rgb, 0, 0, imageSize[0], imageSize[1]
        )
        preprocessed_image = tf.expand_dims(cropped_image, 0)

        # Run super-resolution
        sr_result = model(preprocessed_image)
        sr_image = tf.squeeze(sr_result).numpy() / 255.0

        # Convert back to single band and resize to match reference
        sr_gray = cv2.cvtColor((sr_image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        resized_band = cv2.resize(sr_gray.astype(np.float32), (target_y, target_x), interpolation=cv2.INTER_CUBIC)

        upscaled_bands.append(resized_band)

    upscaled_cube_array = np.stack(upscaled_bands, axis=0)

    dc.set_cube(upscaled_cube_array)
    return dc


def upscale_datacube_fsrcnn(dc, scale, model_path):
    """
    Upscale the spatial dimensions of a DataCube using the FSRCNN super-resolution model.

    This function applies the FSRCNN (Fast Super-Resolution Convolutional Neural Network)
    model from OpenCV’s dnn_superres module to each spectral slice of the given DataCube.
    Since FSRCNN expects a 3-channel input, each single-band slice is duplicated across three
    channels before processing. The output slices are then reassembled into a new DataCube
    with upscaled spatial dimensions.

    Parameters
    ----------
    dc : DataCube
        An instance of the DataCube class. Must have attributes:
        - .cube: numpy array of shape (v, x, y)
        - .wavelength: list of length v
    scale : int
        The upscaling factor (2, 3, or 4) supported by the FSRCNN model.
    model_path : str
        Filesystem path to the pretrained FSRCNN `.pb` model file
        (e.g., "FSRCNN_x3.pb").

    Returns
    -------
    DataCube
        A new DataCube instance whose `.cube` has shape
        (v, x * scale, y * scale) and the same `.wavelength` list.

    Raises
    ------
    FileNotFoundError
        If the specified `model_path` does not exist.
    ValueError
        If `scale` is not in {2, 3, 4}.
    cv2.error
        If OpenCV fails to load the model or perform upsampling.

    Notes
    -----
    - Requires `opencv-contrib-python>=4.3.0`.
    - Processing is done slice-by-slice and may be slow for large cubes.
    - Memory usage grows by approximately `scale**2`.

    Examples
    --------
    >>> dc = wizard.read("hyperspectral.npy", wavelengths=[...])
    >>> up_dc = upscale_datacube_fsrcnn(dc, scale=3, model_path="FSRCNN_x3.pb")
    >>> print(up_dc.cube.shape)
    (v, x*3, y*3)
    """
    # Validate model file
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    # Validate supported scale factors
    if scale not in (2, 3, 4):
        raise ValueError(f"FSRCNN only supports scale factors 2, 3, or 4, got {scale}")

    # Initialize FSRCNN super-resolver
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("fsrcnn", scale)

    # Prepare new cube
    v, x, y = dc.cube.shape
    new_x, new_y = x * scale, y * scale
    up_cube = np.empty((v, new_x, new_y), dtype=dc.cube.dtype)

    # Upscale each spectral band
    for i in range(v):
        band = dc.cube[i, :, :]
        bgr = cv2.merge([band, band, band])
        up_bgr = sr.upsample(bgr)
        up_band = up_bgr[:, :, 0]
        up_cube[i, :, :] = up_band

    # Create and return new DataCube
    dc.set_cube(up_cube)
    return dc


def remove_vignette(dc: DataCube, vignette_map: np.ndarray, flip: bool = False) -> DataCube:
    """
    Subtract a vignette pattern from every spectral layer.

    Removes spatial vignetting by subtracting the provided vignette_map
    from each (x, y) layer in the data cube. If flip=True, the vignette
    pattern is inverted (dark center → bright center) before subtraction.

    Parameters
    ----------
    dc: DataCube
        An instance of the DataCube class. Must have attributes:
        - .cube: numpy array of shape (v, x, y)
        - .wavelength: list of length v
    vignette_map : np.ndarray
        2D array of shape (x, y) representing the vignette intensity to subtract.
        Values should be on the same scale as the cube’s pixel intensities.
    flip : bool, default=False
        If True, invert the vignette_map before subtraction.

    Returns
    -------
    None
        Modifies the DataCube.cube in-place.

    Raises
    ------
    ValueError
        If vignette_map.shape does not match the spatial dimensions of the cube.

    Notes
    -----
    - After subtraction, any negative values in the cube are clipped to zero.
    - Assumes cube and vignette_map share the same intensity scale.

    Examples
    --------
    >>> dc = DataCube(cube=np.random.rand(10, 256, 256), wavelength=list(np.linspace(400,700,10)))
    >>> # Remove standard vignette (darker at edges, brighter center)
    >>> dc.remove_vignette(vignette_map=my_vignette_image)
    >>> # Remove flipped vignette (darker center, brighter edges)
    >>> dc.remove_vignette(vignette_map=my_vignette_image, flip=True)
    """
    # Check that the vignette map matches spatial dims
    if vignette_map.shape != dc.cube.shape[1:]:
        raise ValueError(
            f"vignette_map shape {vignette_map.shape} does not match cube spatial shape {dc.cube.shape[1:]}"
        )

    cube = dc.cube.copy()

    # Optionally invert the vignette pattern
    if flip:
        vignette_map = vignette_map.max() - vignette_map

    # Subtract vignette from each layer
    # Using broadcasting: vignette_map has shape (x, y), expand to (1, x, y)
    cube -= vignette_map[np.newaxis, :, :]

    # Clip negative values to zero
    np.clip(cube, a_min=0, a_max=None, out=cube)

    dc.set_cube(cube)

    return dc


def uniform_filter_dc(dc, size=3):
    """
    Smooth each spectral band of a DataCube using a uniform spatial filter.

    Applies a uniform filter of the given window size to every slice (band) in the
    DataCube’s cube, reducing spatial noise by averaging within a local neighborhood.
    The operation modifies the DataCube in place.

    Parameters
    ----------
    dc : DataCube
        The DataCube instance whose `cube` attribute (a numpy array of shape (v, x, y))
        will be smoothed across the spatial dimensions for each spectral band.
    size : int, optional
        The size of the square window used by `scipy.ndimage.uniform_filter` for
        smoothing. Must be a positive odd integer. Defaults to 3.

    Returns
    -------
    DataCube
        The same DataCube instance, with its `cube` attribute replaced by the
        smoothed data of shape (v, x, y).

    Raises
    ------
    ValueError
        If `size` is not a positive integer.

    Notes
    -----
    - Requires `scipy.ndimage.uniform_filter` to be imported.
    - Smoothing is performed independently on each spectral band.
    - This function updates `dc` in place; no new DataCube is created.

    """
    if not isinstance(size, int) or size < 1:
        raise ValueError("`size` must be a positive integer")
    cube = dc.cube
    for i in range(dc.cube.shape[0]):
        cube[i] = uniform_filter(cube[i], size=size)
    dc.set_cube(cube)
    return dc
