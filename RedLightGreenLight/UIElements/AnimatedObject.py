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

    def load_animation(self, spritesheet_path: str, frame_rect: tuple[int, int, int, int],
                       frame_count: int, loop: bool = True, grid_columns: int = None):
        """
        Lädt Animation aus SpriteSheet und skaliert sie proportional auf Kreisgröße

        Args:
            spritesheet_path: Pfad zum Spritesheet
            frame_rect: (x, y, width, height) des ersten Frames
            frame_count: Anzahl der Frames
            loop: Ob Animation loopen soll
            grid_columns: Anzahl Spalten im Grid (None = horizontale Strip)
        """
        if not os.path.isfile(spritesheet_path):
            print(f"Spritesheet nicht gefunden: {spritesheet_path}")
            return

        self._visible = True

        self._loop = loop
        self._frames = []

        x, y, frame_width, frame_height = frame_rect

        # Extrahiere Frames aus Grid oder Strip
        if grid_columns is None:
            # Horizontaler Strip (alte Methode mit SpriteSheet-Klasse)
            sheet = SpriteSheet(spritesheet_path)
            raw_frames = sheet.get_strip(x, y, frame_width, frame_height, frame_count)
        else:
            # Grid Layout - lade Spritesheet direkt
            spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
            raw_frames = []

            for i in range(frame_count):
                col = i % grid_columns
                row = i // grid_columns
                frame_x = x + col * frame_width
                frame_y = y + row * frame_height

                # Extrahiere Frame mit subsurface
                frame_rect = pygame.Rect(frame_x, frame_y, frame_width, frame_height)
                frame = spritesheet.subsurface(frame_rect).copy()
                raw_frames.append(frame)

        # Skalierung (wie vorher)
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

    def animation_finished(self):
        return not self._loop and self._frame_index == len(self._frames) - 1

    def update(self, dt:float):
        """Animation abspielen, falls geladen"""
        if self._frames:
            self._time += dt
            if self._time >= self._frame_speed:
                self._time = 0
                self._frame_index = (self._frame_index + 1) % len(self._frames)
                if not self.animation_finished():
                    self._image = self._frames[self._frame_index]
                    self._rect = self._image.get_rect(center=self._rect.center)
                else:
                    self.set_visible(False)
