import pandas as pd
import numpy as np
import warnings
from pykrait.io.io import load_timelapse_lazy, get_files_from_folder
from pykrait.preprocessing.segmentation import create_cellpose_segmentation, timelapse_projection
from pykrait.preprocessing.timeseries_extraction import extract_mean_intensities, extract_cell_properties, get_adjacency_matrix
from pykrait.trace_analysis.filtering import detrend_with_sinc_filter
from pykrait.trace_analysis.peak_analysis import find_peaks
from pykrait.trace_analysis.oscillations import find_oscillating_rois_from_peak_series
from dataclasses import dataclass, asdict
from typing import Literal
import os
import tifffile


@dataclass
class AnalysisParameters:
    """This dataclass holds the modifiable parameters for calcium video analysis.

    :var tproj_type: Type of projection accross T-axis to be used for segmentation; 'std' computes standard deviation, 'sum' computes temporal sum, defaults to std.
    :vartype tproj_type: Literal['std', 'sum'], optional

    :var CLAHE_normalize: whether to apply CLAHE (Contrast Limited Adaptive Histogram Equalization) normalization to enhance image contrast.
    :vartype CLAHE_normalize: bool, optional

    :var cellpose_model_path: Path to the Cellpose model used for segmentation. Defaults to "cpsam" for the built-in CPSAM model.
    :vartype cellpose_model_path: str, optional

    :var frame_interval: time interval between consecutive video frames in seconds, defaults to None. If None provided, the frame interval obtained from the image metadata will be used or it will default to 1 second. The code will output a warning if a frame interval is provided which doesn't match with the metadata frame interval.
    :vartype frame_interval: float, optional

    :var neighbour_tolerance: Maximum distance in micrometers used to detect neighboring cells. Converted to pixels internally.
    :vartype neighbour_tolerance: float, optional

    :var sinc_filter_window: Window size for the sinc filter used to detrend the signal, specified in seconds. Converted to frame count internally.
    :vartype sinc_filter_window: float, optional

    :var peak_min_width: Minimum width at half-maximum of a detected peak in seconds. Converted to frames internally.
    :vartype peak_min_width: float, optional

    :var peak_max_width: Maximum width at half-maximum of a detected peak in seconds. Converted to frames internally.
    :vartype peak_max_width: float, optional

    :var peak_prominence: Minimum prominence of a detected peak, defined as the height difference between the peak and its surrounding baseline. Arbitrary units.
    :vartype peak_prominence: float, optional

    :var peak_min_height: Minimum height of a detected peak in arbitrary units.
    :vartype peak_min_height: float, optional

    :var std_quantile: Quantile used to threshold based on standard deviation for activity detection.
    :vartype std_quantile: float, optional

    :var cov_quantile: Quantile used to threshold based on the coefficient of variation for activity detection.
    :vartype cov_quantile: float, optional
    """
    tproj_type: Literal['std', 'sum'] = "std"
    CLAHE_normalize: bool = True
    cellpose_model_path: str = "cpsam"
    frame_interval: float = None
    neighbour_tolerance: float = 10
    sinc_filter_window: float = 300
    peak_min_width: float = 1
    peak_max_width: float = 40
    peak_prominence: float = 1000
    peak_min_height: float = 80
    std_quantile: float = 0.01
    cov_quantile: float = 0.01
    

    def to_pandas(self) -> pd.DataFrame:
        """Convert the dataclass to a pandas DataFrame."""
        return pd.DataFrame([asdict(self)])

@dataclass
class AnalysisOutput:
    """
    This dataclass holds the output variables of the pipeline.
    :var filepath: Path to the calcium imaging video file.
    :vartype filepath: str
    :var filename: name of the video file
    :vartype filename: str
    :var frame_interval: time interval between frames in seconds
    :vartype frame_interval: float
    :var pixel_interval_y: pixel size in y direction in micrometers
    :vartype pixel_interval_y: float
    :var pixel_interval_x: pixel size in x direction in micrometers
    :vartype pixel_interval_x: float
    :var number_of_cells: number of cells detected in the video
    :vartype number_of_cells: int
    :var number_of_frames: number of frames in the video
    :vartype number_of_frames: int
    :var normalized_peaks: number of peaks per 100 cells and 10 minutes of recording
    :vartype normalized_peaks: float
    :var cells_four_peaks: number of cells with at least 4 peaks detected
    :vartype cells_four_peaks: int
    :var std_threshold: calculated threshold for the standard deviation in seconds
    :vartype std_threshold: float
    :var random_below_std: number of cells with a standard deviation below the threshold in the random control
    :vartype random_below_std: int
    :var experiment_below_std: number of cells with a standard deviation below the threshold in the recording
    :vartype experiment_below_std: int
    :var cov_threshold: calculated threshold for the coefficient of variation
    :vartype cov_threshold: float
    :var random_below_cov: number of cells with a coefficient of variation below the threshold in the random control
    :vartype random_below_cov: int
    :var experiment_below_cov: number of cells with a coefficient of variation below the threshold in the recording
    :vartype experiment_below_cov: int
    :var random_1st_neighbour_zscore: z-score of synchronicity of the first neighbours in the random control
    :vartype random_1st_neighbour_zscore: float
    :var random_2nd_neighbour_zscore: z-score of synchronicity of the second neighbours in the random control
    :vartype random_2nd_neighbour_zscore: float
    :var random_3rd_neighbour_zscore: z-score of synchronicity of the third neighbours in the random control
    :vartype random_3rd_neighbour_zscore: float
    :var experiment_1st_neighbour_zscore: z-score of synchronicity of the first neighbours in the recording
    :vartype experiment_1st_neighbour_zscore: float
    :var experiment_2nd_neighbour_zscore: z-score of synchronicity of the second neighbours in the recording
    :vartype experiment_2nd_neighbour_zscore: float
    :var experiment_3rd_neighbour_zscore: z-score of synchronicity of the third neighbours in the recording
    :vartype experiment_3rd_neighbour_zscore: float
    :var pykrait_version: version of the pykrait package used for the analysis
    :vartype pykrait_version: str
    :var timestamp: timestamp of the analysis
    :vartype timestamp: np.datetime64
    """
    filepath: str = None
    filename: str = None
    frame_interval: float = None
    pixel_interval_y: float = None
    pixel_interval_x: float = None
    number_of_cells: int = None
    number_of_frames: int = None
    normalized_peaks: float = None
    cells_four_peaks: int = None
    std_threshold: float = None
    random_below_std: int = None
    experiment_below_std: int = None
    cov_threshold: float = None
    random_below_cov: int = None
    experiment_below_cov: int = None
    random_1st_neighbour_zscore: float = None
    random_2nd_neighbour_zscore: float = None
    random_3rd_neighbour_zscore: float = None
    experiment_1st_neighbour_zscore: float = None
    experiment_2nd_neighbour_zscore: float = None
    experiment_3rd_neighbour_zscore: float = None
    pykrait_version: str = None
    timestamp: np.datetime64 = None

    def to_pandas(self):
        """Convert the dataclass to a pandas DataFrame."""
        return pd.DataFrame([asdict(self)])
    

class CalciumVideo():
    """
    _summary_
    """
    def __init__(self, video_path:str, params: AnalysisParameters):
        """
        _summary_

        :param video_path: path to the calcium video
        :type video_path: str
        :param cellpose_model_path: path to the cellpose model, defaults to "cpsam" to use the built-in cellpose model
        :type cellpose_model_path: str, optional
        """
        self.analysis_parameters = params
        self.analysis_output = AnalysisOutput(filepath=video_path)
    
    def run(self) -> AnalysisOutput:
        """
        runs the pipeline according to
        """
        self.analysis_output.filename = self.analysis_output.filepath.split("/")[-1]
        print(f"Running analysis on {self.analysis_output.filename}")
        # Create analysis folder in the parent directory of the video file
        parent_dir = os.path.dirname(self.analysis_output.filepath)
        filename_wo_ext = os.path.splitext(self.analysis_output.filename)[0]
        analysis_folder = os.path.join(parent_dir, f"Analysis_{filename_wo_ext}")
        os.makedirs(analysis_folder, exist_ok=True)

        # load image data lazily
        self.timelapse_data, frame_interval, self.analysis_output.pixel_interval_y, self.analysis_output.pixel_interval_x = load_timelapse_lazy(file_path = self.analysis_output.filepath)

        if frame_interval is None and self.analysis_parameters.frame_interval is None:
            warnings.warn("No frame interval provided in the analysis parameters, and no frame interval could be inferred from the metadata. Defaulting to 1 second.")
            self.analysis_output.frame_interval = 1  # Default to 1 second if not provided
        elif self.analysis_parameters.frame_interval is None and frame_interval is not None:
            self.analysis_output.frame_interval = frame_interval
        elif frame_interval is not None and self.analysis_parameters.frame_interval != frame_interval:
            warnings.warn(f"Provided frame_interval ({self.analysis_parameters.frame_interval}) does not match inferred frame_interval ({frame_interval}) from metadata. Using provided value.")

        # perform the zproj
        self.zproj = timelapse_projection(self.timelapse_data, method=self.analysis_parameters.tproj_type, normalize=self.analysis_parameters.CLAHE_normalize, verbose=True)
        tifffile.imwrite(os.path.join(analysis_folder, f"{filename_wo_ext}_zproj.ome.tif"), self.zproj.astype(np.uint16), metadata={'axes': 'CYX'}, compression="zlib")

        # create cellpose segmentation    
        self.masks = create_cellpose_segmentation(self.zproj, cellpose_model_path=self.analysis_parameters.cellpose_model_path)
        tifffile.imwrite(os.path.join(analysis_folder, f"{filename_wo_ext}_cp_masks.ome.tif"), self.masks.astype(np.uint16), metadata={'axes': 'YX'}, compression="zlib")

        # extracts the mean intensities of the masks
        self.mean_intensities = extract_mean_intensities(self.timelapse_data, self.masks)
        self.analysis_output.number_of_frames, self.analysis_output.number_of_cells = self.mean_intensities.shape
        
        self.cell_properties = extract_cell_properties(self.masks)

        # convert seconds and µm to frames and pixels
        neighbour_tolerance_pixels = int(self.analysis_parameters.neighbour_tolerance / self.analysis_output.pixel_interval_x)  # convert micrometers to pixels
        peak_min_width_frames = int(self.analysis_parameters.peak_min_width / self.analysis_output.frame_interval)  # convert seconds to frames
        peak_max_width_frames = int(self.analysis_parameters.peak_max_width / self.analysis_output.frame_interval) # convert seconds to frames

        # checking if the parameters are valid
        if neighbour_tolerance_pixels < 1:
            warnings.warn(f"Neighbour tolerance of {neighbour_tolerance_pixels} pixels is too small, setting to 1 pixel.")
            neighbour_tolerance_pixels = 1
        if peak_min_width_frames < 1:
            warnings.warn(f"Peak minimum width of {peak_min_width_frames} frames is too small, setting to 1 frame.")
            peak_min_width_frames = 1
        if peak_max_width_frames <= peak_min_width_frames:
            warnings.warn(f"Peak maximum width of {peak_max_width_frames} frames is smaller or equal than peak minimum width of {peak_min_width_frames} seconds, setting to peak minimum width + 1.")
            peak_max_width_frames = peak_min_width_frames + 1
        
        self.adjacency_matrix = get_adjacency_matrix(self.masks, neighbour_tolerance=neighbour_tolerance_pixels)

        self.detrended_timeseries = detrend_with_sinc_filter(signals=self.mean_intensities, 
                                                             cutoff_period=self.analysis_parameters.sinc_filter_window,
                                                             sampling_interval=self.analysis_output.frame_interval)
        
        self.peak_series = find_peaks(peak_min_width=peak_min_width_frames,
                                      peak_max_width=peak_max_width_frames,
                                      peak_prominence=self.analysis_parameters.peak_prominence,
                                      peak_min_height=self.analysis_parameters.peak_min_height,
                                      detrended_timeseries=self.detrended_timeseries)
        
        peaks_per_100c_per_10_min = (np.sum(self.peak_series) / (self.analysis_output.number_of_cells / 100)) / ((self.analysis_output.number_of_frames * self.analysis_output.frame_interval) / 600) # normalize to 100 cells and 10 minutes of recording
        self.analysis_output.normalized_peaks = round(peaks_per_100c_per_10_min, 2)

        self.analysis_output.cells_four_peaks = np.sum(np.sum(self.peak_series, axis=0) >= 4)
        
        self.analysis_output.std_threshold, self.analysis_output.experiment_below_std, self.analysis_output.random_below_std, self.analysis_output.cov_threshold, self.analysis_output.experiment_below_cov, self.analysis_output.random_below_cov = find_oscillating_rois_from_peak_series(self.peak_series, 
                                                                                                                                                                                                                                                                                            self.analysis_parameters.std_quantile, 
                                                                                                                                                                                                                                                                                            self.analysis_parameters.cov_quantile,
                                                                                                                                                                                                                                                                                            self.analysis_output.frame_interval,
                                                                                                                                                                                                                                                                                            n_iter=100)
        # saving the parameters and output to the analysis folder
        self.analysis_output.to_pandas().to_csv(os.path.join(analysis_folder, f"{filename_wo_ext}_analysis_output.csv"), index=False)
        self.analysis_parameters.to_pandas().to_csv(os.path.join(analysis_folder, f"{filename_wo_ext}_analysis_parameters.csv"), index=False)
        return self.analysis_output


class BatchExperiment:
    def __init__(self, folder: str, params: AnalysisParameters, extension:str = ".czi"):
        files = get_files_from_folder(folder, extension=extension)
        self.experiments = [CalciumVideo(video_path=video_path, params=params) for video_path in files]
        self.results = pd.DataFrame()

    def run(self):

        for experiment in self.experiments:
            result = experiment.run().to_pandas()
            self.results = pd.concat([self.results, result], ignore_index=True)


        
        
        
