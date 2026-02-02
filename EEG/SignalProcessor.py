import numpy as np
from scipy.signal import butter, lfilter, welch

class SignalProcessor:
    """
    Handles EEG signal processing: filtering and frequency spectrum analysis.
    """
    def __init__(self, sampling_rate=250):
        self._sampling_rate = sampling_rate
        # Bands as specified by user
        self._alpha_band = (8, 12)
        self._beta_band = (12, 30)

    def _butter_bandpass(self, lowcut, highcut, order=5):
        nyq = 0.5 * self._sampling_rate
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def _calculate_band_power_filtering(self, data, band):
        """
        Calculates the power in a specific band using Butterworth filtering.
        1. Centers data (removes DC).
        2. Applies bandpass filter.
        3. Returns variance (power) per channel. (Naturally length-normalized).
        """
        if len(data) == 0:
            return []

        data_np = np.array(data)
        # Center data to remove massive DC offset
        data_centered = data_np - np.mean(data_np, axis=0)
        
        # Create filter
        b, a = self._butter_bandpass(band[0], band[1])
        
        # Apply filter along time axis (axis 0)
        filtered_data = lfilter(b, a, data_centered, axis=0)
        
        # Calculate power as variance (Mean Square of the AC signal)
        powers = np.var(filtered_data, axis=0)
        
        return powers.tolist()

    def process_calibration_data(self, relaxed_data, concentrated_data):
        """
        Processes two datasets and returns the Alpha and Beta ratios per channel.
        Ratio = Concentrated_Power / Relaxed_Power
        Returns (alpha_ratios_list, beta_ratios_list)
        """
        if len(relaxed_data) == 0 or len(concentrated_data) == 0:
            return [], []

        # Alpha Powers (8-12 Hz)
        alpha_rel = self._calculate_band_power_filtering(relaxed_data, self._alpha_band)
        alpha_con = self._calculate_band_power_filtering(concentrated_data, self._alpha_band)
        
        # Beta Powers (12-30 Hz)
        beta_rel = self._calculate_band_power_filtering(relaxed_data, self._beta_band)
        beta_con = self._calculate_band_power_filtering(concentrated_data, self._beta_band)
        
        # Calculate per-channel ratios
        arr_a_rel = np.array(alpha_rel)
        arr_a_con = np.array(alpha_con)
        arr_b_rel = np.array(beta_rel)
        arr_b_con = np.array(beta_con)
        
        alpha_ratios = np.where(arr_a_rel > 0, arr_a_con / arr_a_rel, 1.0)
        beta_ratios = np.where(arr_b_rel > 0, arr_b_con / arr_b_rel, 1.0)
        
        return alpha_ratios.tolist(), beta_ratios.tolist()
