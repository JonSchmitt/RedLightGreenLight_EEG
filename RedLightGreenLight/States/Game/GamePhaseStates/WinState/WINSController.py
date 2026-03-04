from typing import Optional
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.States.Game.GamePhaseStates.WinState.WINSModel import WINSModel
from RedLightGreenLight.States.Game.GamePhaseStates.WinState.WINSView import WINSView
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhasesEnum import GamePhasesEnum

class WINSController:
    """
    Controller for the Win state.
    """
    def __init__(self, model: WINSModel, view: WINSView, settings_model: SettingsModel, music_manager: MusicManager):
        self._model = model
        self._view = view
        self._settings_model = settings_model
        self._music_manager = music_manager

    def enter(self, game_model: GameModel):
        game_model.update_phase_info(GamePhasesEnum.WINS)
        self._model.reset()
        self._model.winner_name = game_model.get_current_winner() or "Someone"

    def update(self, delta_time: float, game_model: GameModel) -> Optional[GamePhaseState]:
        self._model.update_time(delta_time)
        self._view.show(delta_time)

        if self._model.is_time_up():
            game_model.restart_game() # This resyncs entities (resets positions/dead status)
            from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
            return GamePhaseStateFactory.create_green_light_state(self._view.get_screen(), self._settings_model, self._music_manager)
        
        from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
        return GamePhaseStateFactory.create_win_state(self._view.get_screen(), self._settings_model, self._music_manager)
