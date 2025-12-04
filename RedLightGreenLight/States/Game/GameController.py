from __future__ import annotations

from typing import List

import pygame
from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseStateFactory import GamePhaseStateFactory
from RedLightGreenLight.States.Game.GamePhaseStates.RestartState.RestartState import RestartState
from RedLightGreenLight.States.Game.GameView import GameView
from RedLightGreenLight.Resources.Sound.SoundManager import MusicManager
from RedLightGreenLight.States.SettingsSubMenu.SettingsModel import SettingsModel
from RedLightGreenLight.States.StateResultsEnum import KEY, BUT, ENTITY_ACTION
from RedLightGreenLight.States.StateResult import StateResult


class GameController:
    """Controller for the game."""
    def __init__(self, settings_model:SettingsModel, music_manager:MusicManager, game_model: GameModel, view: GameView, screen:pygame.Surface):
        self._settings = settings_model
        self._game_model = game_model
        self._view = view
        self._music_manager = music_manager
        self._screen = screen

        self._context = GameContext()
        self._game_phase = GamePhaseStateFactory.create_green_light_state(screen, settings_model, music_manager)
        self._settings.add_observer(self._game_phase)
        self._game_phase.enter(self._context)

        self._initialize_entities()



    def _initialize_entities(self):
        self._game_model.load_entities()
        for e in self._game_model.get_entities():
            e.initialize(self._context)

    def enter(self):
        self._game_phase.enter(self._context)



    def update(self,delta_time:float)->StateResult:
        result = StateResult()

        # Update game phase
        new_game_phase = self._game_phase.update(delta_time, self._context)

        # Quit Game on None return
        if self._game_phase is None:
            result.set_quit(True)
            return result

        # Switch GamePhase
        if self._game_phase and self._game_phase is not new_game_phase:
            self._game_phase = new_game_phase
            self._settings.add_observer(self._game_phase)
            self._game_phase.enter(self._context)

        # Respawn in Restart State
        if isinstance(self._game_phase, RestartState):
            self._game_model.respawn_player(self._context)

        # Update entities
        for e in self._game_model.get_entities():
            # The Action is decided in the Entity level statemachine
            e.update(ENTITY_ACTION.NONE, self._context)

        self._view.show(delta_time)

        # Return to Menu with ESC or Quit game
        self._handle_events(result)

        return result




    def _handle_keyboard_press_event(self, event)->KEY|None:
        if event.key == pygame.K_ESCAPE:
            return KEY.ESC
        else:
            return None


    def _handle_events(self,result:StateResult):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                result.add_key(self._handle_keyboard_press_event(event))
            elif event.type == pygame.QUIT:
                result.set_quit(True)

    def update_settings(self):
        self._game_model.update_settings(self._settings.is_second_player(),self._context)







