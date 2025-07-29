"""
_processing/spectral.py
========================

.. module:: spectral
   :platform: Unix
   :synopsis: Provides methods for processing data cubes, including spike removal and intensity calculations.

Module Overview
---------------

This module includes functions for processing data cubes. It calculates the modified z-score of a data cube to
identify intensity differences, removes spikes from the data by replacing them with mean values of neighboring data,
and processes data cubes in parallel to enhance performance.

"""

import numpy as np
from scipy.signal import savgol_filter, butter, filtfilt
from scipy import sparse
from scipy.sparse.linalg import spsolve


def smooth_savgol(spectrum, window_length: int = 11, polyorder: int = 2):
    """
    Apply a Savitzky-Golay filter to smooth a given spectrum.

    :param spectrum: Input spectrum to be smoothed.
    :type spectrum: numpy.ndarray
    :param window_length: Length of the filter window, must be a positive odd integer.
    :type window_length: int, optional
    :param polyorder: Order of the polynomial used to fit the samples.
    :type polyorder: int, optional
    :return: Smoothed spectrum.
    :rtype: numpy.ndarray
    """
    return savgol_filter(spectrum, window_length=window_length, polyorder=polyorder)


def smooth_moving_average(spectrum, window_size: int = 5):
    """
    Apply a moving average filter to smooth a given spectrum.

    :param spectrum: Input spectrum to be smoothed.
    :type spectrum: numpy.ndarray
    :param window_size: Size of the moving window.
    :type window_size: int, optional
    :return: Smoothed spectrum.
    :rtype: numpy.ndarray
    """
    return np.convolve(spectrum, np.ones(window_size) / window_size, mode='valid')


def smooth_butter_lowpass(spectrum, cutoff: float = .1, fs: float = 1., order: int = 5):
    """
    Apply a Butterworth low-pass filter to the input spectrum.

    :param spectrum: Input spectrum to be filtered.
    :type spectrum: numpy.ndarray
    :param cutoff: Cutoff frequency of the filter.
    :type cutoff: float, optional
    :param fs: Sampling frequency of the input signal.
    :type fs: float, optional
    :param order: Order of the filter.
    :type order: int, optional
    :return: Filtered spectrum.
    :rtype: numpy.ndarray
    """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, spectrum)


def spec_baseline_als(spectrum: np.array, lam: float, p: float, niter: int = 10) -> np.array:
    """
    Perform baseline correction using Asymmetric Least Squares Smoothing.

    :param spectrum: Input spectrum to be smoothed.
    :type spectrum: numpy.ndarray
    :param lam: Smoothness parameter, typically between 10^2 and 10^9.
    :type lam: float
    :param p: Asymmetry parameter, usually between 0.001 and 0.1.
    :type p: float
    :param niter: Number of iterations.
    :type niter: int, optional
    :return: Smoothed baseline.
    :rtype: numpy.ndarray
    """
    m = len(spectrum)
    D = sparse.diags([1, -2, 1], [0, 1, 2], shape=(m, m)).tocsc()
    w = np.ones(m)
    for _ in range(niter):
        W = sparse.diags(w, 0).tocsc()
        Z = W + lam * D @ D.T
        z = spsolve(Z, w * spectrum)
        w = p * (spectrum > z) + (1 - p) * (spectrum < z)
    return z


def calculate_modified_z_score(spectrum: np.array):
    """
    Calculate the modified z-score of a data cube by computing the difference in intensity along the first axis.

    :param spectrum: spectrum
    :type spectrum: numpy.ndarray
    :return: Modified z-score representing the difference in intensity along the first axis.
    :rtype: numpy.ndarray
    """
    mean_spectrum = np.mean(spectrum, keepdims=True)  # Compute mean
    return spectrum - mean_spectrum  # Subtract mean from each element


def get_ratio_two_specs(spectrum: np.array, waves: np.array, wave_1: int, wave_2: int) -> np.array:
    """
    Calculate the ratio between two selected wavelengths in the spectrum.

    :param spectrum: Main spectrum from which the wavelengths will be selected.
    :type spectrum: numpy.ndarray
    :param waves: Array of wavelengths for the given spectrum.
    :type waves: numpy.ndarray
    :param wave_1: First selected wavelength.
    :type wave_1: int
    :param wave_2: Second selected wavelength.
    :type wave_2: int
    :return: Ratio of the two selected wavelengths.
    :rtype: numpy.ndarray
    """
    idx_1 = np.searchsorted(waves, wave_1)
    idx_2 = np.searchsorted(waves, wave_2)
    return spectrum[idx_1] / spectrum[idx_2] if idx_1 < len(waves) and idx_2 < len(waves) else -1


def get_sub_tow_specs(spectrum: np.array, waves: np.array, wave_1: int, wave_2: int) -> np.array:
    """
    Subtract two selected wavelengths from a spectrum.

    :param spectrum: Main spectrum from which the wavelengths will be selected.
    :type spectrum: numpy.ndarray
    :param waves: Array of wavelengths for the given spectrum.
    :type waves: numpy.ndarray
    :param wave_1: First selected wavelength.
    :type wave_1: int
    :param wave_2: Second selected wavelength.
    :type wave_2: int
    :return: Difference of the two selected wavelengths.
    :rtype: numpy.ndarray
    """
    idx_1 = np.searchsorted(waves, wave_1)
    idx_2 = np.searchsorted(waves, wave_2)
    return spectrum[idx_1] - spectrum[idx_2] if idx_1 < len(waves) and idx_2 < len(waves) else -1


def signal_to_noise(spectrum: np.array) -> float:
    """
    Calculate the signal-to-noise ratio (SNR) of a given spectrum.

    :param spectrum: 1D array representing the intensity values of the spectrum.
    :type spectrum: numpy.ndarray
    :return: Signal-to-noise ratio (SNR) value in decibels (dB).
    :rtype: float
    """
    mean = np.mean(spectrum)
    std = np.std(spectrum)
    return 20 * np.log10(abs(mean / std)) if std != 0 else 0


def del_leading_zeros(spectrum, idx: int = -1, auto_offset: int = 5):
    """
    Remove leading zeros from a spectrum array.

    :param spectrum: Input spectrum array.
    :type spectrum: numpy.ndarray
    :param idx: Index value for cutting.
    :type idx: int, optional
    :param auto_offset: Number of values to be deleted in auto mode (idx + auto_offset).
    :type auto_offset: int, optional
    :return: Spectrum array with leading zeros removed.
    :rtype: numpy.ndarray
    """
    if idx == -1:
        idx = 0
        for idx, i in enumerate(spectrum):
            if i != 0:
                break
        idx += auto_offset
    return spectrum[idx:]


def del_last_zeros(spectrum, idx: int = -1, auto_offset: int = 5):
    """
    Remove trailing zeros from a spectrum array.

    :param spectrum: Input spectrum array.
    :type spectrum: numpy.ndarray
    :param idx: Index value for cutting.
    :type idx: int, optional
    :param auto_offset: Number of values to be deleted in auto mode (idx + auto_offset).
    :type auto_offset: int, optional
    :return: Spectrum array with trailing zeros removed.
    :rtype: numpy.ndarray
    """
    if idx == -1:
        idx = 0
        for idx, i in enumerate(reversed(spectrum)):
            if i != 0:
                break
        idx += auto_offset
    return spectrum[:idx]
