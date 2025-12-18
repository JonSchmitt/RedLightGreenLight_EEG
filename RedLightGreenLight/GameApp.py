import pygame

from RedLightGreenLight.Inputs.InputManager import InputManager
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GameState import GameState
from RedLightGreenLight.States.QuitState import QuitState
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateFactory import StateFactory


class GameApp:
    """
    Central class that initializes the game application and controls the main loop.
    It manages the initialization of Pygame, the managers (Input, Music, Settings),
    and the state transitions.
    """
    def __init__(self):
        pass

    def run(self):
        """
        Main loop of the application.

        Initializes:
        - Pygame
        - SettingsModel (Settings)
        - MusicManager (Background Music)
        - InputManager (Input Processing)
        - Screen (Window)

        Starts the application in 'MenuState'.

        The Loop (Game Loop):
        1. Limits framerate (60 FPS).
        2. Processes inputs (InputManager).
        3. Updates the current state (current_state.update).
        4. Switches the state if a new state is returned.
        5. Exits the app when 'QuitState' is reached.
        """
        pygame.init()

        settings_model = SettingsModel()
        music_manager = MusicManager()
        input_manager = InputManager()
        screen = pygame.display.set_mode(
            (settings_model.get_window_width(),
             settings_model.get_window_height())
        )

        game_screen = screen.copy()

        # initial state
        current_state = StateFactory.create_menu_state(screen, settings_model, music_manager)
        current_state.enter()
        settings_model.add_observer(current_state)

        # Clock
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(60)
            delta_time = clock.get_time() / 1000.0

            keys = input_manager.process_inputs()
            new_state = current_state.update(delta_time,keys)

            if isinstance(new_state,GameState):
                game_screen = screen.copy()

            if new_state and new_state is not current_state:
                current_state = new_state
                settings_model.add_observer(current_state)
                current_state.enter(game_screen)

            elif isinstance(new_state,QuitState):
                running = False




