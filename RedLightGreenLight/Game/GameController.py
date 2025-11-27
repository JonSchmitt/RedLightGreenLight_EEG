from __future__ import annotations
from queue import Queue

import pygame

from RedLightGreenLight.Game.GameModel import GameModel
from RedLightGreenLight.Game.GameView import GameView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateKeywords import StateKeywords as skw


class GameController:
    """Controller for the game."""
    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager, model: GameModel, view: GameView,state_events:Queue):
        self._settings = settings_model
        self._model = model
        self._view = view
        self._state_events = state_events
        self._music_manager = music_manager


    def update(self,delta_time:float):
        self._view.show(delta_time)
        self._model.update_time(delta_time)
        self._check_movement()
        self._update_music()


    def _check_movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if not self._model.is_pause():
                self._model.set_player_moving(True)
                if not self._model.is_red_light():
                    self._model.move_player(1, 0)
                else:
                    self._view.show_game_over()
                    self._model.restart_game()
        else:
            self._model.set_player_moving(False)

    def _update_music(self):
        if self._settings.is_music():
            if self._model.get_remaining_in_phase_time() < 1:
                self._music_manager.fade_out(1)
            if self._model.get_current_gamephase() == "GreenLight":
                self._music_manager.play(SoundPaths.GREEN_LIGHT)
            elif self._model.get_current_gamephase() == "RedLight":
                self._music_manager.play(SoundPaths.RED_LIGHT)


    def _handle_keyboard_press_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self._state_events.put(skw.GAME_ESC)




    def handle_events(self,events:pygame.event):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._handle_keyboard_press_event(event)

    def update_settings(self):
        if self._settings.is_settings_changed():
            self._model.update_settings(self._settings.get_switch_time(), self._settings.get_warning_time())
            # update the game settings with the current model settings

