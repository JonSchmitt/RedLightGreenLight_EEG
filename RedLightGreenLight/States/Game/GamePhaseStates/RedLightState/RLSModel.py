class RLSModel:
    def __init__(self, switch_time:int):
        self._switch_time = switch_time
        self._time_passed = 0


    def update_settings(self, switch_time: int):
        self._switch_time = switch_time

    def update_time_in_phase(self, delta_time: float):
            self._time_passed += delta_time

    def reset_time_in_phase(self):
        self._time_passed = 0

    def get_remaining_time_in_phase(self):
        return self._switch_time - self._time_passed

    def switch_phase(self)-> bool:
        if self._time_passed >= self._switch_time:
            return True
        return False