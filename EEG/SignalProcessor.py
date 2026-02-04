import numpy as np
from scipy.signal import butter, lfilter, filtfilt

class SignalProcessor:
    """
    Handles EEG signal processing: filtering and frequency spectrum analysis.
    Uses spectral power (FFT magnitude summation) matching the user's MATLAB logic.
    """

    def __init__(self, sampling_rate=250):
        self._sampling_rate = sampling_rate
        # Bands as specified by user
        self._alpha_band = (8, 12)
        self._beta_band = (13, 30) # Using 13-30 as per MATLAB bounds

    @property
    def alpha_band(self): return self._alpha_band

    @property
    def beta_band(self): return self._beta_band

    @property
    def sampling_rate(self): return self._sampling_rate

    def calculate_band_power(self, data, band):
        """
        Calculates power in a band using Butterworth filtering and FFT magnitude summation.
        Matches MATLAB: sum(abs(fft(filtered_signal(band))))

        Args:
            data (list or np.ndarray): The raw EEG data (samples x channels).
            band (tuple): The frequency band (low, high) in Hz.

        Returns:
            float or list: The spectral power for each channel.
        """

        data_np = np.array(data)
        
        # Subtract mean (DC offset) to minimize filter transients
        data_np = data_np - np.mean(data_np, axis=0)
        
        # Create filter
        b, a = self._create_butter_bandpass(3, band[0], band[1])
        
        # Apply filter (causal lfilter for consistency between calibration and real-time)
        filtered_data = lfilter(b, a, data_np, axis=0)
        
        # Calculate spectral magnitude Mean (to be window-length independent)
        N = len(filtered_data)
        freqs = np.fft.rfftfreq(N, 1/self._sampling_rate)
        fft_mags = np.abs(np.fft.rfft(filtered_data, axis=0)) / N # Normalize by N
        
        # Mask for the relevant frequency bins
        mask = (freqs >= band[0]) & (freqs <= band[1])
        
        # Mean magnitude across the band
        spectral_means = np.mean(fft_mags[mask, :], axis=0)
        
        if np.isscalar(spectral_means):
            return float(spectral_means)
        
        return spectral_means.tolist()

    def calculate_ratios(self, data):
        """
        Calculates the Beta/Alpha ratio for all channels using causal filtering.

        Args:
            data (list or np.ndarray): Raw EEG data.

        Returns:
            np.ndarray: Array of ratios (Beta/Alpha) for each channel.
        """
        alpha_power = np.array(self.calculate_band_power(data, self._alpha_band))
        beta_power = np.array(self.calculate_band_power(data, self._beta_band))
        
        # Avoid division by zero
        ratios = np.where(alpha_power > 0, beta_power / alpha_power, 1.0)
        return ratios

    def _create_butter_bandpass(self,order,F_low,F_high):
        nyq = 0.5 * self._sampling_rate
        low = F_low / nyq
        high = F_high / nyq
        b, a = butter(order, [low, high], btype='band')
        return b,a
