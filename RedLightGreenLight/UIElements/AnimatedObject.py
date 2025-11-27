import os.path

from RedLightGreenLight.UIUtil.SpriteSheet import SpriteSheet
import pygame


class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self, pos, radius, color=(255,0,0)):
        super().__init__()
        self.radius = radius
        self.color = color

        # Anfangs Kreis
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=pos)

        # Animation
        self.frames = None
        self.frame_index = 0
        self.frame_speed = 0.12  # kannst du ändern
        self.time = 0

    def load_animation(self, spritesheet_path, frame_rect, frame_count):
        """Lädt Animation aus SpriteSheet und skaliert sie proportional auf Kreisgröße"""
        if not os.path.isfile(spritesheet_path):
            raise FileNotFoundError(f"Spritesheet nicht gefunden: {spritesheet_path}")

        sheet = SpriteSheet(spritesheet_path)
        raw_frames = sheet.get_strip(
            frame_rect[0], frame_rect[1],
            frame_rect[2], frame_rect[3],
            frame_count
        )

        self.frames = []
        max_size = self.radius * 2

        for f in raw_frames:
            orig_width, orig_height = f.get_size()
            scale_factor = min(max_size / orig_width, max_size / orig_height)
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)
            scaled_frame = pygame.transform.smoothscale(f, (new_width, new_height))
            self.frames.append(scaled_frame)

        self.frame_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt, pos=None):
        """Animation abspielen, falls geladen"""
        if self.frames:
            self.time += dt
            if self.time >= self.frame_speed:
                self.time = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(center=self.rect.center)
        if pos:
            self.rect.center = pos