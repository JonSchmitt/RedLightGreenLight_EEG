from __future__ import annotations

from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver


class SettingsModel:
    """
    Model for global settings (used like a Singleton but instantiated).
    Implements the Subject in the Observer pattern to report changes to settings
    to registered observers (States).
    """
    def __init__(self):
        self._settings_observers = []

        # Default settings
        self._fullscreen = False
        self._window_width = 1900
        self._window_height = 1000
        self._music = True
        self._warning_time = 10
        self._switch_time = 10
        self._ui_scaling = 1.5
        self._game_over_duration = 5
        self._second_player = False
        self._music_fade_out_time = 1.5
        self._music_fade_in_time = 2.0

    def add_observer(self, observer:SettingsObserver):
        if isinstance(observer, SettingsObserver):
            if observer not in self._settings_observers:
                self._settings_observers.append(observer)
                # print(f"Observer added: {observer}")

    def remove_observer(self, observer):
        self._settings_observers.remove(observer)

    def notify_observers(self):
        for observer in self._settings_observers:
            observer.update_settings()

    def is_fullscreen(self):
        return self._fullscreen

    def set_fullscreen(self, fullscreen:bool):
        self._fullscreen = fullscreen
        self.notify_observers()

    def get_window_width(self):
        return self._window_width

    def set_window_width(self, screen_width:int):
        self._window_width = screen_width
        self.notify_observers()

    def get_window_height(self):
        return self._window_height

    def set_window_height(self, screen_height:int):
        self._window_height = screen_height
        self.notify_observers()

    def is_music(self):
        return self._music

    def set_music(self, sound:bool):
        self._music = sound
        self.notify_observers()

    def get_warning_time(self):
        return self._warning_time

    def set_warning_time(self, warning_time:int):
        self._warning_time = warning_time
        self.notify_observers()

    def get_switch_time(self):
        return self._switch_time

    def set_switch_time(self, switch_time:int):
        self._switch_time = switch_time
        self.notify_observers()


    def get_ui_scaling(self):
        return self._ui_scaling

    def set_ui_scaling(self, ui_scaling:int):
        self._ui_scaling = ui_scaling
        self.notify_observers()

    def get_game_over_duration(self):
        return self._game_over_duration

    def set_game_over_duration(self, game_over_duration:float):
        self._game_over_duration = game_over_duration
        self.notify_observers()

    def is_second_player(self):
        return self._second_player

    def set_second_player(self, second_player:bool):
        self._second_player = second_player
        self.notify_observers()

    def get_music_fade_out_time(self):
        return self._music_fade_out_time

    def set_music_fade_out_time(self, music_fade_out_time: float):
        self._music_fade_out_time = music_fade_out_time
        self.notify_observers()

    def get_music_fade_in_time(self):
        return self._music_fade_in_time

    def set_music_fade_in_time(self, music_fade_in_time: float):
        self._music_fade_in_time = music_fade_in_time
        self.notify_observers()



