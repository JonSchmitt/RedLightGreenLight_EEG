from typing import Optional

import pygame

from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSController import RLSController
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSModel import RLSModel
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSView import RLSView
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver




class RedLightState(GamePhaseState, SettingsObserver):
    """
    RedLightState
    """
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        _screen = screen
        _model = RLSModel(settings_model.get_switch_time())
        _view = RLSView(screen, _model, settings_model, music_manager)
        self._controller = RLSController(_model, _view, settings_model, music_manager)
        _settings_model = settings_model
        _music_manager = music_manager

    def enter(self,game_model:GameModel):
        super().enter(game_model)
        self._controller.enter(game_model)

    def update(self, delta_time: float,game_model:GameModel) -> Optional[GamePhaseState]:
        return self._controller.update(delta_time,game_model)



    def update_settings(self):
        self._controller.update_settings()