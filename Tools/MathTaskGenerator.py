import random
import time

class MathTaskGenerator:
    """
    Class responsible for generating mental arithmetic tasks and managing update intervals.
    Can be used for calibration and in-game mechanics.
    """
    def __init__(self, interval=5.0):
        self._interval = interval
        self._current_task = ""
        self._last_update_time = 0

    @property
    def current_task(self):
        return self._current_task

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    def update(self):
        """
        Checks if a new task should be generated based on the interval.
        Returns True if a new task was generated, False otherwise.
        """
        if self._current_task == "" or time.time() - self._last_update_time >= self._interval:
            self.generate_new_task()
            return True
        return False

    def generate_new_task(self):
        """
        Generates and returns a new random math task string.
        Ensures integer division for ':'.
        """
        ops = ['+', '-', '·', ':']
        op = random.choice(ops)
        
        if op == ':':
            # Ensure integer division: a = b * factor
            b = random.randint(1, 10)
            factor = random.randint(1, 10)
            a = b * factor
        else:
            # For +, -, ·
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            
        self._current_task = f"{a} {op} {b} = ?"
        self._last_update_time = time.time()
        return self._current_task

    def reset(self):
        """Resets the task state."""
        self._current_task = ""
        self._last_update_time = 0
