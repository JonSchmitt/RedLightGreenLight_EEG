from queue import Queue
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.SettingsSubMenu.SettingsController import SettingsController
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.SettingsSubMenu.SettingsView import SettingsView
from RedLightGreenLight.States.State import State


class SettingsState(State):
    def __init__(self,screen:pygame.Surface, settings_model:SettingsModel, music_manager:MusicManager, state_events:Queue):
        self.view = SettingsView(settings_model,screen)
        self.controller = SettingsController(settings_model,music_manager, self.view, state_events)

    def enter(self):
        print("Entering Settings State")

    def exit(self):
        print("Exiting Settings State")
        self.view.hide()


    def update(self,delta_time:float):
        self.controller.update(delta_time)

    def handle_events(self,events:pygame.event):
        self.controller.handle_events(events)

