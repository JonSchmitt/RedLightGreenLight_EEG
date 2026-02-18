import time
import numpy as np
from .CalibrationPhase import CalibrationPhase
from Tools.MathTaskGenerator import MathTaskGenerator
from EEG.SignalProcessor import SignalProcessor


class CalibrationModel:
    """
    Model for the calibration process. Manages timestamps, data buffers, 
    and calculation results.
    Refactored to use a SINGLE METRIC: Ratio = Frontal Beta / Occipital Alpha.
    """
    def __init__(self):
        self._phase = CalibrationPhase.EXPLANATION
        self._start_time = 0
        self._phase_duration = 30.0  # seconds
        self._sensitivity = 0.7 # Weighted threshold: 0.5 = middle, >0.5 = harder to trigger (closer to concentration)
        
        # Data storage
        self._relaxed_data = []
        self._concentrated_data = []
        
        # Result (Single Ratio Threshold)
        # Ratio = Beta(Front) / Alpha(Back)
        self._threshold_ratio = 1.0
        self._margin_ratio = 0.1
        
        # Math tasks (Centralized Logic)
        self._math_generator = MathTaskGenerator(interval=5.0)

    @property
    def threshold_ratio(self): return self._threshold_ratio
    
    @property
    def margin_ratio(self): return self._margin_ratio

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value

    @property
    def current_math_task(self):
        return self._math_generator.current_task

    def start_phase(self, phase):
        self._phase = phase
        self._start_time = time.time()
        if phase == CalibrationPhase.CONCENTRATED:
            self._math_generator.reset()
            self._math_generator.update()

    def get_remaining_time(self):
        if self._phase in [CalibrationPhase.RELAXED, CalibrationPhase.CONCENTRATED]:
            elapsed = time.time() - self._start_time
            return max(0, self._phase_duration - elapsed)
        return 0

    def is_phase_over(self):
        return self.get_remaining_time() <= 0

    def check_math_task_update(self):
        """
        Logic to decide if a new math task is needed.
        Delegates to the centralized MathTaskGenerator.
        """
        if self._phase == CalibrationPhase.CONCENTRATED:
            self._math_generator.update()

    def add_data(self, data):
        if self._phase == CalibrationPhase.RELAXED:
            self._relaxed_data.extend(data)
        elif self._phase == CalibrationPhase.CONCENTRATED:
            self._concentrated_data.extend(data)

    @property
    def concentrated_data(self):
        return self._concentrated_data

    def calculate_calibration_results(self, signal_processor: SignalProcessor):
        """
        Calculates the single threshold based on the Ratio:
        Ratio = Beta(Ch1 - Frontal) / Alpha(Ch8 - Occipital)
        
        Args:
            signal_processor (SignalProcessor): The processor used for spectral analysis.
        """
        if not self._relaxed_data or not self._concentrated_data:
            print("Warning: Missing calibration data for calculation.")
            return

        self._relaxed_data = self._relaxed_data[1250:-1250]
        self._concentrated_data = self._concentrated_data[1250:-1250]

        # Helper to calculate average Ratio for a dataset
        def get_average_ratio(data_chunk):
            # Calculate Band Powers for all channels
            alpha_powers = np.array(signal_processor.calculate_band_power(data_chunk, signal_processor.alpha_band))
            beta_powers = np.array(signal_processor.calculate_band_power(data_chunk, signal_processor.beta_band))
            
            # Ch1 (Frontal) is index 0 -> Use Beta
            beta_front = beta_powers[0]
            
            # Ch8 (Occipital) is index 7 -> Use Alpha
            alpha_back = alpha_powers[7]
            
            # Avoid division by zero
            if alpha_back == 0: alpha_back = 0.0001
            
            return beta_front / alpha_back

        # Calculate average ratios for both phases
        avg_ratio_relaxed = get_average_ratio(self._relaxed_data)
        avg_ratio_concentrated = get_average_ratio(self._concentrated_data)
        
        print(f"DEBUG: Avg Ratio Relaxed: {avg_ratio_relaxed:.4f}")
        print(f"DEBUG: Avg Ratio Concentrated: {avg_ratio_concentrated:.4f}")

        # Calculate Threshold
        # We expect Concentrated Ratio > Relaxed Ratio.
        # Threshold is weighted average.
        self._threshold_ratio = avg_ratio_relaxed + self._sensitivity * (avg_ratio_concentrated - avg_ratio_relaxed)
        
        # Margin is 20% of the distance
        self._margin_ratio = abs(avg_ratio_concentrated - avg_ratio_relaxed) * 0.2
        
        print(f"Calibration Results calculated in Model:")
        print(f"  Ratio (Beta_Ch1 / Alpha_Ch8) -> Th: {self._threshold_ratio:.4f}, Margin: {self._margin_ratio:.4f}")
