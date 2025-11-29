import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.Game.GamePhaseStates.PauseState.PauseModel import PauseModel
from RedLightGreenLight.States.Game.GamePhaseStates.PauseState.PauseView import PauseView
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateResult import StateResult


class PauseController:
    def __init__(self, model: PauseModel, view: PauseView, settings_model: SettingsModel, music_manager: MusicManager):
        pass
        self._model = model
        # self._view = view
        # self._music_manager = music_manager
        # self._settings_model = settings_model

    def enter(self,context:GameContext):
        context.update_from_phase("PauseState")
        self._update_music()

    def update(self, delta_time: float, context:GameContext) -> StateResult:
        pass
        # result = StateResult()
        # self._game_model.update_time(delta_time)
        # self._handle_events(result)
        # self._view.show(delta_time)
        # return result

    def _handle_events(self, result) -> None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result.set_quit()

    def _handle_keyboard_press_event(self, event) -> str|None:
        pass

    def _update_music(self) -> None:
        pass
        # if self._settings_model.is_music():
        #     self._music_manager.play(SoundPaths.RED_LIGHT,True)

    def update_settings(self):
        self._model.update_settings()