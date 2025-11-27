from __future__ import annotations
from queue import Queue

import pygame

from RedLightGreenLight.Game.GameModel import GameModel
from RedLightGreenLight.Game.GameView import GameView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.Resources.Sound.SoundPaths import SoundPaths
from RedLightGreenLight.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateKeywords import StateKeywords as skw
from RedLightGreenLight.States.StateResult import StateResult


class GameController:
    """Controller for the game."""
    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager, model: GameModel, view: GameView):
        self._settings = settings_model
        self._model = model
        self._view = view
        self._music_manager = music_manager


    def update(self,delta_time:float)->StateResult:
        result = StateResult()
        time_stamp = pygame.time.get_ticks()/1000
        self._model.update_time(delta_time)
        self._model.evaluate_game_over(time_stamp)
        self._view.show(delta_time,time_stamp)
        self._handle_events(result)
        self._check_movement(time_stamp)
        self._model.move_entities()
        self._update_music()

        return result


    def _check_movement(self,time_stamp):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if not self._model.is_pause() and not self._model.is_game_over():
                if not self._model.is_red_light():
                    self._model.set_player_moving((1, 0))
                else:
                    self._on_game_over(time_stamp)
            else:
                self._model.set_player_moving((0, 0))

        else:
            self._model.set_player_moving((0, 0))

    def _update_music(self):
        if self._settings.is_music():
            if not self._model.is_game_over():
                if self._model.get_current_gamephase() == "GreenLight":
                    self._music_manager.play(SoundPaths.GREEN_LIGHT)
                elif self._model.get_current_gamephase() == "RedLight":
                    self._music_manager.play(SoundPaths.RED_LIGHT)

                if self._model.get_remaining_in_phase_time() < 1:
                    self._music_manager.fade_out(1)


    def _handle_keyboard_press_event(self, event)->str|None:
        if event.key == pygame.K_ESCAPE:
            return skw.GAME_ESC
        else:
            return None


    def _handle_events(self,result:StateResult):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                result.add_key(self._handle_keyboard_press_event(event))
            elif event.type == pygame.QUIT:
                result.set_quit(True)

    def update_settings(self):
        self._model.update_settings(self._settings.get_switch_time(), self._settings.get_warning_time())

    def _on_game_over(self,time_stamp):
        self._music_manager.stop()
        self._music_manager.play(SoundPaths.GAME_OVER, False)
        self._model.start_game_over(time_stamp)





