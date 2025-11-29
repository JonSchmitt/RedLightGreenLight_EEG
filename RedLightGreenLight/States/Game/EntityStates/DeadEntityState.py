from __future__ import annotations

from RedLightGreenLight.States.Game.EntityStates.EntityState import EntityState
from RedLightGreenLight.States.Game.EntityStates.EntityStateFactory import EntityStateFactory
from RedLightGreenLight.States.StateResultsEnum import ENTITY_ACTION
from RedLightGreenLight.States.Game.GameContext import GameContext
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from RedLightGreenLight.States.Game.Entites.Entity import Entity

class DeadEntityState(EntityState):
    """Dead State for all Entities"""

    def enter(self, entity:Entity,context:GameContext):
        super().enter(entity,context)
        entity.set_animation("dead",loop=False)

    def update(self, entity:Entity, action: ENTITY_ACTION, context:GameContext) -> EntityState:
        if action == ENTITY_ACTION.SPAWN:
            return EntityStateFactory.create_idle_state()
        return EntityStateFactory.create_dead_state()