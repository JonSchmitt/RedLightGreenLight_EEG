import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_frame(self, frame_rect):
        """frame_rect = (x, y, width, height)"""
        frame = pygame.Surface((frame_rect[2], frame_rect[3]), pygame.SRCALPHA)
        frame.blit(self.sheet, (0, 0), frame_rect)
        return frame

    def get_strip(self, start_x, start_y, width, height, count):
        """Extrahiert eine Reihe von Frames"""
        frames = []
        for i in range(count):
            frame_rect = (start_x + i*width, start_y, width, height)
            frames.append(self.get_frame(frame_rect))
        return frames