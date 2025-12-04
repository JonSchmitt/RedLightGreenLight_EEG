from __future__ import annotations

import pygame
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.UIUtil.UIManager import UIManager


class GameView:
    """View for the game."""
    def __init__(self,settings_model:SettingsModel, model:GameModel, screen:pygame.Surface):
        self._screen = screen
        self._settings = settings_model
        self._model = model
        self._manager = UIManager(self._screen)



    def get_screen(self)->pygame.Surface:
        return self._screen

    def show(self,delta_time):
        self._manager.update(delta_time)
        self._manager.draw_ui(self._screen)
        pygame.display.flip()


    def hide(self):
        pass
