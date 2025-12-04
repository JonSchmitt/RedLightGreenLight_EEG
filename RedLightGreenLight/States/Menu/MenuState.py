
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu import SettingsModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.Menu.MenuController import MenuController
from RedLightGreenLight.States.Menu.MenuView import MenuView
from RedLightGreenLight.States.Menu.MenuModel import MenuModel
from RedLightGreenLight.States.StateFactory import StateFactory
from RedLightGreenLight.Inputs.KeysEnum import KEY


class MenuState(State, SettingsObserver):
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        screen = screen
        settings_model = settings_model
        music_manager = music_manager

        model = MenuModel()
        view = MenuView(settings_model, model, screen)
        self._controller = MenuController(settings_model, music_manager,
                                          model, view)


    def enter(self,screen:pygame.Surface = None):
        super().enter(screen)
        self._controller.enter(screen)


    def update(self,delta_time:float,keys:list[list[KEY]]) -> State|None:
        """
        Update - call every frame
        """
        return self._controller.update(delta_time,keys)



    def update_settings(self):
        """
        Update settings - Listener callback for Settingsmodel
        """
        self._controller.update_settings()
