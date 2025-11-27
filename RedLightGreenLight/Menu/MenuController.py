from __future__ import annotations

from queue import Queue
import pygame_gui
from RedLightGreenLight.Menu.MenuView import MenuView
from RedLightGreenLight.Menu.MenuModel import MenuModel
import pygame

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.States.StateKeywords import StateKeywords as skw
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel


class MenuController:
    """Controller for the menu."""
    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager,model: MenuModel, view: MenuView, state_events:Queue):
        self._settings = settings_model
        self._model = model
        self._view = view
        self._state_events = state_events # Callback function to exit the menu
        self._music_manager = music_manager

    def handle_events(self,events:pygame.event):
        """Handles all events for the menu."""
        for event in events:
            self._view.get_manager().process_events(event)
            if event.type == pygame.KEYDOWN:
                self._handle_keyboard_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_events(event)

    def update(self,delta_time):
        self._view.show(delta_time)
        if self._settings.is_music():
            self._music_manager.play(SoundPaths.MENU_MUSIC)


    def _handle_keyboard_events(self, event):
        """Handles a single keyboard event."""
        if event.key == pygame.K_ESCAPE:
            self._on_esc_pressed()

    def _handle_button_events(self, event):
        """Handles a single button event."""
        if event.ui_element == self._view.get_ok_button():
            self._on_ok_pressed()
        elif event.ui_element == self._view.get_quit_button():
            self._on_quit_pressed()
        elif event.ui_element == self._view.get_settings_button():
            self._on_settings_pressed()

    def _on_ok_pressed(self):
        self._state_events.put(skw.MENU_OK)

    def _on_esc_pressed(self):
        self._state_events.put(skw.MENU_ESC)

    def _on_quit_pressed(self):
        self._state_events.put(skw.GAME_QUIT)

    def _on_settings_pressed(self):
        self._state_events.put(skw.MENU_SETTINGS)

    def update_settings(self):
        pass
    #TODO: implement update_settings method
