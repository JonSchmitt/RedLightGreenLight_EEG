

class StateFactory:
    """
    Factory Pattern for creaing and managing state instances.
    Uses Lazy Initialization and Singleton-like behavior to reuse states.
    """
    _game_state = None
    _menu_state = None
    _settings_state = None
    _quit_state = None

    @staticmethod
    def create_game_state(screen, settings_model, music_manager):
        """Creates or returns the existing GameState."""
        if not StateFactory._game_state:
            from RedLightGreenLight.States.Game.GameState import GameState
            StateFactory._game_state = GameState(screen, settings_model, music_manager)
        return StateFactory._game_state

    @staticmethod
    def create_menu_state(screen, settings_model, music_manager):
        """Creates or returns the existing MenuState."""
        if not StateFactory._menu_state:
            from RedLightGreenLight.States.Menu.MenuState import MenuState
            StateFactory._menu_state = MenuState(screen, settings_model, music_manager)
        return StateFactory._menu_state

    @staticmethod
    def create_settings_state(screen, settings_model, music_manager):
        """Creates or returns the existing SettingsState."""
        if not StateFactory._settings_state:
            from RedLightGreenLight.States.SettingsSubMenu.SettingsState import SettingsState
            StateFactory._settings_state = SettingsState(screen, settings_model, music_manager)
        return StateFactory._settings_state

    @staticmethod
    def create_quit_state():
        """Creates or returns the existing QuitState."""
        if not StateFactory._quit_state:
            from RedLightGreenLight.States.QuitState import QuitState
            StateFactory._quit_state = QuitState()
        return StateFactory._quit_state

