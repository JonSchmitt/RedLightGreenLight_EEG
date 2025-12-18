from __future__ import annotations

from RedLightGreenLight.Inputs.KeysEnum import KEY
from RedLightGreenLight.States.Game.Entites.Actions import Actions
from RedLightGreenLight.States.Game.Entites.EntityModel import EntityModel
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityState import EntityState
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStateFactory import EntityStateFactory
from RedLightGreenLight.States.Game.GameModel import GameModel


class WalkingEntityState(EntityState):
    """Walking State for all Entities - Singleton"""


    def enter(self, keys_pressed:list[list[KEY]], entity_model:EntityModel, game_model:GameModel):
        super().enter(keys_pressed,entity_model,game_model)
        entity_model.set_movement_direction((1,0))

    def update(self, keys_pressed:list[list[KEY]], entity_model:EntityModel, game_model:GameModel) -> EntityState:
        if game_model.is_movement_kills_player(): # while moving and moving kills
            return EntityStateFactory.create_dead_state()

        if game_model.is_game_paused(): # while moving and game is paused
            return EntityStateFactory.create_idle_state()

        entity_model.move()
        action = self._get_action(keys_pressed, entity_model.get_entity_id())
        if action == Actions.IDLE:
            return EntityStateFactory.create_idle_state()
        return EntityStateFactory.create_walking_state()

    def _get_action(self, keys_presssed:list[list[KEY]], entity_id: str):
        keys_held = keys_presssed[0]
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
