"""
_utils/helper.py
=================

.. module:: helper
   :platform: Unix
   :synopsis: Helper functions for processing wave and cube values.

Module Overview
---------------

This module contains helper functions to assist in processing wave and cube values.

Functions
---------

.. autofunction:: find_nex_greater_wave
.. autofunction:: find_nex_smaller_wave

"""

import cv2
import warnings
import numpy as np
from skimage.feature import canny


class RegistrationError(Exception):
    """Custom exception for registration errors."""

    pass


def find_nex_greater_wave(waves, wave_1: int, maximum_deviation: int = 5) -> int:
    """
    Find the next greater wave value within a specified deviation.

    This function searches for the smallest wave value greater than or equal to `wave_1`
    that exists in the `waves` list, within a deviation range up to `maximum_deviation`.
    If no such wave is found, the function returns -1.

    Parameters
    ----------
    waves : list[int]
        A list of integer wave values to search within.
    wave_1 : int
        The reference wave value to find the next greater wave after.
    maximum_deviation : int, optional
        The maximum positive offset from `wave_1` to consider (default is 5).

    Returns
    -------
    int
        The next greater wave value found within the range, or -1 if none exists.

    Raises
    ------
    None

    Notes
    -----
    The function stops searching once it finds the first match within the allowed range.

    Examples
    --------
    >>> find_nex_greater_wave([400, 405, 410, 415], 403)
    405

    >>> find_nex_greater_wave([400, 405, 410, 415], 416)
    -1
    """
    wave_next = -1

    for n in range(maximum_deviation):
        wave_n = wave_1 + n

        if wave_n in waves:
            wave_next = wave_n
            break

    return wave_next


def find_nex_smaller_wave(waves, wave_1: int, maximum_deviation: int = 5) -> int:
    """
    Find the next smaller wave value within a specified deviation.

    This function searches for the largest wave value smaller than or equal to `wave_1`
    that exists in the `waves` list, within a deviation range up to `maximum_deviation`.
    If no such wave is found, the function returns -1.

    Parameters
    ----------
    waves : list[int]
        A list of integer wave values to search within.
    wave_1 : int
        The reference wave value to find the next smaller wave before.
    maximum_deviation : int, optional
        The maximum negative offset from `wave_1` to consider (default is 5).

    Returns
    -------
    int
        The next smaller wave value found within the range, or -1 if none exists.

    Raises
    ------
    None

    Notes
    -----
    The function stops searching once it finds the first match within the allowed range.

    Examples
    --------
    >>> find_nex_smaller_wave([390, 395, 400, 405], 402)
    400

    >>> find_nex_smaller_wave([390, 395, 400, 405], 389)
    -1
    """
    wave_next = -1

    for n in range(maximum_deviation):
        wave_n = wave_1 - n

        if wave_n in waves:
            wave_next = wave_n
            break

    return wave_next


def normalize_spec(spec):
    """
    Normalize a spectrum to the range [0, 1].

    This function scales the input spectral array so that its values lie between 0 and 1.
    If the spectrum has constant values (i.e., no variation), it is returned unchanged.
    The function ensures numerical stability using `np.clip`.

    Parameters
    ----------
    spec : np.ndarray
        A one-dimensional NumPy array representing the spectrum to normalize.

    Returns
    -------
    np.ndarray
        A normalized NumPy array with values scaled to the [0, 1] range, or the original
        array if it has no dynamic range.

    Raises
    ------
    None

    Notes
    -----
    Normalization is only performed if the minimum and maximum values differ.

    Examples
    --------
    >>> import numpy as np
    >>> normalize_spec(np.array([2.0, 4.0, 6.0]))
    array([0. , 0.5, 1. ])

    >>> normalize_spec(np.array([5.0, 5.0, 5.0]))
    array([5., 5., 5.])
    """
    spec_min, spec_max = spec.min(), spec.max()
    return np.clip((spec - spec_min) / (spec_max - spec_min), 0, 1) if spec_max > spec_min else spec


def feature_regestration(o_img: np.ndarray, a_img: np.ndarray, max_features: int = 5000, match_percent: float = 0.1):
    """
    Perform feature-based registration of two grayscale images.

    This function aligns a moving image (`a_img`) to a reference image (`o_img`) using
    ORB keypoints and brute-force Hamming descriptor matching. It returns the aligned image
    and the computed homography transformation matrix.

    Parameters
    ----------
    o_img : np.ndarray
        A 2D NumPy array representing the reference (original) grayscale image.
    a_img : np.ndarray
        A 2D NumPy array representing the image to be aligned (affine-transformed).
    max_features : int, optional
        The maximum number of ORB features to detect (default is 5000).
    match_percent : float, optional
        The fraction of best matches to use when computing the homography (default is 0.1).

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        A tuple containing:
        - The aligned image (np.ndarray) warped to match the reference.
        - The homography matrix (np.ndarray) used for the transformation.

    Raises
    ------
    ValueError
        If feature matching fails or not enough good matches are found to compute homography.

    Notes
    -----
    Images are automatically normalized and converted to 8-bit if needed. The function uses
    RANSAC to compute a robust homography estimate from feature correspondences.

    Examples
    --------
    >>> import numpy as np
    >>> import cv2
    >>> ref_img = cv2.imread("reference.png", cv2.IMREAD_GRAYSCALE)
    >>> mov_img = cv2.imread("moving.png", cv2.IMREAD_GRAYSCALE)
    >>> aligned, H = feature_regestration(ref_img, mov_img)
    >>> print(H.shape)
    (3, 3)
    """
    orb = cv2.ORB_create(max_features)

    if o_img.dtype != np.uint8:
        o_img = (o_img - o_img.min()) / (o_img.max() - o_img.min())
        o_img = (o_img * 255).astype(np.uint8)

    if a_img.dtype != np.uint8:
        a_img = (a_img - a_img.min()) / (a_img.max() - a_img.min())
        a_img = (a_img * 255).astype(np.uint8)

    a_img_key, a_img_descr = orb.detectAndCompute(a_img, None)
    o_img_key, o_img_descr = orb.detectAndCompute(o_img, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(a_img_descr, o_img_descr, None)

    matches = list(matches)
    # Sort matches by score
    matches = sorted(matches, key=lambda x: x.distance)

    # Remove not so good matches
    num_good_matches = int(len(matches) * match_percent)
    matches = matches[: num_good_matches]

    # Extract location of good matches
    a_points = np.zeros((len(matches), 2), dtype=np.float32)
    o_points = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        a_points[i, :] = a_img_key[match.queryIdx].pt
        o_points[i, :] = o_img_key[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(a_points, o_points, cv2.RANSAC)

    # Use homography
    height, width = o_img.shape
    aligned_img = cv2.warpPerspective(a_img, h, (width, height))

    return aligned_img, h


def feature_registration(o_img: np.ndarray, a_img: np.ndarray, max_features: int = 5000, match_percent: float = 0.1) -> tuple[np.ndarray, np.ndarray]:
    """
    Perform ORB-based feature registration.

    Aligns `a_img` to `o_img` using ORB features and RANSAC
    to find the homography matrix.

    Parameters
    ----------
    o_img : numpy.ndarray
        The target (reference) image.
    a_img : numpy.ndarray
        The source image to be aligned.
    max_features : int, optional
        Maximum number of ORB features to detect, defaults to 5000.
    match_percent : float, optional
        Percentage of best matches to use for homography, defaults to 0.1.

    Returns
    -------
    aligned_img : numpy.ndarray
        The `a_img` warped to align with `o_img`.
    H : numpy.ndarray
        The 3x3 homography matrix mapping points from `a_img` to `o_img`.

    Raises
    ------
    RegistrationError
        If no descriptors are found, not enough good matches are found,
        or homography estimation fails.
    """
    def to_uint8(im: np.ndarray) -> np.ndarray:
        """Convert image to uint8, normalizing if necessary."""
        if im.dtype != np.uint8:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in true_divide")
                warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in divide")
                min_val, max_val = im.min(), im.max()
                if min_val == max_val:
                    im_norm = np.zeros_like(im, dtype=np.float32)
                else:
                    im_norm = (im.astype(np.float32) - min_val) / (max_val - min_val)
                im_norm = np.nan_to_num(im_norm, nan=0.0, posinf=1.0, neginf=0.0)
            im = (im_norm * 255).astype(np.uint8)
        return im

    o8, a8 = to_uint8(o_img), to_uint8(a_img)
    orb = cv2.ORB_create(max_features)
    kp1, des1 = orb.detectAndCompute(a8, None)
    kp2, des2 = orb.detectAndCompute(o8, None)

    if des1 is None or des2 is None:
        raise RegistrationError("No descriptors found")

    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(des1, des2)
    matches = sorted(matches, key=lambda m: m.distance)
    n_good = max(4, int(len(matches) * match_percent))
    matches = matches[:n_good]

    if len(matches) < 4:
        raise RegistrationError(f"Not enough good matches found ({len(matches)}/{n_good})")

    ptsA = np.float32([kp1[m.queryIdx].pt for m in matches])
    ptsO = np.float32([kp2[m.trainIdx].pt for m in matches])

    H, mask = cv2.findHomography(ptsA, ptsO, cv2.RANSAC)
    if H is None:
        raise RegistrationError("Homography estimation failed")

    H = H / H[2, 2]
    h_o, w_o = o_img.shape
    aligned = cv2.warpPerspective(a_img, H, (w_o, h_o), flags=cv2.INTER_LINEAR)
    return aligned, H


def _process_slice(spec_out_flat: np.ndarray, spikes_flat: np.ndarray, idx: int, window: int) -> tuple:
    """
    Process a single slice to remove spikes.

    Replaces spikes with the mean of neighboring values within a given window.

    Parameters
    ----------
    spec_out_flat : numpy.ndarray
        Flattened output spectrum data from the data cube.
    spikes_flat : numpy.ndarray
        Flattened boolean array indicating spike detections.
    idx : int
        Index of the current slice to process.
    window : int
        Size of the window for mean calculation.

    Returns
    -------
    tuple
        A tuple containing the index of the processed slice and the
        modified spectrum slice.
    """
    w_h = int(window / 2)
    spike = spikes_flat[idx]
    tmp = np.copy(spec_out_flat[idx])
    for spk_idx in np.where(spike)[0]:
        window_min = max(0, spk_idx - w_h)
        window_max = min(len(tmp), spk_idx + w_h + 1)
        if window_min == spk_idx:
            window_data = tmp[spk_idx + 1:window_max]
        elif window_max == spk_idx + 1:
            window_data = tmp[window_min:spk_idx]
        else:
            window_data = np.concatenate((tmp[window_min:spk_idx], tmp[spk_idx + 1:window_max]))
        if len(window_data) > 0:
            tmp[spk_idx] = np.mean(window_data)
    return idx, tmp


def decompose_homography(H: np.ndarray) -> tuple[float, np.ndarray]:
    """
    Extract rotation angle and singular values from the 2x2 linear part of H.

    Parameters
    ----------
    H : numpy.ndarray
        The 3x3 homography matrix.

    Returns
    -------
    angle : float
        The rotation angle in degrees.
    S : numpy.ndarray
        The singular values (scales) from the 2x2 affine part of H.
    """
    A = H[:2, :2]
    U, S, Vt = np.linalg.svd(A)
    R = U.dot(Vt)
    angle = np.degrees(np.arctan2(R[1, 0], R[0, 0]))
    return angle, S


def auto_canny(img: np.ndarray, sigma: float = 0.33) -> np.ndarray:
    """
    Automatic Canny edge detection using median-based thresholds.

    Assumes img is a float in the range [0,1].

    Parameters
    ----------
    img : numpy.ndarray
        Input image (float, range [0,1]).
    sigma : float, optional
        Sigma value for threshold calculation, defaults to 0.33.

    Returns
    -------
    numpy.ndarray
        Binary edge map from Canny detector.
    """
    v = np.median(img)
    lower = max(0.0, (1.0 - sigma) * v)
    upper = min(1.0, (1.0 + sigma) * v)
    return canny(img, low_threshold=lower, high_threshold=upper)


def normalize_polarity(img: np.ndarray) -> np.ndarray:
    """
    Ensure features are dark-on-light by inverting if necessary.

    If the image is mostly bright (mean pixel value > 0.5 after
    normalization to [0,1]), it inverts the image.
    Handles float or uint8 inputs transparently, returning a float32
    image in the range [0,1].

    Parameters
    ----------
    img : numpy.ndarray
        Input image.

    Returns
    -------
    numpy.ndarray
        Polarity-normalized image as float32 in [0,1].

    """
    if img.dtype == np.uint8:
        img_f = img.astype(np.float32) / 255.0
    else:
        min_val, max_val = img.min(), img.max()
        if min_val < 0.0 or max_val > 1.0:
            if max_val == min_val:
                img_f = np.zeros_like(img, dtype=np.float32)
            else:
                img_f = (img.astype(np.float32) - min_val) / (max_val - min_val)
        else:
            img_f = (img.astype(np.float32) - min_val) / (max_val - min_val)

    if np.mean(img_f) > 0.5:
        img_f = 1.0 - img_f
    return img_f
