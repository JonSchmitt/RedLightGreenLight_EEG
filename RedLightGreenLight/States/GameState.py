from queue import Queue
from typing import Optional
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.MenuState import MenuState
from RedLightGreenLight.States.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.State import State
from RedLightGreenLight.Game.GameController import GameController
from RedLightGreenLight.Game.GameView import GameView
from RedLightGreenLight.Game.GameModel import GameModel
from RedLightGreenLight.States.StateFactory import StateFactory
from RedLightGreenLight.States.StateKeywords import StateKeywords as skw


class GameState(State, SettingsObserver):
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self.screen = screen
        self.settings_model = settings_model
        self.music_manager = music_manager


        self.model = GameModel(settings_model.get_switch_time(),
                               settings_model.get_warning_time())
        self.view = GameView(settings_model, self.model, screen)
        self.controller = GameController(settings_model, music_manager,
                                         self.model, self.view)



    def enter(self, delta_time: float) -> State|None:
        """
        Entering Game State - führt Entry-Aktion aus
        """
        print("Entering Game State")
        self.model.set_pause(False)
        # What happens in the controller decides the next state
        result = self.controller.update(delta_time)
        # Return state based on teh keyword returned
        if result.get_quit():
            return None
        for key in result.get_keys():
            if key == skw.GAME_ESC:
                self.model.set_pause(True)
                self.view.hide()
                print("Exiting Game State")
                return StateFactory.create_menu_state(self.screen, self.settings_model, self.music_manager)

        return StateFactory.create_game_state(self.screen, self.settings_model, self.music_manager)


    def update_settings(self):
        self.controller.update_settings()
