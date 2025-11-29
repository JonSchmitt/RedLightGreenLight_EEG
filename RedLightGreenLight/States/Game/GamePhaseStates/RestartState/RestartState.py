from typing import Optional

import pygame

from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSModel import GameOverModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSController import GameOverController
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSView import GameOverView
from RedLightGreenLight.States.StateResultsEnum import STATE


class RestartState(GamePhaseState):
    """
    RedLightState
    """
    def __init__(self, screen: pygame.Surface,  settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._screen = screen
        self._settings_model = settings_model
        self._music_manager = music_manager



    def enter(self, context: GameContext) ->None:
        super().enter(context)

    def update(self, delta_time: float, context: GameContext) -> Optional[GamePhaseState]:
        return GamePhaseStateFactory.create_green_light_state(self._screen, self._settings_model, self._music_manager)
