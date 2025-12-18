from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStatesEnum import EntityStatesEnum
from RedLightGreenLight.States.Game.Entites.EntityTypesEnum import EntityTypesEnum


class EntityModel:
    """
    Model for an Entity.
    Stores identity, location, size, speed, and state.
    """
    def __init__(self, entity_id:str, entity_type:EntityTypesEnum, is_player:bool, spawn_position:tuple[int,int], size:tuple[int,int], movement_speed:int, state:EntityStatesEnum):
        # Identity
        self._is_player = is_player
        self._entity_id = entity_id
        self._entity_type = entity_type

        # Location and speed
        self._spawn_position = spawn_position
        self._position = spawn_position
        self._current_movement_speed = movement_speed
        self._max_movement_speed = movement_speed
        self._movement_direction = (0,0)

        self._size = size

        self._state:EntityStatesEnum = state
        self._is_dead = False


    def is_player(self) -> bool:
        return self._is_player

    def move(self):
        self._position = (self._position[0] + self._movement_direction[0] * self._current_movement_speed, self._position[1] + self._movement_direction[1] * self._current_movement_speed)

    def get_current_movement_speed(self) -> int:
        return self._current_movement_speed

    def set_current_movement_speed(self, movement_speed: int):
        self._current_movement_speed = movement_speed

    def get_max_movement_speed(self) -> int:
        return self._max_movement_speed

    def set_max_movement_speed(self, max_movement_speed: int):
        self._max_movement_speed = max_movement_speed

    def get_position(self) -> tuple[int, int]:
        return self._position

    def set_position(self, position: tuple[int, int]):
        self._position = position

    def get_spawn_position(self) -> tuple[int, int]:
        return self._spawn_position

    def set_spawn_position(self, spawn_position: tuple[int, int]):
        self._spawn_position = spawn_position

    def set_movement_direction(self, direction: tuple[int, int]):
        self._movement_direction = direction

    def get_movement_direction(self) -> tuple[int, int]:
        return self._movement_direction



    def reset_position(self):
        self._position = self._spawn_position

    def get_entity_id(self) -> str:
        return self._entity_id

    def get_size(self) -> tuple[int, int]:
        return self._size

    def get_state(self) -> EntityStatesEnum:
        return self._state

    def set_state(self, state:EntityStatesEnum):
        self._state = state
        if state == EntityStatesEnum.DEAD:
            self._is_dead = True

    def get_entity_type(self) -> EntityTypesEnum:
        return self._entity_type

    def is_dead(self) -> bool:
        return self._is_dead

    def set_dead(self, is_dead: bool):
        self._is_dead = is_dead