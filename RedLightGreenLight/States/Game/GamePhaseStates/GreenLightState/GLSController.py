import pygame

from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GreenLightState.GLSModel import GLSModel
from RedLightGreenLight.States.Game.GamePhaseStates.GreenLightState.GLSView import GLSView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateResult import StateResult
from RedLightGreenLight.States.StateResultsEnum import STATE


class GLSController:
    def __init__(self, model: GLSModel, view: GLSView, settings_model: SettingsModel, music_manager: MusicManager):
        self._model = model
        self._view = view
        self._music_manager = music_manager
        self._settings = settings_model

    def enter(self,context:GameContext):
        context.update_from_phase("GreenLightState")
        self._update_music()
        self._model.reset_time_in_phase()

    def update(self, delta_time: float,context:GameContext) -> StateResult:
        result = StateResult()
        self._model.update_time_in_phase(delta_time)
        self._view.show(delta_time)
        self._update_music()
        self._decide_next_state(context, result)
        return result


    def _decide_next_state(self, context:GameContext, result):
        if context.all_players_dead():
            result.set_next_state(STATE.GAME_OVER_STATE)
        elif self._model.switch_phase():
            result.set_next_state(STATE.RED_LIGHT_STATE)
        else:
            result.set_next_state(STATE.GREEN_LIGHT_STATE)


    def _update_music(self) -> None:
        if self._settings.is_music():
            self._music_manager.play(SoundPaths.GREEN_LIGHT,True)

    def update_settings(self):
        self._model.update_settings(self._settings.get_switch_time(), self._settings.get_warning_time())