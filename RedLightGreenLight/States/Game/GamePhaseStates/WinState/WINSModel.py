class WINSModel:
    """
    Model for the Win state.
    Tracks elapsed time and winner name.
    """
    def __init__(self, win_duration: float = 5.0):
        self._win_duration = win_duration
        self._time_passed = 0
        self._winner_name = ""

    def update_time(self, delta_time: float):
        self._time_passed += delta_time

    def is_time_up(self) -> bool:
        return self._time_passed >= self._win_duration

    def reset(self):
        self._time_passed = 0

    @property
    def winner_name(self):
        return self._winner_name

    @winner_name.setter
    def winner_name(self, name: str):
        self._winner_name = name
