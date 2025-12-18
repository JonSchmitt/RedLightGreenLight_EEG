from __future__ import annotations

import pygame

from RedLightGreenLight.Resources.Spritesheets import SpriteSheetStruct
from RedLightGreenLight.States.Game.Entites.EntityTypesEnum import EntityTypesEnum
from RedLightGreenLight.States.Game.Entites.EntityStateMachine import EntityStateMachine
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhasesEnum import GamePhasesEnum


class GameModel:
    """
    Model for the game.
    Manages the game state, entities (players), phase information,
    and rules (e.g., movement allowed/forbidden).
    """
    def __init__(self, second_player: bool, screen: pygame.Surface):
        self._screen = screen

        # Entities
        self._entities: list[EntityStateMachine] = []
        self._second_player = second_player

        # Phase-Info
        self._is_movement_allowed = False
        self._is_movement_kills_player = False
        self._is_game_paused = False
        self._is_game_over = False

    def load_entities(self):
        self._entities = []
        self._entities.append(
            EntityStateMachine(self, "Player_1", EntityTypesEnum.PLAYER, True, (100, 720), (200, 500), 1,
                               SpriteSheetStruct.PlayerEntity, self._screen))
        if self._second_player:
            self._entities.append(
                EntityStateMachine(self, "Player_2", EntityTypesEnum.PLAYER, True, (100, 320), (200, 500), 1,
                                   SpriteSheetStruct.PlayerEntity, self._screen))
    def get_entities(self):
        return self._entities

    def update_settings(self, second_player: bool):
        if second_player is not self._second_player:
            if not second_player:
                self._entities.remove(self._entities[1])
            else:
                new_entity = EntityStateMachine(self, "Player_2", EntityTypesEnum.PLAYER, True, (100, 320), (200, 500),
                                                1,
                                                SpriteSheetStruct.PlayerEntity, self._screen)
                self._entities.append(new_entity)
        self._second_player = second_player

    def get_all_players_dead(self):
        for e in self._entities:
            e_model = e.get_entity_model()
            if e_model.get_entity_type() == EntityTypesEnum.PLAYER:
                if not e_model.is_dead():
                    return False
        return True

    def restart_game(self):
        for e in self._entities:
            e_model = e.get_entity_model()
            if e_model.get_entity_type() == EntityTypesEnum.PLAYER: # Respawn Player(s)
                e_model.reset_position()
                e_model.set_dead(False)


    def update_phase_info(self, game_state_phase: GamePhasesEnum):
        if game_state_phase == GamePhasesEnum.RLS:
            self._is_movement_allowed = True
            self._is_movement_kills_player = True
            self._is_game_paused = False
            self._is_game_over = False
        elif game_state_phase == GamePhasesEnum.GLS:
            self._is_movement_allowed = True
            self._is_movement_kills_player = False
            self._is_game_paused = False
            self._is_game_over = False
        elif game_state_phase == GamePhasesEnum.GOS:
            self._is_movement_allowed = False
            self._is_movement_kills_player = False
            self._is_game_paused = False
            self._is_game_over = True
        elif game_state_phase == GamePhasesEnum.RES:
            self._is_movement_allowed = False
            self._is_movement_kills_player = False
            self._is_game_paused = True
            self._is_game_over = False
        elif game_state_phase == GamePhasesEnum.PAU:
            self._is_movement_allowed = False
            self._is_movement_kills_player = False
            self._is_game_paused = True
            self._is_game_over = False

    def is_movement_allowed(self) -> bool:
        return self._is_movement_allowed

    def is_movement_kills_player(self) -> bool:
        return self._is_movement_kills_player

    def is_game_paused(self) -> bool:
        return self._is_game_paused

    def is_game_over(self) -> bool:
        return self._is_game_over
