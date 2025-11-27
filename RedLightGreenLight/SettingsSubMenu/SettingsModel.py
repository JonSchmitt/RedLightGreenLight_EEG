from __future__ import annotations

class SettingsModel:
    def __init__(self):
        # Default settings
        self._fullscreen = False
        self._window_width = 1600
        self._window_height = 800
        self._music = True
        self._warning_time = 5
        self._switch_time = 10
        self._ui_scaling = 1.5
        self._settings_changed = False


    def is_fullscreen(self):
        return self._fullscreen

    def set_fullscreen(self, fullscreen:bool):
        self._fullscreen = fullscreen

    def get_window_width(self):
        return self._window_width

    def set_window_width(self, screen_width:int):
        self._window_width = screen_width

    def get_window_height(self):
        return self._window_height

    def set_window_height(self, screen_height:int):
        self._window_height = screen_height

    def is_music(self):
        return self._music

    def set_music(self, sound:bool):
        self._music = sound

    def get_warning_time(self):
        return self._warning_time

    def set_warning_time(self, warning_time:int):
        self._warning_time = warning_time

    def get_switch_time(self):
        return self._switch_time

    def set_switch_time(self, switch_time:int):
        self._switch_time = switch_time

    def is_settings_changed(self):
        return self._settings_changed

    def set_settings_changed(self, settings_changed:bool):
        self._settings_changed = settings_changed

    def get_ui_scaling(self):
        return self._ui_scaling

    def set_ui_scaling(self, ui_scaling:int):
        self._ui_scaling = ui_scaling


