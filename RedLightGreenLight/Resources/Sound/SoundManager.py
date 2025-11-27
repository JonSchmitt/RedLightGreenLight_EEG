import pygame

class MusicManager:
    def __init__(self):
        self._current_track = None

    def play(self, music_file, loop=True):
        if self._current_track != music_file:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1 if loop else 0)
            self._current_track = music_file

    def stop(self):
        pygame.mixer.music.stop()
        self._current_track = None

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def get_current_track(self):
        return self._current_track

    def fade_out(self, time):
        pygame.mixer.music.fadeout(time*1000)
