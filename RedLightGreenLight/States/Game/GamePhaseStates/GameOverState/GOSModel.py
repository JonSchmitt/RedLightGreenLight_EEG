

class GameOverModel:
    def __init__(self,game_over_duration:int):
        self._game_over = False
        self._game_over_start_time = 0.0
        self._game_over_duration = game_over_duration
        self._elapsed_time = 0.0

    def start_game_over(self):
        """ Call this on GameOverState Entry to init the game over start time """
        self._game_over = True
        self._game_over_start_time = 0.0

    def _update_time_in_game_over(self,dt:float):
        if self._game_over:
            self._elapsed_time += dt

    def is_game_over(self,dt:float)->bool:
        """Call this every frame to check if game is still over"""
        if self._game_over:
            self._update_time_in_game_over(dt)
            if self._elapsed_time >= self._game_over_duration:
                self.end_game_over()
                return False
            return True
        return False

    def end_game_over(self):
        self._elapsed_time = 0.0
        self._game_over = False

    def get_remaining_game_over_time(self):
        return self._game_over_duration - self._elapsed_time

    def get_maximum_game_over_duration(self):
        return self._game_over_duration

    def update_settings(self, game_over_duration:int):
        self._game_over_duration = game_over_duration