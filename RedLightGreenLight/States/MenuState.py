
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.State import State
from RedLightGreenLight.Menu.MenuController import MenuController
from RedLightGreenLight.Menu.MenuView import MenuView
from RedLightGreenLight.Menu.MenuModel import MenuModel
from RedLightGreenLight.States.StateFactory import StateFactory
from RedLightGreenLight.States.StateKeywords import StateKeywords as skw


class MenuState(State, SettingsObserver):
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self.screen = screen
        self.settings_model = settings_model
        self.music_manager = music_manager

        self.model = MenuModel()
        self.view = MenuView(settings_model, self.model, screen)
        self.controller = MenuController(settings_model, music_manager,
                                         self.model, self.view)


    def enter(self,delta_time:float) -> State|None:
        """
        Entering Menu State - führt Entry-Aktion aus
        """
        print("Entering Menu State")
        result = self.controller.update(delta_time)
        if result.get_quit():
            return None

        for key in result.get_keys():
            if key == skw.MENU_OK or key == skw.MENU_ESC:
                self.view.hide()
                print("Exiting Menu State")
                return StateFactory.create_game_state(self.screen, self.settings_model, self.music_manager)
            if key == skw.MENU_SETTINGS:
                self.view.hide()
                print("Exiting Menu State")
                return StateFactory.create_settings_state(self.screen, self.settings_model, self.music_manager)
        return StateFactory.create_menu_state(self.screen, self.settings_model, self.music_manager)



    def update_settings(self):
        self.controller.update_settings()
