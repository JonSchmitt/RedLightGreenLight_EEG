import pygame

from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhasesEnum import GamePhasesEnum
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSModel import RLSModel
from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RLSView import RLSView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.StateResult import StateResult
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.Game.GameModel import GameModel

class RLSController:
    def __init__(self, model: RLSModel, view: RLSView, settings_model: SettingsModel, music_manager: MusicManager):
        self._model = model
        self._view = view
        self._music_manager = music_manager#
        self._settings_model = settings_model

    def enter(self,game_model:GameModel):
        game_model.update_phase_info(GamePhasesEnum.RLS)
        self._start_music()


    def update(self, delta_time: float,game_model:GameModel) -> GamePhaseState:
        self._model.update_time_in_phase(delta_time)
        self._view.show(delta_time)
        self._update_music(delta_time)
        return self._decide_next_state(game_model,)

    def update_settings(self):
        self._model.update_settings(self._settings_model.get_switch_time())

    def _decide_next_state(self, game_model:GameModel)->GamePhaseState:
        if game_model.get_all_players_dead():
            self._model.reset_time_in_phase()
            return GamePhaseStateFactory.create_game_over_state(self._view.get_screen(), self._settings_model, self._music_manager)
        elif self._model.switch_phase():
            self._model.reset_time_in_phase()
            return GamePhaseStateFactory.create_green_light_state(self._view.get_screen(), self._settings_model,
                                                                self._music_manager)
        else:
            return GamePhaseStateFactory.create_red_light_state(self._view.get_screen(), self._settings_model, self._music_manager)

    def _start_music(self) -> None:
        if self._settings_model.is_music():
            self._music_manager.play(SoundPaths.RED_LIGHT, True, fade_in=True,
                                     fade_in_time=self._settings_model.get_music_fade_in_time())

    def _update_music(self, delta_time: float) -> None:
        if self._settings_model.is_music():
            if self._model.get_remaining_time_in_phase() <= self._settings_model.get_music_fade_out_time()*1.1:
                self._music_manager.stop(True, self._settings_model.get_music_fade_out_time())
            self._music_manager.update(delta_time)



