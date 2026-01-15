from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates import GamePhaseState
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSModel import GOSModel
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSView import GOSView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhasesEnum import GamePhasesEnum
from RedLightGreenLight.States.StateResult import StateResult
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel


class GOSController:
    """
    Controller for the Game Over State.
    Manages the game over timer and restart transition.
    """
    def __init__(self, model:GOSModel, view: GOSView, settings_model: SettingsModel, music_manager: MusicManager):

        self._model = model
        self._view = view
        self._music_manager = music_manager
        self._settings_model = settings_model

    def enter(self, game_model:GameModel)->None:
        game_model.update_phase_info(GamePhasesEnum.GOS)
        self._update_music()
        self._model.start_game_over()

    def update(self, dt: float, game_model:GameModel) -> GamePhaseState:
        self._view.show(dt)
        self._update_music()
        if not self._model.is_game_over(dt):
            return GamePhaseStateFactory.create_restart_state(self._view.get_screen(), self._settings_model, self._music_manager)
        else:
            return GamePhaseStateFactory.create_game_over_state(self._view.get_screen(), self._settings_model, self._music_manager)


    def _handle_keyboard_press_event(self, event) -> str|None:
        pass

    def _update_music(self) -> None:
        # Play this even when music setting is disabled
        self._music_manager.play(SoundPaths.GAME_OVER,False)


    def update_settings(self):
        self._model.update_settings(self._settings_model.get_game_over_duration())