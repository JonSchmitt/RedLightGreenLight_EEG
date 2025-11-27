from queue import Queue

import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.State import State
from RedLightGreenLight.Game.GameController import GameController
from RedLightGreenLight.Game.GameView import GameView
from RedLightGreenLight.Game.GameModel import GameModel

class GameState(State, SettingsObserver):
    def __init__(self,screen:pygame.Surface, settings_model:SettingsModel, music_manager: MusicManager, state_events:Queue):
        self.model = GameModel(settings_model.get_switch_time(), settings_model.get_warning_time())
        self.view = GameView(settings_model,self.model,screen)
        self.controller = GameController(settings_model,music_manager,self.model, self.view,state_events)

        self._settings = settings_model

    def enter(self):
        print("Entering Game State")
        self.model.set_pause(False)

    def exit(self):
        print("Exiting Game State")
        self.model.set_pause(True)
        self.view.hide()

    def update(self,delta_time:float):
        self.controller.update(delta_time)


    def handle_events(self,events:pygame.event):
        self.controller.handle_events(events)

    def update_settings(self):
        self.controller.update_settings()
