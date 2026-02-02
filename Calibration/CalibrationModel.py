import time
from .CalibrationPhase import CalibrationPhase
from Tools.MathTaskGenerator import MathTaskGenerator

class CalibrationModel:
    """
    Model for the calibration process. Manages timestamps, data buffers, 
    and calculation results.
    """
    def __init__(self):
        self._phase = CalibrationPhase.EXPLANATION
        self._start_time = 0
        self._phase_duration = 5.0  # seconds
        
        # Data storage
        self._relaxed_data = []
        self._concentrated_data = []
        
        # Results
        self._alpha_ratio = 1.0
        self._beta_ratio = 1.0
        
        # Math tasks
        self._math_generator = MathTaskGenerator()
        self._current_math_task = ""
        self._last_math_task_time = 0
        self._math_task_interval = 5.0

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value

    @property
    def alpha_ratio(self):
        return self._alpha_ratio

    @alpha_ratio.setter
    def alpha_ratio(self, value):
        self._alpha_ratio = value

    @property
    def beta_ratio(self):
        return self._beta_ratio

    @beta_ratio.setter
    def beta_ratio(self, value):
        self._beta_ratio = value

    @property
    def current_math_task(self):
        return self._current_math_task

    def start_phase(self, phase):
        self._phase = phase
        self._start_time = time.time()
        if phase == CalibrationPhase.CONCENTRATED:
            self._generate_new_math_task()

    def get_remaining_time(self):
        if self._phase in [CalibrationPhase.RELAXED, CalibrationPhase.CONCENTRATED]:
            elapsed = time.time() - self._start_time
            return max(0, self._phase_duration - elapsed)
        return 0

    def is_phase_over(self):
        return self.get_remaining_time() <= 0

    def check_math_task_update(self):
        """
        Logic to decide if a new math task is needed based on the timer.
        Called by the Controller.
        """
        if self._phase == CalibrationPhase.CONCENTRATED:
            if time.time() - self._last_math_task_time >= self._math_task_interval:
                self._generate_new_math_task()

    def _generate_new_math_task(self):
        self._current_math_task = self._math_generator.generate_task()
        self._last_math_task_time = time.time()

    def add_data(self, data):
        if self._phase == CalibrationPhase.RELAXED:
            self._relaxed_data.extend(data)
        elif self._phase == CalibrationPhase.CONCENTRATED:
            self._concentrated_data.extend(data)

    @property
    def relaxed_data(self):
        return self._relaxed_data

    @property
    def concentrated_data(self):
        return self._concentrated_data
