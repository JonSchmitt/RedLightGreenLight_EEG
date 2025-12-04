from __future__ import annotations
from abc import abstractmethod

from RedLightGreenLight.States.Game.EntityStates.DeadEntityState import DeadEntityState
from RedLightGreenLight.States.Game.EntityStates.EntityState import EntityState
from RedLightGreenLight.States.Game.EntityStates.WalkingEntityState import WalkingEntityState
from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.StateResultsEnum import ENTITY_ACTION
from RedLightGreenLight.UIElements.AnimatedObject import AnimatedObject


class Entity:
    def __init__(self, entity_id:str, entity_type:str, is_player:bool, spawn_position:tuple[int,int], size:tuple[int,int], movement_speed:int, sprite_sheets:dict[str, tuple[str, tuple[int,int,int,int], int, int]], color:tuple[int,int,int]=(255,0,0)):
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

        # State
        self._current_state:EntityState|None = None

        # Appearance if no sprite sheet is set
        self._color = color
        self._size = size

        # Animation
        self._sprite_sheets = sprite_sheets
        self._current_animation_key = None
        self._animation = AnimatedObject(spawn_position,  size, color)

    def __str__(self):
        return f"Entity({self._entity_id})"

    def initialize(self, context: GameContext):
        """Initialize Entity and register in context"""
        context.register_entity(self._entity_id, self._entity_type, self._spawn_position)
        self._current_state = self.get_initial_state()
        self._current_state.enter(self,context)
        self._sync_to_context(context)

    def update(self, action: ENTITY_ACTION, context: GameContext):
        """Update entity state machine"""
        # update state
        new_state = self._current_state.update(self,action, context)
        if new_state != self._current_state:
            self._current_state = new_state
            self._current_state.enter(self,context)

        # Synchronize context
        self._sync_to_context(context)

    def _sync_to_context(self, context: GameContext):
        """Schreibt aktuellen Status in den Context"""
        context.update_entity(
            self._entity_id,
            isinstance(self._current_state, WalkingEntityState),
            isinstance(self._current_state, DeadEntityState),
            self._position
        )

    def respawn(self,context:GameContext):
        self.set_position(self._spawn_position)
        self._current_state = self.get_initial_state()
        self._current_state.enter(self,context)
        self._sync_to_context(context)



    @abstractmethod
    def get_initial_state(self) -> EntityState:
        pass

    def is_player(self) -> bool:
        return self._is_player

    def move(self):
        self._position = (self._position[0] + self._movement_direction[0] * self._current_movement_speed, self._position[1] + self._movement_direction[1] * self._current_movement_speed)
        self._animation.set_position(self._position)

    def update_animation(self, dt:float):
        self._animation.update(dt)

    def get_current_movement_speed(self) -> int:
        return self._current_movement_speed

    def set_current_movement_speed(self, movement_speed:int):
        self._current_movement_speed = movement_speed

    def get_max_movement_speed(self) -> int:
        return self._max_movement_speed

    def set_max_movement_speed(self, max_movement_speed:int):
        self._max_movement_speed = max_movement_speed

    def get_position(self) -> tuple[int,int]:
        return self._position

    def set_position(self, position:tuple[int,int]):
        self._position = position
        self._animation.set_position(self._position)

    def get_spawn_position(self) -> tuple[int,int]:
        return self._spawn_position

    def set_spawn_position(self, spawn_position:tuple[int,int]):
        self._spawn_position = spawn_position


    def set_movement_direction(self, direction:tuple[int,int]):
        self._movement_direction = direction

    def get_movement_direction(self) -> tuple[int,int]:
        return self._movement_direction

    def get_animation(self) -> AnimatedObject:
        return self._animation

    def reset_position(self):
        self._position = self._spawn_position
        self._animation.set_position(self._position)

    def get_entity_id(self) -> str:
        return self._entity_id


    def set_animation(self, key: str, loop:bool=True):
        if key == self._current_animation_key:
            return
        if key in self._sprite_sheets:
            self._current_animation_key = key
            path, frame_rect, frame_count, grid_columns = self._sprite_sheets[key]
            self._animation.load_animation(path, frame_rect, frame_count,loop,grid_columns)
        else:
            print(f"Animation {key} not found")

