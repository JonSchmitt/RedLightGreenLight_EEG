from __future__ import annotations

from RedLightGreenLight.States.Menu.MenuModel import MenuModel
import pygame_gui
import pygame

from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.UIElements.VBox import VBox
from RedLightGreenLight.UIUtil.UIManager import UIManager


class MenuView:
    """View for the menu."""

    def __init__(self, settings_model:SettingsModel,model: MenuModel, screen:pygame.Surface):
        self._screen = screen
        self._settings = settings_model
        self._model = model

        self._manager = UIManager(self._screen)


        # create vBox:
        vBox_height = int(50 * self._settings.get_ui_scaling())
        vBox_width = int(50 * self._settings.get_ui_scaling())
        vbox = VBox(pygame.Rect(0, 0, vBox_width, vBox_height), self._manager, spacing=20,anchors={'centerx': 'centerx', 'centery': 'centery'})

        # create buttons
        button_width = int(200 * self._settings.get_ui_scaling())
        button_height = int(50 * self._settings.get_ui_scaling())
        self._ok_button = pygame_gui.elements.UIButton(pygame.Rect(0, 0, button_width, button_height), text="OK", manager=self._manager, container=vbox.get_panel())
        self._settings_button = pygame_gui.elements.UIButton(pygame.Rect(0, 0, button_width, button_height), text="Settings", manager=self._manager,container=vbox.get_panel())
        self._quit_button = pygame_gui.elements.UIButton(pygame.Rect(0, 0, button_width, button_height), text="Quit", manager=self._manager, container=vbox.get_panel())

        # add buttons to vBox
        vbox.add_element(self._ok_button)
        vbox.add_element(self._settings_button)
        vbox.add_element(self._quit_button)

    def enter(self,screen:pygame.Surface)->None:
        self._screen.blit(screen, (0, 0))

    def get_manager(self)->pygame_gui.UIManager:
        return self._manager

    def get_screen(self)->pygame.Surface:
        return self._screen

    def get_ok_button(self)->pygame_gui.elements.UIButton:
        return self._ok_button

    def get_quit_button(self)->pygame_gui.elements.UIButton:
        return self._quit_button

    def get_settings_button(self)->pygame_gui.elements.UIButton:
        return self._settings_button


    def show(self,time_delta)->None:
        pygame.display.set_caption('Menu')
        self._manager.update(time_delta)
        self._manager.draw_ui(self._screen)
        pygame.display.update()





