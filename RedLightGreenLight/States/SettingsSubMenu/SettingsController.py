from __future__ import annotations

import pygame_gui

from RedLightGreenLight.Inputs.KeysEnum import KEY
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.SettingsSubMenu.SettingsView import SettingsView
import pygame
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.StateFactory import StateFactory


class SettingsController:
    """Controller for the settings-menu."""
    _MENU = "menu"
    _QUIT = "quit"

    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager, view: SettingsView):
        self._settings_model = settings_model
        self._view = view
        self._music_manager = music_manager


    def enter(self,screen:pygame.Surface = None)->None:
        self._start_music()
        if screen:
            self._view.enter(screen)

    def update(self,delta_time,keys_pressed:list[list[KEY]])->State:
        self._view.show(delta_time)
        self._update_music(delta_time)
        return self._decide_next_state(keys_pressed)


    def _start_music(self) -> None:
        if self._settings_model.is_music():
            self._music_manager.play(SoundPaths.MENU_MUSIC, True, fade_in=True,
                                     fade_in_time=self._settings_model.get_music_fade_in_time())

    def _update_music(self, delta_time: float) -> None:
        if self._settings_model.is_music():
            self._music_manager.update(delta_time)

    def _decide_next_state(self, keys_pressed: list[list[KEY]]):
        results = self._handle_events(keys_pressed)
        if self._QUIT in results:
            return StateFactory.create_quit_state()
        if self._MENU in results:
            return StateFactory.create_menu_state(self._view.get_screen(), self._settings_model, self._music_manager)
        return StateFactory.create_settings_state(self._view.get_screen(), self._settings_model,
                                                  self._music_manager)

    def _handle_events(self, keys_pressed: list[list[KEY]]) -> list[str]:
        results = []
        self._handle_keyboard_events(results, keys_pressed)
        for event in pygame.event.get():
            self._view.get_manager().process_events(event)
            if event.type == pygame.QUIT:
                results.append(self._QUIT)
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_event(event, results)
            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                self._handle_slider_events(event)
            elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED or event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                self._handle_checkbox_events(event)
        return results

    def _handle_keyboard_events(self, results: list[str], keys_pressed: list[list[KEY]]) -> None:
        key_down = keys_pressed[1]
        if KEY.ESC in key_down:
            results.append(self._MENU)

    def _handle_button_event(self, event: pygame.event, results: list[str]) -> None:
        """Handles a single button event."""
        if event.ui_element == self._view.get_ok_button():
            self._update_settings_in_model()
            results.append(self._MENU)

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



