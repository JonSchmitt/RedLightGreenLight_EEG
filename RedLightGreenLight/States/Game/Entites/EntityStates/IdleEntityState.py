from __future__ import annotations

from RedLightGreenLight.Inputs.KeysEnum import KEY
from RedLightGreenLight.States.Game.Entites.EntityModel import EntityModel
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityState import EntityState
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStateFactory import EntityStateFactory
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStatesEnum import EntityStatesEnum
from RedLightGreenLight.States.Game.GameModel import GameModel
from RedLightGreenLight.States.Game.Entites.Actions import Actions
class IdleEntityState(EntityState):
    """Idle State for all Entities"""
    def enter(self, keys_pressed:list[list[KEY]], entity_model:EntityModel, game_model:GameModel):
        super().enter(keys_pressed, entity_model, game_model)
        entity_model.set_state(EntityStatesEnum.IDLE)

    def update(self, keys_pressed:list[list[KEY]], entity_model:EntityModel, game_model:GameModel) -> EntityState:
        if self._get_action(keys_pressed, entity_model.get_entity_id()) == Actions.MOVE: # Try to move
            if game_model.is_movement_allowed(): # Check if move is possible
                if entity_model.is_player() and game_model.is_movement_kills_player(): # Check if move kills player and entity is player
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

    def _get_action(self, keys_presed:list[list[KEY]], entity_id:str):
        keys_held = keys_presed[0]
        if entity_id == "Player_1":
            if KEY.SPACE in keys_held:
                return Actions.MOVE
            else:
                return Actions.IDLE
        elif entity_id == "Player_2":
            if KEY.RIGHT in keys_held:
                return Actions.MOVE
            else:
                return Actions.IDLE

        else:
            return Actions.NONE
