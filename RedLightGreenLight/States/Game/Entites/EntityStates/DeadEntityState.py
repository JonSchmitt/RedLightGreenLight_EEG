from __future__ import annotations

from RedLightGreenLight.Inputs.KeysEnum import KEY
from RedLightGreenLight.States.Game.Entites import EntityModel
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityState import EntityState
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStateFactory import EntityStateFactory
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStatesEnum import EntityStatesEnum
from RedLightGreenLight.States.Game.GameModel import GameModel


class DeadEntityState(EntityState):
    """Dead State for all Entities"""

    def enter(self, keys_pressed:list[list[KEY]], entity_model:EntityModel, game_model:GameModel):
        super().enter(keys_pressed,entity_model,game_model)
        entity_model.set_state(EntityStatesEnum.DEAD)


    def update(self, keys_pressed:list[list[KEY]], entity_model:EntityModel, game_model:GameModel) -> EntityState:
        if not entity_model.is_dead():
            return EntityStateFactory.create_idle_state()
        return EntityStateFactory.create_dead_state()