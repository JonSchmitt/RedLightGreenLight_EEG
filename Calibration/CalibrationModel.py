import time
import numpy as np
from .CalibrationPhase import CalibrationPhase
from Tools.MathTaskGenerator import MathTaskGenerator
from EEG.SignalProcessor import SignalProcessor


class CalibrationModel:
    """
    Model for the calibration process. Manages timestamps, data buffers, 
    and calculation results.
    """
    def __init__(self):
        self._phase = CalibrationPhase.EXPLANATION
        self._start_time = 0
        self._phase_duration = 30.0  # seconds
        
        # Data storage
        self._relaxed_data = []
        self._concentrated_data = []
        
        # Results (Independent thresholds for Ch 1 and Ch 8)
        self._threshold_1 = 1.0
        self._dir_1 = 1 # 1: Concentration > Relaxed, -1: Concentration < Relaxed
        self._threshold_8 = 1.0
        self._dir_8 = 1
        self._margin_1 = 0.01
        self._margin_8 = 0.01
        
        # Math tasks (Centralized Logic)
        self._math_generator = MathTaskGenerator(interval=5.0)

    @property
    def threshold_1(self): return self._threshold_1
    @threshold_1.setter
    def threshold_1(self, v): self._threshold_1 = v

    @property
    def dir_1(self): return self._dir_1
    @dir_1.setter
    def dir_1(self, v): self._dir_1 = v

    @property
    def threshold_8(self): return self._threshold_8
    @threshold_8.setter
    def threshold_8(self, v): self._threshold_8 = v

    @property
    def dir_8(self): return self._dir_8
    @dir_8.setter
    def dir_8(self, v): self._dir_8 = v

    @property
    def margin_1(self): return self._margin_1
    @margin_1.setter
    def margin_1(self, v): self._margin_1 = v

    @property
    def margin_8(self): return self._margin_8
    @margin_8.setter
    def margin_8(self, v): self._margin_8 = v

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value

    @property
    def concentration_threshold(self):
        return self._concentration_threshold

    @concentration_threshold.setter
    def concentration_threshold(self, value):
        self._concentration_threshold = value

    @property
    def concentration_margin(self):
        return self._concentration_margin

    @concentration_margin.setter
    def concentration_margin(self, value):
        self._concentration_margin = value

    @property
    def current_math_task(self):
        return self._math_generator.current_task

    def start_phase(self, phase):
        self._phase = phase
        self._start_time = time.time()
        if phase == CalibrationPhase.CONCENTRATED:
            self._math_generator.reset()
            self._math_generator.update()

    @property
    def is_concentration_greater(self):
        return self._is_concentration_greater

    @is_concentration_greater.setter
    def is_concentration_greater(self, value):
        self._is_concentration_greater = value

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
        Calculates thresholds, directions, and margins based on collected calibration data.
        
        Args:
            signal_processor (SignalProcessor): The processor used for spectral analysis.
        """
        if not self._relaxed_data or not self._concentrated_data:
            print("Warning: Missing calibration data for calculation.")
            return

        # Calculate Beta/Alpha ratios for both phases for all channels
        ratios_rel = signal_processor.calculate_ratios(self._relaxed_data)
        ratios_con = signal_processor.calculate_ratios(self._concentrated_data)
        
        # Channel 1: Frontal (index 0)
        avg_rel_1 = float(ratios_rel[0])
        avg_con_1 = float(ratios_con[0])
        self._threshold_1 = (avg_rel_1 + avg_con_1) / 2.0
        self._dir_1 = 1 if avg_con_1 > avg_rel_1 else -1
        self._margin_1 = abs(avg_con_1 - avg_rel_1) * 0.1

        # Channel 8: Occipital (index 7)
        avg_rel_8 = float(ratios_rel[7])
        avg_con_8 = float(ratios_con[7])
        self._threshold_8 = (avg_rel_8 + avg_con_8) / 2.0
        self._dir_8 = 1 if avg_con_8 > avg_rel_8 else -1
        self._margin_8 = abs(avg_con_8 - avg_rel_8) * 0.1
        
        print(f"Calibration Results calculated in Model:")
        print(f"  Ch 1 (Frontal) -> Th: {self._threshold_1:.4f}, Dir: {self._dir_1}, Margin: {self._margin_1:.4f}")
        print(f"  Ch 8 (Occipital) -> Th: {self._threshold_8:.4f}, Dir: {self._dir_8}, Margin: {self._margin_8:.4f}")

