
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu import SettingsModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.Menu.MenuController import MenuController
from RedLightGreenLight.States.Menu.MenuView import MenuView
from RedLightGreenLight.States.Menu.MenuModel import MenuModel
from RedLightGreenLight.States.StateFactory import StateFactory
from RedLightGreenLight.States.StateResultsEnum import KEY, BUT


class MenuState(State, SettingsObserver):
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._screen = screen
        self._settings_model = settings_model
        self._music_manager = music_manager

        self._model = MenuModel()
        self._view = MenuView(settings_model, self._model, screen)
        self._controller = MenuController(settings_model, music_manager,
                                          self._model, self._view)


    def enter(self,screen:pygame.Surface = None):
        self._controller.enter(screen)


    def update(self,delta_time:float) -> State|None:
        """
        Update - call every frame
        """
        result = self._controller.update(delta_time)
        if result.get_quit():
            return None
        for key in result.get_keys():
            if key == BUT.OK or key == KEY.ESC:
                return StateFactory.create_game_state(self._screen, self._settings_model, self._music_manager)
            if key == BUT.SETTINGS:
                return StateFactory.create_settings_state(self._screen, self._settings_model, self._music_manager)
        return StateFactory.create_menu_state(self._screen, self._settings_model, self._music_manager)


    def update_settings(self):
        """
        Update settings - Listener callback for Settingsmodel
        """
        self._controller.update_settings()
