from __future__ import annotations
from RedLightGreenLight.States.Game.EntityStates.EntityState import EntityState
from RedLightGreenLight.States.Game.EntityStates.EntityStateFactory import EntityStateFactory
from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState
from RedLightGreenLight.States.StateResultsEnum import ENTITY_ACTION
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from RedLightGreenLight.States.Game.Entites.Entity import Entity


class WalkingEntityState(EntityState):
    """Walking State für alle Entities - Singleton"""


    def enter(self, entity:Entity, context:GameContext):
        super().enter(entity,context)
        entity.set_animation("walk")
        entity.set_movement_direction((1,0))

    def update(self, entity: Entity, action: ENTITY_ACTION, context:GameContext) -> EntityState:
        if context.is_movement_kills_player(): # while moving and moving kills
            return EntityStateFactory.create_dead_state()

        entity.move()

        if context.is_game_paused(): # while moving and game is paused
            return EntityStateFactory.create_idle_state()

        if action == ENTITY_ACTION.IDLE: # input to idle (e.g. release move key)
            return EntityStateFactory.create_idle_state()

        return EntityStateFactory.create_walking_state()
