from typing import Optional
import pygame
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.States.Game.GamePhaseStates.WinState.WINSController import WINSController
from RedLightGreenLight.States.Game.GamePhaseStates.WinState.WINSModel import WINSModel
from RedLightGreenLight.States.Game.GamePhaseStates.WinState.WINSView import WINSView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver

class WinState(GamePhaseState, SettingsObserver):
    """
    Win State: Displays the winner for 5 seconds.
    """
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._model = WINSModel()
        self._view = WINSView(screen, self._model, settings_model, music_manager)
        self._controller = WINSController(self._model, self._view, settings_model, music_manager)

    def enter(self, game_model: GameModel) -> None:
        super().enter(game_model)
        self._controller.enter(game_model)

    def update(self, delta_time: float, game_model: GameModel) -> Optional[GamePhaseState]:
        return self._controller.update(delta_time, game_model)

    def update_settings(self):
        # Optional: update settings if needed
        pass
