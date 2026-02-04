from __future__ import annotations

import pygame_gui
import pygame
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from UIUtils.SliderWithLabel import SliderWithLabel
from UIUtils.VBox import VBox
from UIUtils.UIManager import UIManager


class SettingsView:
    """View for the settings menu."""

    def __init__(self, settings_model: SettingsModel, screen: pygame.Surface):
        self._screen = screen
        self._settings = settings_model
        self._manager = UIManager(self._screen)

        # create vBox:
        vBox_height = int(250 * self._settings.get_ui_scaling())
        vBox_width = int(250 * self._settings.get_ui_scaling())
        self._vbox = VBox(pygame.Rect(0, 0, vBox_width, vBox_height), self._manager, spacing=30,
                          anchors={'centerx': 'centerx', 'centery': 'centery'})

        # create buttons
        button_width = int(200 * self._settings.get_ui_scaling())
        button_height = int(50 * self._settings.get_ui_scaling())
        self._ok_button = pygame_gui.elements.UIButton(pygame.Rect(0, 0, button_width, button_height), text="OK",
                                                       manager=self._manager, container=self._vbox.get_panel())

        # create Checkboxes
        checkbox_width = int(50 * self._settings.get_ui_scaling())
        checkbox_height = checkbox_width
        self._music_checkbox = pygame_gui.elements.UICheckBox(pygame.Rect(0, 0, checkbox_width, checkbox_height),
                                                              text="Music", manager=self._manager,
                                                              container=self._vbox.get_panel())
        self._music_checkbox.set_state(self._settings.is_music())

        # create Sliders
        slider_width = int(200 * self._settings.get_ui_scaling())
        slider_height = int(50 * self._settings.get_ui_scaling())
        self._warning_time_slider = SliderWithLabel(manager=self._manager, container=self._vbox.get_panel(),
                                                    width=slider_width, height=slider_height, label_text="Warning time",
                                                    start_value=self._settings.get_warning_time(), value_range=(0, 60),
                                                    suffix="s")

        self._switch_time_slider = SliderWithLabel(manager=self._manager, container=self._vbox.get_panel(),
                                                   width=slider_width, height=slider_height, label_text="Switch time",
                                                   start_value=self._settings.get_switch_time(), value_range=(0, 60),
                                                   suffix="s")

        self._game_over_time_slider = SliderWithLabel(manager=self._manager, container=self._vbox.get_panel(),
                                                    width=slider_width, height=slider_height, label_text="Game Over Duration",
                                                    start_value=self._settings.get_game_over_duration(), value_range=(0, 25),
                                                    suffix="s")

        self._second_player_checkbox = pygame_gui.elements.UICheckBox(pygame.Rect(0, 0, checkbox_width, checkbox_height),
                                                              text="Second Player", manager=self._manager,
                                                              container=self._vbox.get_panel())
        self._second_player_checkbox.set_state(self._settings.is_second_player())

        # add buttons to vBox
        self._vbox.add_element(self._ok_button)
        self._vbox.add_element(self._music_checkbox)
        self._vbox.add_element(self._warning_time_slider.get_panel())
        self._vbox.add_element(self._switch_time_slider.get_panel())
        self._vbox.add_element(self._game_over_time_slider.get_panel())
        self._vbox.add_element(self._second_player_checkbox)

    def enter(self,screen:pygame.Surface = None):
        self._screen.blit(screen, (0, 0))

    def get_manager(self) -> pygame_gui.UIManager:
        return self._manager

    def get_ok_button(self) -> pygame_gui.elements.UIButton:
        return self._ok_button

    def get_music_checkbox(self) -> pygame_gui.elements.UICheckBox:
        return self._music_checkbox

    def get_warning_time_slider(self) -> SliderWithLabel:
        return self._warning_time_slider

    def get_switch_time_slider(self) -> SliderWithLabel:
        return self._switch_time_slider

    def get_game_over_time_slider(self) -> SliderWithLabel:
        return self._game_over_time_slider

    def get_second_player_checkbox(self) -> pygame_gui.elements.UICheckBox:
        return self._second_player_checkbox

    def get_screen(self) -> pygame.Surface:
        return self._screen

    def show(self, time_delta) -> None:
        pygame.display.set_caption('Settings')
        self._screen.fill((30, 30, 40))
        self._manager.update(time_delta)
        self._manager.draw_ui(self._screen)
        pygame.display.update()



    def reset_changes(self):
        self._switch_time_slider.set_value(self._settings.get_switch_time())
        self._warning_time_slider.set_value(self._settings.get_warning_time())
        self._music_checkbox.set_state(self._settings.is_music())
        self._game_over_time_slider.set_value(self._settings.get_game_over_duration())
        self._second_player_checkbox.set_state(self._settings.is_second_player())
