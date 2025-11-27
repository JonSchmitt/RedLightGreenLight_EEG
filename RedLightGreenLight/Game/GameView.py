from __future__ import annotations

import os

import pygame
import pygame_gui

from RedLightGreenLight.Game.GameModel import GameModel
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.UIElements.AnimatedObject import AnimatedObject
from RedLightGreenLight.UIElements.VBox import VBox
from RedLightGreenLight.UIUtil.UIManager import UIManager


class GameView:
    """View for the game."""
    def __init__(self,settings_model:SettingsModel, model:GameModel, screen:pygame.Surface):
        self._screen = screen
        self._settings = settings_model
        self._model = model
        self._manager = UIManager(self._screen)


        """
        vBox_height = int(100 * self._settings.get_ui_scaling())
        vBox_width = int(150 * self._settings.get_ui_scaling())
        label_height = int(50 * self._settings.get_ui_scaling())
        label_width = int(200 * self._settings.get_ui_scaling())
        self._vbox = VBox(pygame.Rect(-vBox_width, 0, vBox_width, vBox_height), self._manager, spacing=10,
                    anchors={'top': 'top', 'right': 'right'})
        self._phase_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, label_width, label_height), manager=self._manager, text="Phase: " + self._model.get_current_gamephase(), container=self._vbox.get_panel())
        self._vbox.add_element(self._phase_label)
        """

        self._warning_time_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, 500, 500), manager=self._manager, text="",anchors={'centerx': 'centerx', 'centery': 'centery'},object_id="#WarningTimeLabel")
        self._game_over_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, 500, 500), manager=self._manager,
                                                               text="",
                                                               anchors={'centerx': 'centerx', 'centery': 'centery'},
                                                               object_id="#WarningTimeLabel")


        self._player = AnimatedObject((model.get_player_position()[0], model.get_player_position()[1]),radius=150, color=(255,255,255))
        self._player.load_animation("RedLightGreenLight/Resources/Spritesheets/walk.png",  frame_rect=(0, 0, 300, 515),frame_count=8)

        self._player_group = pygame.sprite.Group()
        self._player_group.add(self._player)

    def get_manager(self)->pygame_gui.UIManager:
        return self._manager

    def show(self,delta_time):
        pygame.display.set_caption('Game')
        # Fill screen with color
        if self._model.is_green_light():
            self._screen.fill((0, 150, 0))
        elif self._model.is_red_light():
            self._screen.fill((150, 0, 0))

        # Draw Player
        if self._model.is_player_moving():
            self._player_group.update(delta_time, self._model.get_player_position())
        self._player_group.draw(self._screen)

        # update Labels
        # self._phase_label.set_text("Phase: " + self._model.get_current_gamephase())
        remaining_warning_time = self._model.get_remaining_warning_time()
        if remaining_warning_time:
            self._warning_time_label.set_text("Stopp in " + str(round(remaining_warning_time)))
        else:
            self._warning_time_label.set_text("")
        remaining_warning_time = self._model.get_remaining_warning_time()

        self._manager.update(delta_time)
        self._manager.draw_ui(self._screen)
        pygame.display.flip()

    def show_game_over(self):
        self._game_over_label.set_text("YOU DIED!")

    def reset_game(self):
        self._game_over_label.set_text("")

    def stop_player_animation(self):
        self._player.stop_animation()


    def hide(self):
        pass
