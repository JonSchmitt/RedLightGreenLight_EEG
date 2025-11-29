from __future__ import annotations

from RedLightGreenLight.States.Game.EntityStates.EntityState import EntityState
from RedLightGreenLight.States.Game.EntityStates.EntityStateFactory import EntityStateFactory
from RedLightGreenLight.States.StateResultsEnum import ENTITY_ACTION
from RedLightGreenLight.States.Game.GameContext import GameContext

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from RedLightGreenLight.States.Game.Entites.Entity import Entity
class IdleEntityState(EntityState):
    """Idle State for all Entities"""

    def enter(self, entity:Entity,context:GameContext):
        super().enter(entity,context)
        entity.set_animation("idle")

    def update(self, entity:Entity, action: ENTITY_ACTION, context:GameContext) -> EntityState:
        if action == ENTITY_ACTION.MOVE: # Try to move
            if context.is_movement_allowed(): # Check if move is possible
                if entity.is_player() and context.is_movement_kills_player(): # Check if move kills player and entity is player
                    print("Move kills player")
                    return EntityStateFactory.create_dead_state()
                else: # Move is possible and does not kill entity
                    print("Move allowed")
                    return EntityStateFactory.create_walking_state()
            else: # Move is not possible
                print("Move not allowed")
                return EntityStateFactory.create_idle_state()
        else: # Not trying to move
            return EntityStateFactory.create_idle_state()
