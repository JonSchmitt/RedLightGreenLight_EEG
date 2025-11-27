from queue import Queue

import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.State import State
from RedLightGreenLight.Menu.MenuController import MenuController
from RedLightGreenLight.Menu.MenuView import MenuView
from RedLightGreenLight.Menu.MenuModel import MenuModel

class MenuState(State, SettingsObserver):
    def __init__(self,screen:pygame.Surface, settings_model:SettingsModel, music_manager:MusicManager, state_events:Queue):
        self.model = MenuModel()
        self.view = MenuView(settings_model,self.model,screen)
        self.controller = MenuController(settings_model,music_manager,self.model, self.view, state_events)

    def enter(self):
        print("Entering Menu State")



    def exit(self):
        print("Exiting Menu State")
        self.view.hide()

    def update(self,delta_time:float):
        self.controller.update(delta_time)

    def handle_events(self,events:pygame.event):
        self.controller.handle_events(events)

    def update_settings(self):
        self.controller.update_settings()