from __future__ import annotations

import pygame_gui

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.SettingsSubMenu.SettingsView import SettingsView
import pygame
from RedLightGreenLight.States.StateResultsEnum import KEY,BUT
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateResult import StateResult


class SettingsController:
    """Controller for the settings-menu."""
    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager, view: SettingsView):
        self._settings_model = settings_model
        self._view = view
        self._music_manager = music_manager



    def enter(self,screen:pygame.Surface = None)->None:
        self._start_music()
        if screen:
            self._view.enter(screen)

    def update(self,delta_time)->StateResult:
        result = StateResult()
        self._view.show(delta_time)
        self._update_music(delta_time)
        self._handle_events(result)

        return result

    def _start_music(self) -> None:
        if self._settings_model.is_music():
            self._music_manager.play(SoundPaths.MENU_MUSIC, True, fade_in=True,
                                     fade_in_time=self._settings_model.get_music_fade_in_time())

    def _update_music(self, delta_time: float) -> None:
        if self._settings_model.is_music():
            self._music_manager.update(delta_time)


    def _handle_events(self,result:StateResult):
        """Handles all events for the settings-menu."""
        for event in pygame.event.get():
            self._view.get_manager().process_events(event)
            if event.type == pygame.QUIT:
                result.set_quit(True)
            if event.type == pygame.KEYDOWN:
                result.add_key(self._handle_keyboard_events(event))
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_events(event,result)
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                self._handle_slider_events(event)
            if event.type == pygame_gui.UI_CHECK_BOX_CHECKED or event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                self._handle_checkbox_events(event)


    def _handle_keyboard_events(self, event)->KEY|None:
        """Handles a single keyboard event."""
        if event.key == pygame.K_ESCAPE:
            self._view.reset_changes()
            if not self._settings_model.is_music():
                self._music_manager.stop()
            return KEY.ESC
        else:
            return None

    def _handle_button_events(self, event:pygame.event,result:StateResult)->BUT|None:
        """Handles a single button event."""
        if event.ui_element == self._view.get_ok_button():
            self._update_settings_in_model()
            result.add_key(BUT.OK)

    def _handle_slider_events(self, event)->None:
        """Handles a single slider event."""
        if event.ui_element == self._view.get_switch_time_slider().get_slider():
            self._view.get_switch_time_slider().on_slider_changed(event)
        elif event.ui_element == self._view.get_warning_time_slider().get_slider():
            self._view.get_warning_time_slider().on_slider_changed(event)
        elif event.ui_element == self._view.get_game_over_time_slider().get_slider():
            self._view.get_game_over_time_slider().on_slider_changed(event)

    def _handle_checkbox_events(self, event)->None:
        """Handles a single checkbox event."""
        if event.ui_element == self._view.get_music_checkbox():
            if self._view.get_music_checkbox().get_state():
                self._music_manager.play(SoundPaths.MENU_MUSIC)
            else:
                self._music_manager.stop()

    def _update_settings_in_model(self)->None:
        switch_time_new = int(self._view.get_switch_time_slider().get_value())
        warning_time_new = int(self._view.get_warning_time_slider().get_value())
        game_over_time_new = int(self._view.get_game_over_time_slider().get_value())
        music_new = self._view.get_music_checkbox().get_state()
        second_player_new = self._view.get_second_player_checkbox().get_state()
        if switch_time_new != self._settings_model.get_switch_time():
            self._settings_model.set_switch_time(switch_time_new)
        if warning_time_new != self._settings_model.get_warning_time():
            self._settings_model.set_warning_time(warning_time_new)
        if music_new != self._settings_model.is_music():
            self._settings_model.set_music(music_new)
        if game_over_time_new != self._settings_model.get_game_over_duration():
            self._settings_model.set_game_over_duration(game_over_time_new)
        if second_player_new != self._settings_model.is_second_player():
            self._settings_model.set_second_player(second_player_new)



