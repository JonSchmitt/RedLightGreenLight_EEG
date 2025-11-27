from __future__ import annotations


class GameModel:
    """Model for the game."""
    def __init__(self, switch_time: int, warning_time: int):
        # Game Phases
        self._gamephase1 = "GreenLight"
        self._gamephase2 = "RedLight"
        self._current_gamephase = self._gamephase1
        self._is_paused = False

        # Time
        self._time_passed = 0
        self._switch_time = switch_time
        self._warning_time = warning_time

        # Player
        self._START_POS = (100,450)
        self._player_pos = self._START_POS
        self._player_moving = False

    def get_current_gamephase(self):
        return self._current_gamephase

    def set_current_gamephase(self, gamephase):
        self._current_gamephase = gamephase

    def switch_gamephase(self):
        if self._current_gamephase == self._gamephase1:
            self._current_gamephase = self._gamephase2
        else:
            self._current_gamephase = self._gamephase1

    def is_red_light(self):
        return self._current_gamephase == self._gamephase2

    def is_green_light(self):
        return self._current_gamephase == self._gamephase1

    def is_pause(self):
        return self._is_paused

    def set_pause(self,pause:bool):
        self._is_paused = pause

    def is_player_moving(self):
        return self._player_moving

    def set_player_moving(self, moving:bool):
        self._player_moving = moving


    def update_settings(self, switch_time: int, warning_time: int):
        self._switch_time = switch_time
        self._warning_time = warning_time

    def update_time(self, delta_time: float):
        if not self._is_paused:
            self._time_passed += delta_time
            if self._time_passed >= self._switch_time:
                self.switch_gamephase()
                self._time_passed = 0

    def get_remaining_warning_time(self):
        if self._current_gamephase == self._gamephase1 and self._switch_time - self._time_passed <= self._warning_time:
            return self._switch_time - self._time_passed
        else:
            return None

    def get_remaining_in_phase_time(self):
        return self._switch_time - self._time_passed


    def move_player(self, dx:float, dy:float):
        self._player_pos = (self._player_pos[0] + dx, self._player_pos[1] + dy)
        print(self._player_pos)


    def reset_player_position(self):
        self._player_pos = self._START_POS

    def get_player_position(self):
        return self._player_pos

    def restart_game(self):
        self._time_passed = 0
        self._current_gamephase = self._gamephase1
        self.reset_player_position()
