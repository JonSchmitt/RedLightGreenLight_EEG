from typing import Optional

import pygame

from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSModel import GOSModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSController import GOSController
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSView import GOSView
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver


class GameOverState(GamePhaseState, SettingsObserver):
    """
    Game Over State.
    Shows the Game Over screen after all players died.
    """
    def __init__(self, screen: pygame.Surface,  settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._screen = screen
        self._game_over_model = GOSModel(settings_model.get_game_over_duration())
        self._view = GOSView(screen, self._game_over_model, settings_model, music_manager)
        self._controller = GOSController(self._game_over_model, self._view, settings_model, music_manager)

        self._settings_model = settings_model
        self._music_manager = music_manager



    def enter(self, game_model:GameModel) ->None:
        super().enter(game_model)
        self._controller.enter(game_model)

    def update(self, delta_time: float, game_model:GameModel) -> Optional[GamePhaseState]:
        return self._controller.update(delta_time, game_model)


    def update_settings(self):
        self._controller.update_settings()
