from typing import Optional

import pygame

from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhasesEnum import GamePhasesEnum
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory


class RestartState(GamePhaseState):
    """
    RestartState
    """
    def __init__(self, screen: pygame.Surface,  settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._screen = screen
        self._settings_model = settings_model
        self._music_manager = music_manager



    def enter(self, game_model: GameModel) ->None:
        super().enter(game_model)
        game_model.update_phase_info(GamePhasesEnum.RES)

    def update(self, delta_time: float, game_model: GameModel) -> Optional[GamePhaseState]:
        game_model.restart_game()
        return GamePhaseStateFactory.create_green_light_state(self._screen, self._settings_model, self._music_manager)
