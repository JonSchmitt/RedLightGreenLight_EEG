from __future__ import annotations

import pygame
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from UIUtils.UIManager import UIManager


class GameView:
    """
    View for the game.
    Handles UI overlays and manages the graphical output.
    """
    def __init__(self, settings_model: SettingsModel, model: GameModel, screen: pygame.Surface):
        """
        Initializes the GameView.

        Args:
            settings_model (SettingsModel): The settings model.
            model (GameModel): The game model.
            screen (pygame.Surface): The main screen surface.
        """
        self._screen = screen
        self._settings = settings_model
        self._model = model
        self._manager = UIManager(self._screen)

    def get_screen(self) -> pygame.Surface:
        """Returns the main screen surface."""
        return self._screen

    def show(self, delta_time: float):
        """
        Updates and draws the UI.

        Args:
            delta_time (float): Time since last frame in seconds.
        """
        self._manager.update(delta_time)
        self._manager.draw_ui(self._screen)
        pygame.display.flip()

    def hide(self):
        """Hides the view (placeholder for cleanup)."""
        pass

