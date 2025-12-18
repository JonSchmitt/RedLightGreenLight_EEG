import pygame

from RedLightGreenLight.Inputs.KeysEnum import KEY
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu import SettingsModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.Game.GameController import GameController
from RedLightGreenLight.States.Game.GameView import GameView
from RedLightGreenLight.States.Game.GameModel import GameModel


class GameState(State, SettingsObserver):
    """
    State for the active game.
    Initializes Controller, Model and View for the game mode.
    """
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        _screen = screen
        _settings_model = settings_model
        _music_manager = music_manager


        _game_model = GameModel(settings_model.is_second_player(),_screen)
        _view = GameView(settings_model, _game_model, screen)
        self._controller = GameController(settings_model, music_manager,
                                          _game_model, _view, screen)

    def enter(self, screen: pygame.Surface = None) -> None:
        """Starts the controller on enter."""
        super().enter(screen)
        self._controller.enter()


    def update(self, delta_time: float,keys_pressed:list[list[KEY]]) -> State|None:
        """
        Delegates workload to the controller.
        """
        # What happens in the controller decides the next state
        return self._controller.update(delta_time,keys_pressed)


    def update_settings(self):
        print(f"GameState.update_settings()")
        self._controller.update_settings()
