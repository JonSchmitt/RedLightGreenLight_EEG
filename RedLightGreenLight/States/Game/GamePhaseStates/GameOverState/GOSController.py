import pygame

from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSModel import GameOverModel
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSView import GameOverView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.StateResult import StateResult
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateResultsEnum import STATE


class GameOverController:
    def __init__(self, model:GameOverModel, view: GameOverView, settings_model: SettingsModel, music_manager: MusicManager):

        self._model = model
        self._view = view
        self._music_manager = music_manager
        self._settings_model = settings_model

    def enter(self, context: GameContext)->None:
        context.update_from_phase("GameOverState")
        self._update_music()
        self._model.start_game_over()

    def update(self, dt: float, context: GameContext) -> StateResult:
        result = StateResult()
        self._view.show(dt)
        self._update_music()
        if not self._model.is_game_over(dt):
            result.set_next_state(STATE.RESTART_STATE)
        else:
            result.set_next_state(STATE.GAME_OVER_STATE)
        return result


    def _handle_keyboard_press_event(self, event) -> str|None:
        pass

    def _update_music(self) -> None:
        # Play this even when music setting is disabled
        self._music_manager.play(SoundPaths.GAME_OVER,False)


    def update_settings(self):
        self._model.update_settings(self._settings_model.get_game_over_duration())