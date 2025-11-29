from typing import Optional
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsController import SettingsController
from RedLightGreenLight.States.SettingsSubMenu import SettingsModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsView import SettingsView
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.StateFactory import StateFactory
from RedLightGreenLight.States.StateResultsEnum import KEY,BUT


class SettingsState(State):
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._screen = screen
        self._settings_model = settings_model
        self._music_manager = music_manager

        self._view = SettingsView(settings_model, screen)
        self._controller = SettingsController(settings_model, music_manager,
                                              self._view)

    def enter(self,screen:pygame.Surface = None):
        self._controller.enter(screen)

    def update(self,delta_time:float) -> Optional[State]:
        """
        Update - call every frame
        """
        result = self._controller.update(delta_time)
        if result.get_quit():
            return None
        for key in result.get_keys():
            if key == BUT.OK or key == KEY.ESC:
                return StateFactory.create_menu_state(self._screen, self._settings_model, self._music_manager)

        return StateFactory.create_settings_state(self._screen, self._settings_model, self._music_manager)


