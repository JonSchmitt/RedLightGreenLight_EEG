from __future__ import annotations

import pygame
import pygame_gui

from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.UIElements.VBox import VBox
from RedLightGreenLight.UIUtil.UIManager import UIManager


class GameView:
    """View for the game."""
    def __init__(self,settings_model:SettingsModel, model:GameModel, screen:pygame.Surface):
        self._screen = screen
        self._settings = settings_model
        self._model = model
        self._manager = UIManager(self._screen)

        #
        #
        # vBox_height = int(100 * self._settings.get_ui_scaling())
        # vBox_width = int(150 * self._settings.get_ui_scaling())
        # label_height = int(50 * self._settings.get_ui_scaling())
        # label_width = int(200 * self._settings.get_ui_scaling())
        # self._vbox = VBox(pygame.Rect(-vBox_width, 0, vBox_width, vBox_height), self._manager, spacing=10,
        #             anchors={'top': 'top', 'right': 'right'})
        # self._phase_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, label_width, label_height), manager=self._manager, text="T: " + str(round(self._model.get_remaining_in_phase_time())), container=self._vbox.get_panel())
        # self._vbox.add_element(self._phase_label)
        #
        #
        # self._warning_time_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, 500, 500), manager=self._manager, text="",anchors={'centerx': 'centerx', 'centery': 'centery'},object_id="#WarningTimeLabel")
        # self._game_over_label = pygame_gui.elements.UILabel(pygame.Rect(0, 0, 500, 500), manager=self._manager,
        #                                                        text="",
        #                                                        anchors={'centerx': 'centerx', 'centery': 'centery'},
        #                                                        object_id="#WarningTimeLabel")




    def show(self,delta_time):
        for e in self._model.get_entities():
            e.update_animation(delta_time)
            if e.get_animation().is_visible():
                self._screen.blit(e.get_animation().image, e.get_animation().rect)

        self._manager.update(delta_time)
        self._manager.draw_ui(self._screen)
        pygame.display.flip()


    def hide(self):
        pass
