import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GameState import GameState
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateFactory import StateFactory


class GameApp:
    def __init__(self):
        pygame.init()

        # Gemeinsame Ressourcen
        self._settings_model = SettingsModel()
        self._music_manager = MusicManager()
        self._screen = pygame.display.set_mode(
            (self._settings_model.get_window_width(),
             self._settings_model.get_window_height())
        )

        self._current_state = 0
        self._game_screen = self._screen.copy()

        # Clock für FPS-Kontrolle
        self._clock = pygame.time.Clock()


    def run(self):
        """Hauptschleife der Anwendung"""
        # initial state
        self._current_state = StateFactory.create_menu_state(self._screen, self._settings_model, self._music_manager)
        self._current_state.enter()
        self._settings_model.add_observer(self._current_state)
        running = True
        while running:
            self._clock.tick(60)
            delta_time = self._clock.get_time() / 1000.0
            new_state = self._current_state.update(delta_time)

            if isinstance(new_state,GameState):
                self._game_screen = self._screen.copy()

            if new_state and new_state is not self._current_state:
                self._current_state = new_state
                self._settings_model.add_observer(self._current_state)
                self._current_state.enter(self._game_screen)

            elif new_state is None:
                running = False




