import numpy as np
from scipy.signal import butter, lfilter, welch

class SignalProcessor:
    """
    Handles EEG signal processing: filtering and frequency spectrum analysis.
    """
    def __init__(self, sampling_rate=250):
        self._sampling_rate = sampling_rate
        self._alpha_band = (8, 13)
        self._beta_band = (14, 30)

    @property
    def sampling_rate(self):
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, value):
        self._sampling_rate = value

    def _butter_bandpass(self, lowcut, highcut, order=5):
        nyq = 0.5 * self._sampling_rate
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data, lowcut, highcut, order=5):
        b, a = self._butter_bandpass(lowcut, highcut, order=order)
        y = lfilter(b, a, data, axis=0)
        return y

    def calculate_band_power(self, data, band):
        """
        Calculates the average power in a specific frequency band using Welch's method.
        'data' should be a 1D array or 2D array (samples, channels).
        """
        if len(data) == 0:
            return 0.0
            
        powers = []
        data_np = np.array(data)
        
        # Assume data is (samples, channels)
        for ch in range(data_np.shape[1]):
            freqs, psd = welch(data_np[:, ch], self._sampling_rate, nperseg=min(len(data_np), 256))
            idx_band = np.logical_and(freqs >= band[0], freqs <= band[1])
            # Use np.trapezoid for NumPy 2.0+ compatibility
            if hasattr(np, 'trapezoid'):
                band_power = np.trapezoid(psd[idx_band], freqs[idx_band])
            else:
                band_power = np.trapz(psd[idx_band], freqs[idx_band])
            powers.append(band_power)
            
        return np.mean(powers)

    def process_calibration_data(self, relaxed_data, concentrated_data):
        """
        Processes two datasets and returns the Alpha and Beta ratios.
        Ratio = Concentrated_Power / Relaxed_Power
        """
        if len(relaxed_data) == 0 or len(concentrated_data) == 0:
            return 1.0, 1.0

        # Alpha Power
        alpha_relaxed = self.calculate_band_power(relaxed_data, self._alpha_band)
        alpha_concentrated = self.calculate_band_power(concentrated_data, self._alpha_band)
        
        # Beta Power
        beta_relaxed = self.calculate_band_power(relaxed_data, self._beta_band)
        beta_concentrated = self.calculate_band_power(concentrated_data, self._beta_band)
        
        # Calculate ratios (with safety for division by zero)
        alpha_ratio = alpha_concentrated / alpha_relaxed if alpha_relaxed > 0 else 1.0
        beta_ratio = beta_concentrated / beta_relaxed if beta_relaxed > 0 else 1.0
        
        return alpha_ratio, beta_ratio
