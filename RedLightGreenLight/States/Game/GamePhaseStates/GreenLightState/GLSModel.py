from Tools.MathTaskGenerator import MathTaskGenerator

class GLSModel:
    """
    Model for Green Light Phase.
    Tracks time passed, math tasks, and switches phases.
    Centralized math task logic via MathTaskGenerator.
    """
    def __init__(self, switch_time: int, warn_time: int):
        self._switch_time = switch_time
        self._warn_time = warn_time
        self._time_passed = 0
        
        # Math tasks (Centralized Logic)
        self._math_generator = MathTaskGenerator(interval=5.0)

    def update_settings(self, switch_time: int, warn_time: int):
        self._switch_time = switch_time
        self._warn_time = warn_time

    def update_time_in_phase(self, delta_time: float):
        self._time_passed += delta_time

    def reset_time_in_phase(self):
        self._time_passed = 0
        self._math_generator.reset()

    def get_remaining_warning_time(self):
        remaining_time = self._switch_time - self._time_passed
        if remaining_time < self._warn_time:
            return remaining_time
        return 0

    def get_remaining_time_in_phase(self):
        return self._switch_time - self._time_passed

    def switch_phase(self) -> bool:
        return self._time_passed >= self._switch_time

    @property
    def current_math_task(self):
        return self._math_generator.current_task

    def check_math_task_update(self):
        """
        Decides if a new math task is needed using the centralized generator.
        """
        self._math_generator.update()