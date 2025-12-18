import pygame

from RedLightGreenLight.States.Game.Entites.EntityModel import EntityModel
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStatesEnum import EntityStatesEnum
from RedLightGreenLight.UIElements.AnimatedObject import AnimatedObject


class EntityView:
    """
    View for an Entity.
    Handles animations and drawing.
    """
    def __init__(self,model:EntityModel,screen:pygame.Surface,sprite_sheets:dict[EntityStatesEnum, tuple[str, tuple[int,int,int,int], int, int]], color:tuple[int,int,int]=(255,0,0)):
        self._model = model
        self._screen = screen

        # Animation
        self._sprite_sheets = sprite_sheets
        self._current_animation_key = None
        self._animation = AnimatedObject(model.get_spawn_position(), model.get_size(), color)


    def _set_animation(self, key: EntityStatesEnum, loop: bool = True):
        if key == self._current_animation_key:
            return
        if key in self._sprite_sheets:
            self._current_animation_key = key
            path, frame_rect, frame_count, grid_columns = self._sprite_sheets[key]
            self._animation.load_animation(path, frame_rect, frame_count, loop, grid_columns)
        else:
            print(f"Animation {key} not found")

    def show(self, delta_time:float):
        state = self._model.get_state()
        loop = state != EntityStatesEnum.DEAD
        self._set_animation(state,loop)
        self._animation.set_position(self._model.get_position())
        self._animation.update(delta_time)
        if self._animation.is_visible():
            self._screen.blit(self._animation.image, self._animation.rect)