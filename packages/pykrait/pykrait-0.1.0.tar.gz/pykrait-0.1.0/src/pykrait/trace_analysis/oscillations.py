import numpy as np
from typing import Tuple

def calculate_std_cov(peak_series: np.ndarray, frame_interval: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    calculates the standard deviation and coefficient of variation (cov) of the peak intervals for each ROI in the peak series.

    :param peak_series: T x n_roi binary array with 1s at the peak locations and 0s elsewhere
    :type peak_series: np.ndarray
    :param frame_interval: frame interval in seconds of the recording
    :type frame_interval: float
    :return: returns standard deviation (sd) and coefficient of variation (cov) of the peak intervals for each ROI
    :rtype: Tuple[np.ndarray, np.ndarray]
    """
    # could probably be further sped up with proper vectorization

    peak_indices = [np.nonzero(col)[0] for col in peak_series.T]
    peak_diff = [np.ediff1d(indices) * frame_interval for indices in peak_indices]
    peak_std = [np.std(row) for row in peak_diff]
    peak_cov = [np.std(row) / np.mean(row) if len(row) > 1 and np.mean(row) != 0 else np.nan for row in peak_diff]

    return np.asarray(peak_std), np.asarray(peak_cov)

def calculate_std_cov_thresholds(filtered_peak_series:np.ndarray, std_quantile:float, cov_quantile:float, frame_interval:float, n_iter:int=100) -> Tuple[float, float]:
    """
    finds the threshold of standard deviation and coefficient of variation for the random control data.

    :param filtered_peak_series: (T x n_roi) binary array with 1s at the peak locations and 0s elsewhere, where n_roi are ROIs with at least 4 peaks
    :type filtered_peak_series: np.ndarray
    :param std_quantile: quantile for standard deviation threshold
    :type std_quantile: float
    :param cov_quantile: quantile for coefficient of variation threshold
    :type cov_quantile: float
    :param n_iter: number of iterations for random control
    :type n_iter: 100
    :param frame_interval: frame interval of the recording in seconds
    :type frame_interval: float
    :return: returns the standard deviation and coefficient of variation thresholds for the random control data
    :rtype: Tuple[float, float]
    """
    # for the random control, generate a stacked peak series
    stacked_peak_series = np.hstack([filtered_peak_series] * n_iter)
    
    # shuffle each column independently
    T, n = stacked_peak_series.shape
    idx = np.argsort(np.random.rand(T, n), axis=0)
    stacked_peak_series = np.take_along_axis(stacked_peak_series, idx, axis=0)

    # calculate std and cv for each column
    stds, cvs = calculate_std_cov(stacked_peak_series, frame_interval)

    # calculate the quantiles
    std_threshold = np.quantile(stds, std_quantile)
    cov_threshold = np.quantile(cvs, cov_quantile)

    return std_threshold, cov_threshold

def find_oscillating_rois(filtered_peak_series: np.ndarray, std_threshold: float, cov_threshold: float, frame_interval: float) -> Tuple[float, int, int, float, int, int]:
    """
    finds the oscillating ROIs based on the standard deviation and coefficient of variation thresholds.

    :param filtered_peak_series: T x n_roi binary array with 1s at the peak locations and 0s elsewhere
    :type filtered_peak_series: np.ndarray
    :param std_threshold: threshold for standard deviation of peak intervals
    :type std_threshold: float
    :param cov_threshold: threshold for coefficient of variation of peak intervals
    :type cov_threshold: float
    :param frame_interval: frame interval in seconds of the recording
    :type frame_interval: float
    :return: returns the threshold, number of ROIs above the threshold for experimental data and random control data for std and cov respectively.
    :rtype: Tuple[float, int, int, float, int, int]
    """

    # experimental data
    exp_stds, exp_covs = calculate_std_cov(filtered_peak_series, frame_interval)
    num_exp_stds = np.sum(exp_stds < std_threshold)
    num_exp_covs = np.sum(exp_covs < cov_threshold)

    # random control data
    T, n = filtered_peak_series.shape
    idx = np.argsort(np.random.rand(T, n), axis=0)
    shuffled_peak_series = np.take_along_axis(filtered_peak_series, idx, axis=0)
    rand_stds, rand_covs = calculate_std_cov(shuffled_peak_series, frame_interval)
    num_rand_stds = np.sum(rand_stds < std_threshold)
    num_rand_covs = np.sum(rand_covs < cov_threshold)

    return std_threshold, num_exp_stds, num_rand_stds, cov_threshold, num_exp_covs, num_rand_covs

def find_oscillating_rois_from_peak_series(peak_series: np.ndarray, std_quantile: float, cov_quantile: float, frame_interval: float, n_iter: int = 100) -> Tuple[float, int, int, float, int, int]:
    """
    finds the oscillating ROIs based on the standard deviation and coefficient of variation thresholds.

    :param peak_series: T x n_roi binary array with 1s at the peak locations and 0s elsewhere
    :type peak_series: np.ndarray
    :param std_quantile: quantile for standard deviation threshold
    :type std_quantile: float
    :param cov_quantile: quantile for coefficient of variation threshold
    :type cov_quantile: float
    :param n_iter: number of iterations for random control
    :type n_iter: int
    :param frame_interval: frame interval in seconds of the recording
    :type frame_interval: float
    :return: returns the threshold, number of ROIs above the threshold for experimental data and random control data for std and cov respectively.
    :rtype: Tuple[float, int, int, float, int, int]
    """

    # filter the peak series to only include ROIs with at least 4 peaks
    filtered_peak_series = peak_series[:, np.sum(peak_series, axis=0) >= 4]

    # calculate the thresholds for standard deviation and coefficient of variation
    std_threshold, cov_threshold = calculate_std_cov_thresholds(filtered_peak_series, std_quantile, cov_quantile, frame_interval, n_iter)

    # find the oscillating ROIs based on the thresholds
    return find_oscillating_rois(filtered_peak_series, std_threshold, cov_threshold, frame_interval)