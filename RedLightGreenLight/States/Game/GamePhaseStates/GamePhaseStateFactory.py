
class GamePhaseStateFactory:
    _pause_state = None
    _red_light_state = None
    _green_light_state = None
    _game_over_state = None
    _restart_state = None

    @staticmethod
    def create_pause_state(screen, settings_model, music_manager):
        if not GamePhaseStateFactory._pause_state:
            from RedLightGreenLight.States.Game.GamePhaseStates.PauseState.PauseState import PauseState
            GamePhaseStateFactory._pause_state = PauseState(screen, settings_model, music_manager)
        return GamePhaseStateFactory._pause_state

    @staticmethod
    def create_red_light_state(screen, settings_model, music_manager):
        if not GamePhaseStateFactory._red_light_state:
            from RedLightGreenLight.States.Game.GamePhaseStates.RedLightState.RedLightState import RedLightState
            GamePhaseStateFactory._red_light_state = RedLightState(screen, settings_model, music_manager)
        return GamePhaseStateFactory._red_light_state

    @staticmethod
    def create_green_light_state(screen, settings_model, music_manager):
        if not GamePhaseStateFactory._green_light_state:
            from RedLightGreenLight.States.Game.GamePhaseStates.GreenLightState.GreenLightState import GreenLightState
            GamePhaseStateFactory._green_light_state = GreenLightState(screen, settings_model, music_manager)
        return GamePhaseStateFactory._green_light_state

    @staticmethod
    def create_game_over_state(screen, settings_model, music_manager):
        if not GamePhaseStateFactory._game_over_state:
            from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GameOverState import GameOverState
            GamePhaseStateFactory._game_over_state = GameOverState(screen, settings_model, music_manager)
        return GamePhaseStateFactory._game_over_state


    @staticmethod
    def create_restart_state(screen, settings_model, music_manager):
        if not GamePhaseStateFactory._restart_state:
            from RedLightGreenLight.States.Game.GamePhaseStates.RestartState.RestartState import RestartState
            GamePhaseStateFactory._restart_state = RestartState(screen, settings_model, music_manager)
        return GamePhaseStateFactory._restart_state