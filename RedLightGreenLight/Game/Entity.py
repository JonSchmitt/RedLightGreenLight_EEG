from RedLightGreenLight.UIElements.AnimatedObject import AnimatedObject


class Entity:
    def __init__(self, is_player:bool, spawn_position:tuple[int,int], size:tuple[int,int], movement_speed:int, sprite_sheets:dict[str, tuple[str, tuple[int,int,int,int], int]], color:tuple[int,int,int]=(255,0,0)):
        self._spawn_position = spawn_position
        self._current_movement_speed = movement_speed
        self._max_movement_speed = movement_speed
        self._sprite_sheets = sprite_sheets
        self._current_animation_key = None
        self._position = spawn_position
        self._color = color
        self._size = size
        self._is_player = is_player
        self._animation = AnimatedObject(spawn_position,  size, color)
        if "idle" in sprite_sheets:
            self.play_animation("idle")
        self._movement_direction = (0,0)





    def move(self):
        self._position = (self._position[0] + self._movement_direction[0] * self._current_movement_speed, self._position[1] + self._movement_direction[1] * self._current_movement_speed)
        self._animation.set_position(self._position)

    def update(self, dt:float):
        self._animation.update(dt)

    def is_player(self) -> bool:
        return self._is_player


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


    def play_animation(self, key: str):
        if key == self._current_animation_key:
            return
        if key in self._sprite_sheets:
            self._current_animation_key = key
            path, frame_rect, frame_count = self._sprite_sheets[key]
            self._animation.load_animation(path, frame_rect, frame_count)
        else:
            print(f"Animation {key} not found")

