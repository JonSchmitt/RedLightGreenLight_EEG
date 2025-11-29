from typing import Optional

import pygame

from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSModel import GameOverModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSController import GameOverController
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSView import GameOverView
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.StateResultsEnum import STATE


class GameOverState(GamePhaseState, SettingsObserver):
    """
    RedLightState
    """
    def __init__(self, screen: pygame.Surface,  settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._screen = screen
        self._game_over_model = GameOverModel(settings_model.get_game_over_duration())
        self._view = GameOverView(screen, self._game_over_model, settings_model, music_manager)
        self._controller = GameOverController(self._game_over_model, self._view, settings_model, music_manager)

        self._settings_model = settings_model
        self._music_manager = music_manager



    def enter(self, context: GameContext) ->None:
        super().enter(context)
        self._controller.enter(context)

    def update(self, delta_time: float, context: GameContext) -> Optional[GamePhaseState]:
        result = self._controller.update(delta_time, context)

        if result.get_quit():
            return None
        elif result.get_next_state() == STATE.RESTART_STATE:
            return GamePhaseStateFactory.create_restart_state(self._screen, self._settings_model, self._music_manager)
        elif result.get_next_state() == STATE.GAME_OVER_STATE:
            return GamePhaseStateFactory.create_game_over_state(self._screen, self._settings_model, self._music_manager)
        else:
            print(f"Warning: GameOverState: Unknown NextState: {result.get_next_state()}")
            return GamePhaseStateFactory.create_game_over_state(self._screen, self._settings_model, self._music_manager)

    def update_settings(self):
        self._controller.update_settings()
