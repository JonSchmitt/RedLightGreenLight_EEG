from __future__ import annotations

from queue import Queue
import pygame_gui

from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.SettingsSubMenu.SettingsView import SettingsView
import pygame
from RedLightGreenLight.States.StateKeywords import StateKeywords as skw
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel

class SettingsController:
    """Controller for the settings-menu."""
    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager, view: SettingsView, state_events:Queue):
        self._settings = settings_model
        self._view = view
        self._state_events = state_events # Callback function to exit the menu
        self._music_manager = music_manager

    def handle_events(self,events:pygame.event):
        """Handles all events for the settings-menu."""
        for event in events:
            self._view.get_manager().process_events(event)
            if event.type == pygame.KEYDOWN:
                self._handle_keyboard_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self._handle_button_events(event)
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                self._handle_slider_events(event)
            if event.type == pygame_gui.UI_CHECK_BOX_CHECKED or event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                self._handle_checkbox_events(event)

    def update(self,delta_time):
        self._view.show(delta_time)
        if self._settings.is_music() and self._view.get_music_checkbox().get_state():
            self._music_manager.play(SoundPaths.MENU_MUSIC)



    def _handle_keyboard_events(self, event):
        """Handles a single keyboard event."""
        if event.key == pygame.K_ESCAPE:
            self._on_esc_pressed()

    def _handle_button_events(self, event):
        """Handles a single button event."""
        if event.ui_element == self._view.get_ok_button():
            self._on_ok_pressed()

    def _handle_slider_events(self, event):
        """Handles a single slider event."""
        if event.ui_element == self._view.get_switch_time_slider().get_slider():
            self._view.get_switch_time_slider().on_slider_changed(event)
        elif event.ui_element == self._view.get_warning_time_slider().get_slider():
            self._view.get_warning_time_slider().on_slider_changed(event)

    def _handle_checkbox_events(self, event):
        """Handles a single checkbox event."""
        if event.ui_element == self._view.get_music_checkbox():
            if self._view.get_music_checkbox().get_state():
                self._music_manager.play(SoundPaths.MENU_MUSIC)
            else:
                self._music_manager.stop()

    def _on_ok_pressed(self):
        self._update_settings()
        self._state_events.put(skw.SETTINGS_OK)

    def _on_esc_pressed(self):
        self._view.reset_changes()
        if not self._settings.is_music():
            self._music_manager.stop()
        self._state_events.put(skw.SETTINGS_ESC)
        # don't update settings on esc press

    def _update_settings(self):
        changed = False
        switch_time_new = int(self._view.get_switch_time_slider().get_value())
        warning_time_new = int(self._view.get_warning_time_slider().get_value())
        music_new = self._view.get_music_checkbox().get_state()
        if switch_time_new != self._settings.get_switch_time():
            self._settings.set_switch_time(switch_time_new)
            changed = True
        if warning_time_new != self._settings.get_warning_time():
            self._settings.set_warning_time(warning_time_new)
            changed = True
        if music_new != self._settings.is_music():
            self._settings.set_music(music_new)
            changed = True

        if changed:
            self._settings.set_settings_changed(True)

