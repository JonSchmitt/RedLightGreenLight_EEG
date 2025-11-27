from __future__ import annotations

import os

import pygame
import pygame_gui

from RedLightGreenLight.Game.Entity import Entity
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



        vBox_height = int(100 * self._settings.get_ui_scaling())
        vBox_width = int(150 * self._settings.get_ui_scaling())
        label_height = int(50 * self._settings.get_ui_scaling())
        label_width = int(200 * self._settings.get_ui_scaling())
        self._vbox = VBox(pygame.Rect(-vBox_width, 0, vBox_width, vBox_height), self._manager, spacing=10,
                    anchors={'top': 'top', 'right': 'right'})
        self._phase_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, label_width, label_height), manager=self._manager, text="T: " + str(round(self._model.get_remaining_in_phase_time())), container=self._vbox.get_panel())
        self._vbox.add_element(self._phase_label)


        self._warning_time_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, 500, 500), manager=self._manager, text="",anchors={'centerx': 'centerx', 'centery': 'centery'},object_id="#WarningTimeLabel")
        self._game_over_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, 500, 500), manager=self._manager,
                                                               text="",
                                                               anchors={'centerx': 'centerx', 'centery': 'centery'},
                                                               object_id="#WarningTimeLabel")




    def show(self,delta_time, time_stamp):
        pygame.display.set_caption('Game')
        # Fill screen with color
        self._draw_background()

        if self._model.is_player_dead(time_stamp):
            self._model.get_player().play_animation("dead")
        elif self._model.is_player_moving():
            self._model.get_player().play_animation("walk")
        else:
            self._model.get_player().play_animation("idle")

        # update and draw entities
        for e in self._model.get_entities():
            e.update(delta_time)
            if e.get_animation().is_visible():
                self._screen.blit(e.get_animation().image, e.get_animation().rect)



        # update Labels
        self._draw_labels()

        # draw game_over
        self._show_game_over_label(time_stamp)

        self._manager.update(delta_time)
        self._manager.draw_ui(self._screen)
        pygame.display.flip()

    def _draw_background(self):
        if self._model.is_green_light():
            self._screen.fill((0, 150, 0))
        elif self._model.is_red_light():
            self._screen.fill((150, 0, 0))

    def _draw_labels(self):
        self._phase_label.set_text("T: " + str(round(self._model.get_remaining_in_phase_time())))
        remaining_warning_time = self._model.get_remaining_warning_time()
        if remaining_warning_time:
            self._warning_time_label.set_text("Stopp in " + str(round(remaining_warning_time)))
        else:
            self._warning_time_label.set_text("")

    def _show_game_over_label(self, dt):
        if not self._model.is_game_over():
            self._game_over_label.hide()
            return

        dt_blinking = 1 # the time difference before game_over ends to hide the label

        elapsed = self._model.get_game_over_elapsed_time(dt)
        total_duration = self._model.get_game_over_duration()
        start_interval = 0.3
        end_interval = 0.1
        progress = min(elapsed / total_duration, 1.0)  # 0..1
        blink_interval = start_interval + (end_interval - start_interval) * progress
        visible = int(elapsed / blink_interval) % 2 == 0 and total_duration - elapsed > dt_blinking
        if visible:
            self._game_over_label.set_text("YOU DIED!!!")
            self._game_over_label.show()
            self._model.get_player().get_animation().set_visible(False)
        else:
            self._game_over_label.hide()
            self._model.get_player().get_animation().set_visible(True)

    def _animate_player_respawn(self, dt):
        if not self._model.is_game_over():
            self._model.get_player().get_animation().set_visible(True)
            return

        elapsed = self._model.get_game_over_elapsed_time(dt)
        total_duration = self._model.get_game_over_duration()
        start_interval = 0.3
        end_interval = 0.1
        progress = min(elapsed / total_duration, 1.0)  # 0..1
        blink_interval = start_interval + (end_interval - start_interval) * progress
        invisible = int(elapsed / blink_interval) % 2 == 0
        if invisible:
            self._model.get_player().get_animation().set_visible(False)
        else:
            self._model.get_player().get_animation().set_visible(True)
            if total_duration - elapsed <= 1:
                pass
                self._model.get_player().reset_position()



    def hide(self):
        pass
