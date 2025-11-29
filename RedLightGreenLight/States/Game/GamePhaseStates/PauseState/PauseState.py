from typing import Optional

import pygame

from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.States.Game.GamePhaseStates.PauseState.PauseController import PauseController
from RedLightGreenLight.States.Game.GamePhaseStates.PauseState.PauseModel import PauseModel
from RedLightGreenLight.States.Game.GamePhaseStates.PauseState.PauseView import PauseView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver


class PauseState(GamePhaseState, SettingsObserver):
    """
    Pause Phase - currently has no usage
    """

    def __init__(self, screen: pygame.Surface,  settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._screen = screen
        self._model = PauseModel()
        self._view = PauseView(screen,self._model,  settings_model, music_manager)
        self._controller = PauseController(self._model, self._view, settings_model, music_manager)
        self._settings_model = settings_model
        self._music_manager = music_manager

        self._previous_GamePhaseState = None

    def enter(self,context:GameContext):
        super().enter(context)
        self._controller.enter(context)


    def update(self, delta_time: float, context:GameContext) -> Optional[GamePhaseState]:
        result = self._controller.update(delta_time,context)

        # Quit Game
        if result.get_quit():
            return None
        # elif ...
        else:
            return GamePhaseStateFactory.create_pause_state(self._screen, self._settings_model, self._music_manager)

    def update_settings(self):
        self._controller.update_settings()