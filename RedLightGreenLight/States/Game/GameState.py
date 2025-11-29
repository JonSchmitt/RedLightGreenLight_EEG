import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu import SettingsModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsObserver import SettingsObserver
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.Game.GameController import GameController
from RedLightGreenLight.States.Game.GameView import GameView
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.StateFactory import StateFactory
from RedLightGreenLight.States.StateResultsEnum import KEY, BUT


class GameState(State, SettingsObserver):
    def __init__(self, screen: pygame.Surface, settings_model: SettingsModel,
                 music_manager: MusicManager):
        super().__init__()
        self._screen = screen
        self._settings_model = settings_model
        self._music_manager = music_manager


        self._game_model = GameModel(settings_model.is_second_player())
        self._view = GameView(settings_model, self._game_model, screen)
        self._controller = GameController(settings_model, music_manager,
                                          self._game_model, self._view, screen)


    def update(self, delta_time: float) -> State|None:
        """
        Update - call every frame
        """
        # What happens in the controller decides the next state
        result = self._controller.update(delta_time)
        # Return state based on teh keyword returned
        if result.get_quit():
            # End Game
            return None
        for key in result.get_keys():
            if key == KEY.ESC:
                # Return to Menu
                return StateFactory.create_menu_state(self._screen, self._settings_model, self._music_manager)

        # Stay in GameState
        return StateFactory.create_game_state(self._screen, self._settings_model, self._music_manager)





    def update_settings(self):
        print(f"GameState.update_settings()")
        self._controller.update_settings()
