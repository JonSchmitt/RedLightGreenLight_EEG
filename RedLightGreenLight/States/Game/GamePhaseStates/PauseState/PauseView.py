import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GamePhaseStates.PauseState.PauseModel import PauseModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel


class PauseView:
    def __init__(self, screen: pygame.Surface, model: PauseModel, settings_model: SettingsModel,
                 music_manager: MusicManager):
        self._screen = screen

    def show(self,delta_time, time_stamp):
        pass

    def get_screen(self):
        return self._screen