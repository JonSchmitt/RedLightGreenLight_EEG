from queue import Queue
from typing import Optional
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.SettingsSubMenu.SettingsController import SettingsController
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.SettingsSubMenu.SettingsView import SettingsView
from RedLightGreenLight.States.MenuState import MenuState
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.StateFactory import StateFactory
from RedLightGreenLight.States.StateKeywords import StateKeywords as skw


class SettingsState(State):
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self.screen = screen
        self.settings_model = settings_model
        self.music_manager = music_manager

        self.view = SettingsView(settings_model, screen)
        self.controller = SettingsController(settings_model, music_manager,
                                             self.view)


    def enter(self,delta_time:float) -> Optional[State]:
        """
        Entering Settings State - führt Entry-Aktion aus
        """
        print("Entering Settings State")
        result = self.controller.update(delta_time)
        if result.get_quit():
            return None
        for key in result.get_keys():
            if key == skw.SETTINGS_OK or key == skw.SETTINGS_ESC:
                self.view.hide()
                print("Exiting Settings State")
                return StateFactory.create_menu_state(self.screen, self.settings_model, self.music_manager)


        return StateFactory.create_settings_state(self.screen, self.settings_model, self.music_manager)


