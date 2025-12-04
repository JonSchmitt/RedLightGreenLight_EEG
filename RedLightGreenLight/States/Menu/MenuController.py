from __future__ import annotations

import pygame_gui
from RedLightGreenLight.States.Menu.MenuView import MenuView
from RedLightGreenLight.States.Menu.MenuModel import MenuModel
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.StateFactory import StateFactory
from RedLightGreenLight.Inputs.KeysEnum import KEY


class MenuController:
    _QUIT = "quit"
    _SETTINGS = "settings"
    _GAME = "game"

    """Controller for the menu."""
    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager,model: MenuModel, view: MenuView):
        self._settings_model = settings_model
        self._model = model
        self._view = view
        self._music_manager = music_manager

    def enter(self,screen:pygame.Surface)->None:
        if screen:
            self._view.enter(screen)

        self._start_music()

    def update(self,delta_time,keys_pressed:list[list[KEY]])->State|None:
        self._view.show(delta_time)
        self._update_music(delta_time)
        next_state = self._decide_next_state(keys_pressed)
        return next_state

    def _decide_next_state(self, keys_pressed:list[list[KEY]]):
        results = self._handle_events(keys_pressed)
        if self._QUIT in results:
            return StateFactory.create_quit_state()
        if self._SETTINGS in results:
            return StateFactory.create_settings_state(self._view.get_screen(),self._settings_model,self._music_manager)
        if self._GAME in results:
            return StateFactory.create_game_state(self._view.get_screen(),self._settings_model,self._music_manager)
        return StateFactory.create_menu_state(self._view.get_screen(),self._settings_model,self._music_manager)


    def _handle_events(self,keys_pressed:list[list[KEY]])->list[str]:
        results = []
        self._handle_keyboard_events(results,keys_pressed)
        for event in pygame.event.get():
            self._view.get_manager().process_events(event)
            if event.type == pygame.QUIT:
                results.append(self._QUIT)
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_event(event, results)
        return results


    def _handle_keyboard_events(self,results:list[str],keys_pressed:list[list[KEY]])->None:
        keys_down = keys_pressed[1]
        if KEY.ESC in keys_down:
            results.append(self._GAME)


    def _handle_button_event(self, event:pygame.event, results:list[str])->None:
        """Handles a single button event."""
        if event.ui_element == self._view.get_ok_button():
            results.append(self._GAME)
        elif event.ui_element == self._view.get_quit_button():
            results.append(self._QUIT)
        elif event.ui_element == self._view.get_settings_button():
            results.append(self._SETTINGS)

    def _start_music(self) -> None:
        if self._settings_model.is_music():
            self._music_manager.play(SoundPaths.MENU_MUSIC, True, fade_in=True,
                                     fade_in_time=self._settings_model.get_music_fade_in_time())

    def _update_music(self, delta_time: float) -> None:
        if self._settings_model.is_music():
                self._music_manager.update(delta_time)


    def update_settings(self):
        pass

