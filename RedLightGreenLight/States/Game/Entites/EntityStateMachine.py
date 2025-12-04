from __future__ import annotations

import pygame

from RedLightGreenLight.Inputs.KeysEnum import KEY
from RedLightGreenLight.States.Game.Entites.EntityModel import EntityModel
from RedLightGreenLight.States.Game.Entites.EntityTypesEnum import EntityTypesEnum
from RedLightGreenLight.States.Game.Entites.EntityView import EntityView
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityState import EntityState
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStateFactory import EntityStateFactory
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStatesEnum import EntityStatesEnum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from RedLightGreenLight.States.Game.GameModel import GameModel


class EntityStateMachine:
    """ The Entity's state machine"""
    def __init__(self, game_model:GameModel, entity_id:str, entity_type:EntityTypesEnum, is_player:bool, spawn_position:tuple[int,int], size:tuple[int,int], movement_speed:int, sprite_sheets:dict[EntityStatesEnum, tuple[str, tuple[int,int,int,int], int, int]], screen:pygame.Surface,color:tuple[int,int,int]=(255,0,0)):
        self._game_model = game_model
        self._entity_model = EntityModel(entity_id,entity_type,is_player,spawn_position,size,movement_speed,EntityStatesEnum.IDLE)
        self._entity_view = EntityView(self._entity_model,screen,sprite_sheets,color)
        self._current_state:EntityState|None = EntityStateFactory.create_idle_state()


    def update(self, delta_time:float, keys_pressed:list[KEY]):
        new_state = self._current_state.update(keys_pressed,self._entity_model,self._game_model)
        if new_state is not self._current_state:
            self._current_state = new_state
            self._current_state.enter(keys_pressed,self._entity_model,self._game_model)

        self._entity_view.show(delta_time)

    def get_entity_model(self)->EntityModel:
        return self._entity_model

