from typing import Optional

import pygame

from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSController import RLSController
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSModel import RLSModel
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSView import RLSView
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.StateResultsEnum import STATE
from RedLightGreenLight.States.Game.GameContext import GameContext



class RedLightState(GamePhaseState, SettingsObserver):
    """
    RedLightState
    """
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._screen = screen
        self._model = RLSModel(settings_model.get_switch_time())
        self._view = RLSView(screen, self._model, settings_model, music_manager)
        self._controller = RLSController(self._model, self._view, settings_model, music_manager)
        self._settings_model = settings_model
        self._music_manager = music_manager

    def enter(self, context:GameContext):
        super().enter(context)
        self._controller.enter(context)

    def update(self, delta_time: float,context:GameContext) -> Optional[GamePhaseState]:
        result = self._controller.update(delta_time,context)
        if result.get_quit():
            return None
        elif result.get_next_state() == STATE.GAME_OVER_STATE:
            return GamePhaseStateFactory.create_game_over_state(self._screen, self._settings_model, self._music_manager)
        elif result.get_next_state() == STATE.GREEN_LIGHT_STATE:
            return GamePhaseStateFactory.create_green_light_state(self._screen, self._settings_model, self._music_manager)
        elif result.get_next_state() == STATE.RED_LIGHT_STATE:
            return GamePhaseStateFactory.create_red_light_state(self._screen, self._settings_model, self._music_manager)
        else:
            print("Warning: RedLightState: Unknown NextState: {result.get_next_state()}")
            return GamePhaseStateFactory.create_red_light_state(self._screen, self._settings_model, self._music_manager)


    def update_settings(self):
        self._controller.update_settings()