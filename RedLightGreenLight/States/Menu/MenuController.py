from __future__ import annotations

import pygame_gui
from RedLightGreenLight.States.Menu.MenuView import MenuView
from RedLightGreenLight.States.Menu.MenuModel import MenuModel
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.StateResultsEnum import KEY, BUT
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateResult import StateResult


class MenuController:
    """Controller for the menu."""
    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager,model: MenuModel, view: MenuView):
        self._settings = settings_model
        self._model = model
        self._view = view
        self._music_manager = music_manager

    def enter(self,screen:pygame.Surface)->None:
        if screen:
            self._view.enter(screen)

    def update(self,delta_time)->StateResult:
        result = StateResult()
        self._view.show(delta_time)
        if self._settings.is_music():
            self._music_manager.play(SoundPaths.MENU_MUSIC)
        self._handle_events(result)
        return result

    def _handle_events(self,result:StateResult):
        """Handles all events for the menu."""
        for event in pygame.event.get():
            self._view.get_manager().process_events(event)
            if event.type == pygame.QUIT:
                result.set_quit(True)
            if event.type == pygame.KEYDOWN:
                result.add_key(self._handle_keyboard_events(event))
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_events(event, result)

    def _handle_keyboard_events(self, event)->KEY|None:
        """Handles a single keyboard event."""
        if event.key == pygame.K_ESCAPE:
            return KEY.ESC
        return None

    def _handle_button_events(self, event:pygame.event,result:StateResult):
        """Handles a single button event."""
        if event.ui_element == self._view.get_ok_button():
            result.add_key(KEY.ESC)
        elif event.ui_element == self._view.get_quit_button():
            result.set_quit(True)
        elif event.ui_element == self._view.get_settings_button():
            result.add_key(BUT.SETTINGS)



    def update_settings(self):
        pass
    #TODO: implement update_settings method
