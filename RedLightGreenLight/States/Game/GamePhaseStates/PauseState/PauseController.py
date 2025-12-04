import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhasesEnum import GamePhasesEnum
from RedLightGreenLight.States.Game.GamePhaseStates.PauseState.PauseModel import PauseModel
from RedLightGreenLight.States.Game.GamePhaseStates.PauseState.PauseView import PauseView
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateResult import StateResult
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory



class PauseController:
    def __init__(self, model: PauseModel, view: PauseView, settings_model: SettingsModel, music_manager: MusicManager):
        pass
        self._model = model
        self._view = view
        self._music_manager = music_manager
        self._settings_model = settings_model

    def enter(self,game_model:GameModel):
        game_model.update_phase_info(GamePhasesEnum.PAU)
        self._update_music()

    def update(self, delta_time: float,game_model:GameModel) -> GamePhaseState:
        return self._handle_events()
        # result = StateResult()
        # self._game_model.update_time(delta_time)
        # self._handle_events(result)
        # self._view.show(delta_time)
        # return result


    def _handle_events(self) -> GamePhaseState:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GamePhaseStateFactory.create_quit_game_state()
        return GamePhaseStateFactory.create_pause_state(self._view.get_screen(),self._settings_model,self._music_manager)

    def _handle_keyboard_press_event(self, event) -> str|None:
        pass

    def _update_music(self) -> None:
        pass
        # if self._settings_model.is_music():
        #     self._music_manager.play(SoundPaths.RED_LIGHT,True)

    def update_settings(self):
        self._model.update_settings()