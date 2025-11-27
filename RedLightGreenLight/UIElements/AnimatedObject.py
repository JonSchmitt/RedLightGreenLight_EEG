import os.path

from RedLightGreenLight.UIUtil.SpriteSheet import SpriteSheet
import pygame


class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self, pos:tuple[int,int], size:tuple[int,int], color=(255, 0, 0)):
        super().__init__()
        self._size = size
        self._color = color
        self._visible = True

        self._image = pygame.Surface((size[0] * 2, size[1] * 2), pygame.SRCALPHA)
        pygame.draw.rect(self._image, color, pygame.Rect(0, 0, size[0] - 1, size[1] - 1))
        self._rect = self._image.get_rect(center=pos)

        # Animation
        self._frames = None
        self._frame_index = 0
        self._frame_speed = 0.12
        self._time = 0



    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    def load_animation(self, spritesheet_path:str, frame_rect:tuple[int,int,int,int], frame_count:int):
        """Lädt Animation aus SpriteSheet und skaliert sie proportional auf Kreisgröße"""
        if not os.path.isfile(spritesheet_path):
            print(f"Spritesheet nicht gefunden: {spritesheet_path}")
            return

        sheet = SpriteSheet(spritesheet_path)
        raw_frames = sheet.get_strip(
            frame_rect[0], frame_rect[1],
            frame_rect[2], frame_rect[3],
            frame_count
        )

        self._frames = []
        max_width, max_height = self._size

        for f in raw_frames:
            orig_width, orig_height = f.get_size()
            scale_factor = min(max_width / orig_width, max_height / orig_height)
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)
            scaled_frame = pygame.transform.smoothscale(f, (new_width, new_height))
            self._frames.append(scaled_frame)

        self._frame_index = 0
        self._image = self._frames[0]
        self._rect = self._image.get_rect(center=self._rect.center)

    def set_position(self, pos:tuple[int,int]):
        self._rect.center = pos

    def set_visible(self, visible:bool):
        self._visible = visible

    def is_visible(self):
        return self._visible

    def update(self, dt:float, pos:tuple[int,int]=None):
        """Animation abspielen, falls geladen"""
        if self._frames:
            self._time += dt
            if self._time >= self._frame_speed:
                self._time = 0
                self._frame_index = (self._frame_index + 1) % len(self._frames)
                self._image = self._frames[self._frame_index]
                self._rect = self._image.get_rect(center=self._rect.center)
