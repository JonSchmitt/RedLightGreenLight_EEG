from __future__ import annotations

import pygame
from RedLightGreenLight.Inputs.KeysEnum import KEY
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
from RedLightGreenLight.States.Game.GameView import GameView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.StateFactory import StateFactory


class GameController:
    """Controller for the game."""
    _MENU = "menu"
    _QUIT = "quit"
    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager, game_model: GameModel, view: GameView, screen:pygame.Surface):
        self._settings_model = settings_model
        self._game_model = game_model
        self._view = view
        self._music_manager = music_manager
        self._screen = screen

        self._game_phase = GamePhaseStateFactory.create_green_light_state(screen, settings_model, music_manager)
        self._settings_model.add_observer(self._game_phase)
        self._game_phase.enter(self._game_model)

        self._game_model.load_entities()

    def enter(self):
        self._game_phase.enter(self._game_model)



    def update(self,delta_time:float, keys_pressed:list[list[KEY]])->State:

        # Update game phase
        new_game_phase = self._game_phase.update(delta_time, self._game_model)

        # Switch GamePhase
        if self._game_phase is not new_game_phase:
            self._game_phase = new_game_phase
            self._settings_model.add_observer(self._game_phase)
            self._game_phase.enter(self._game_model)


        # Update entities
        for e in self._game_model.get_entities():
            # The Action is decided in the Entity level statemachine
            e.update(delta_time, keys_pressed)

        self._view.show(delta_time)

        return self._decide_next_state(keys_pressed)



    def _decide_next_state(self,keys_pressed:list[list[KEY]])->State:
        results = self._handle_events(keys_pressed)
        if self._QUIT in results:
            return StateFactory.create_quit_state()
        if self._MENU in results:
            return StateFactory.create_menu_state(self._view.get_screen(),self._settings_model,self._music_manager)
        return StateFactory.create_game_state(self._view.get_screen(),self._settings_model,self._music_manager)

    def _handle_keyboard_press_event(self, keys_pressed:list[list[KEY]], results:list[str])->None:
        keys_down = keys_pressed[1]
        if KEY.ESC in keys_down:
            results.append(self._MENU)


    def _handle_events(self,keys_pressed:list[list[KEY]]):
        results = []
        self._handle_keyboard_press_event(keys_pressed, results)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                results.append(self._QUIT)
        return results

    def update_settings(self):
        self._game_model.update_settings(self._settings_model.is_second_player())







