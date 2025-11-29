import pygame

from RedLightGreenLight.States.Game.Entites import EntityTypes
from RedLightGreenLight.States.Game.Entites.Entity import Entity
from RedLightGreenLight.States.Game.EntityStates.EntityState import EntityState
from RedLightGreenLight.States.Game.EntityStates.EntityStateFactory import EntityStateFactory
from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.StateResultsEnum import ENTITY_ACTION


class Player(Entity):
    def __init__(self, entity_id:str,spawn_position:tuple[int,int], size:tuple[int,int], movement_speed:int, sprite_sheets:dict[str, tuple[str, tuple[int,int,int,int], int]], color:tuple[int,int,int]=(255,0,0)):
        super().__init__(entity_id,EntityTypes.Player,True,spawn_position, size, movement_speed, sprite_sheets, color)



    def get_initial_state(self) -> EntityState:
        return EntityStateFactory.create_idle_state()

    def update(self, action: ENTITY_ACTION, context: GameContext):
        if self._entity_id == "Player_1":
            self._handle_player_1(context)
        elif self._entity_id == "Player_2":
            self._handle_player_2(context)

        else:
            print(f"[Player] Unknown player: {self._entity_id}")

    def _handle_player_1(self,context):
        keys = pygame.key.get_pressed()
        action = ENTITY_ACTION.NONE
        if keys[pygame.K_SPACE]:
            action = ENTITY_ACTION.MOVE
        else:
            action = ENTITY_ACTION.IDLE

        super().update(action, context)

    def _handle_player_2(self,context):
        keys = pygame.key.get_pressed()
        action = ENTITY_ACTION.NONE

        if keys[pygame.K_RIGHT]:
            action = ENTITY_ACTION.MOVE
        else:
            action = ENTITY_ACTION.IDLE

        super().update(action, context)