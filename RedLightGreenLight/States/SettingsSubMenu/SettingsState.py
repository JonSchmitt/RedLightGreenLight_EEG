from typing import Optional
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsController import SettingsController
from RedLightGreenLight.States.SettingsSubMenu import SettingsModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsView import SettingsView
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.StateFactory import StateFactory
from RedLightGreenLight.Inputs.KeysEnum import KEY

class SettingsState(State):
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        screen = screen
        settings_model = settings_model
        music_manager = music_manager

        view = SettingsView(settings_model, screen)
        self._controller = SettingsController(settings_model, music_manager, view)

    def enter(self,screen:pygame.Surface = None):
        super().enter(screen)
        self._controller.enter(screen)

    def update(self,delta_time:float, keys_pressed:list[list[KEY]]) -> Optional[State]:
        """
        Update - call every frame
        """
        return self._controller.update(delta_time,keys_pressed)



