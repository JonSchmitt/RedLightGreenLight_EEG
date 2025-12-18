import pygame
import pygame_gui

from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.Game.GamePhaseStates.GameOverState.GOSModel import GameOverModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.UIElements.AutoLabel import AutoLabel
from RedLightGreenLight.UIUtil.UIManager import UIManager


class GOSView:
    """
    View for the Game Over State.
    Displays "Game Over" text.
    """
    def __init__(self, screen: pygame.Surface, game_over_model: GameOverModel, settings_model: SettingsModel,
                 music_manager: MusicManager):
        self._screen = screen
        self._game_over_model = game_over_model
        self._settings = settings_model
        self._music_manager = music_manager
        self._manager = UIManager(self._screen)

        self._initialize_ui()

    def show(self, delta_time: float) -> None:
        self._screen.fill((50, 50, 50))
        self._update_labels()
        self._manager.update(delta_time)
        self._manager.draw_ui(self._screen)

    def _initialize_ui(self):
        self._game_over_label = AutoLabel(
            text="",
            rect=pygame.Rect(0, 0, 400, 100),  # Breite und Höhe angeben!
            manager=self._manager,
            object_id="#GameOverLabel",
            anchors={'centerx': 'centerx', 'centery': 'centery'}
        )
        # self._game_over_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, 500, 500), manager=self._manager,
        #                                                     text="",
        #                                                     anchors={'centerx': 'centerx', 'centery': 'centery'},
        #                                                     object_id="#GameOverLabel")

    def _update_labels(self):
        new_text = f"YOU DIED!\nContinue in: {int(round(self._game_over_model.get_remaining_game_over_time()))}"
        self._game_over_label.set_text(new_text)

    def get_screen(self):
        return self._screen
