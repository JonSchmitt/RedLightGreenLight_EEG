from typing import Optional

import pygame

from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.States.Game.GamePhaseStates.GreenLightState.GLSController import GLSController
from RedLightGreenLight.States.Game.GamePhaseStates.GreenLightState.GLSModel import GLSModel
from RedLightGreenLight.States.Game.GamePhaseStates.GreenLightState.GLSView import GLSView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver


class GreenLightState(GamePhaseState, SettingsObserver):
    """
    Green Light Phase: Players can move freely.
    """
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        screen = screen
        model = GLSModel(settings_model.get_switch_time(), settings_model.get_warning_time())
        view = GLSView(screen, model, settings_model, music_manager)
        self._controller = GLSController(model,view,settings_model,music_manager)


    def enter(self, game_model:GameModel) -> None:
        super().enter(game_model)
        self._controller.enter(game_model)

    def update(self, delta_time: float, game_model:GameModel) -> Optional[GamePhaseState]:
        return self._controller.update(delta_time,game_model)

    def update_settings(self):
        self._controller.update_settings()