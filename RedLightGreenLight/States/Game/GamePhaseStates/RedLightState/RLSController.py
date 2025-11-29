import pygame

from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSModel import RLSModel
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSView import RLSView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.StateResult import StateResult
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateResultsEnum import STATE


class RLSController:
    def __init__(self, model: RLSModel, view: RLSView, settings_model: SettingsModel, music_manager: MusicManager):
        self._model = model
        self._view = view
        self._music_manager = music_manager#
        self._settings_model = settings_model

    def enter(self,context:GameContext):
        context.update_from_phase("RedLightState")
        self._update_music()
        self._model.reset_time_in_phase()

    def update(self, delta_time: float,context:GameContext) -> StateResult:
        result = StateResult()
        self._model.update_time_in_phase(delta_time)
        self._view.show(delta_time)
        self._decide_next_state(context, result)
        return result

    def update_settings(self):
        self._model.update_settings(self._settings_model.get_switch_time())

    def _decide_next_state(self, context:GameContext, result):
        if context.all_players_dead():
            result.set_next_state(STATE.GAME_OVER_STATE)
        elif self._model.switch_phase():
            result.set_next_state(STATE.GREEN_LIGHT_STATE)
        else:
            result.set_next_state(STATE.RED_LIGHT_STATE)


    def _update_music(self) -> None:
        if self._settings_model.is_music():
            self._music_manager.play(SoundPaths.RED_LIGHT,True)



