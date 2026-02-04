import pygame
from typing import Optional



class MusicManager:
    """
    Manages background music playback, including fading effects.
    """
    def __init__(self):
        self._current_track: Optional[str] = None
        self._target_volume = 1.0
        self._current_volume = 1.0

        # Fade state
        self._is_fading = False
        self._fade_direction = 0  # 1 = fade in, -1 = fade out, 0 = no fade
        self._fade_speed = 0.0  # Volume change per second
        self._fade_start_volume = 0.0
        self._fade_target_volume = 1.0

    def play(self, music_file: str, loop: bool = True, volume: float = 1.0,
             fade_in: bool = False, fade_in_time: float = 0.0,
             restart_track: bool = False) -> None:
        """
        Plays a music track.

        Args:
            music_file (str): Path to the music file.
            loop (bool): Whether to loop the track.
            volume (float): Target volume (0.0 - 1.0).
            fade_in (bool): Whether to fade in.
            fade_in_time (float): Duration of fade-in in seconds.
            restart_track (bool): Forces restart even if the track is already playing.
        """
        self._target_volume = volume

        # Check if track needs to be reloaded
        track_changed = self._current_track != music_file
        should_restart = track_changed or restart_track

        if should_restart:
            # Load and start track
            pygame.mixer.music.load(music_file)

            if fade_in and fade_in_time > 0:
                # Start at volume 0 and fade in
                pygame.mixer.music.set_volume(0.0)
                self._current_volume = 0.0
                self._start_fade_in(volume, fade_in_time)
            else:
                # Start directly with target volume
                pygame.mixer.music.set_volume(volume)
                self._current_volume = volume
                self._stop_fade()

            pygame.mixer.music.play(loops=-1 if loop else 0)
            self._current_track = music_file
        else:
            # Track already playing - just fade in if requested
            if fade_in and fade_in_time > 0 and self._current_volume < volume:
                self._start_fade_in(volume, fade_in_time)

    def stop(self, fade_out: bool = False, fade_out_time: float = 0.0) -> None:
        """
        Stops the music.

        Args:
            fade_out (bool): Whether to fade out before stopping.
            fade_out_time (float): Duration of fade-out in seconds.
        """
        if fade_out and fade_out_time > 0 and pygame.mixer.music.get_busy():
            self._start_fade_out(fade_out_time)
        else:
            pygame.mixer.music.stop()
            self._current_track = None
            self._stop_fade()

    def pause(self) -> None:
        """Pauses the music."""
        pygame.mixer.music.pause()

    def unpause(self) -> None:
        """Unpauses the music."""
        pygame.mixer.music.unpause()

    def get_current_track(self) -> Optional[str]:
        """Returns the currently playing track path."""
        return self._current_track

    def set_volume(self, volume: float, fade_time: float = 0.0) -> None:
        """
        Sets the volume.

        Args:
            volume (float): Target volume (0.0 - 1.0).
            fade_time (float): Transition duration in seconds (0 = immediate).
        """
        self._target_volume = volume

        if fade_time > 0:
            if volume > self._current_volume:
                self._start_fade_in(volume, fade_time)
            elif volume < self._current_volume:
                self._start_fade_out(fade_time, stop_at_end=False)
        else:
            pygame.mixer.music.set_volume(volume)
            self._current_volume = volume
            self._stop_fade()

    def update(self, delta_time: float) -> None:
        """
        Updates the fading logic. Should be called every frame.

        Args:
            delta_time (float): Time since last frame in seconds.
        """
        if not self._is_fading:
            return

        # Calculate new volume
        volume_change = self._fade_speed * delta_time
        new_volume = self._current_volume + volume_change

        # Check if target reached
        if self._fade_direction > 0:  # Fade in
            if new_volume >= self._fade_target_volume:
                new_volume = self._fade_target_volume
                self._stop_fade()
        else:  # Fade out
            if new_volume <= self._fade_target_volume:
                new_volume = self._fade_target_volume
                self._stop_fade()

                # Stop music if faded to 0
                if new_volume <= 0.0:
                    pygame.mixer.music.stop()
                    self._current_track = None

        # Set new volume
        self._current_volume = max(0.0, min(1.0, new_volume))
        pygame.mixer.music.set_volume(self._current_volume)

    def is_fading(self) -> bool:
        """Returns True if a fade effect is currently active."""
        return self._is_fading

    def get_current_volume(self) -> float:
        """Returns the current volume."""
        return self._current_volume

    # Private Helper methods

    def _start_fade_in(self, target_volume: float, duration: float) -> None:
        """Starts a fade-in effect."""
        self._is_fading = True
        self._fade_direction = 1
        self._fade_target_volume = target_volume
        self._fade_start_volume = self._current_volume

        # Speed: (target - start) / time
        volume_delta = target_volume - self._current_volume
        self._fade_speed = volume_delta / duration if duration > 0 else 0

    def _start_fade_out(self, duration: float, stop_at_end: bool = True) -> None:
        """Starts a fade-out effect."""
        self._is_fading = True
        self._fade_direction = -1
        self._fade_target_volume = 0.0 if stop_at_end else self._target_volume
        self._fade_start_volume = self._current_volume

        # Speed
        volume_delta = self._fade_target_volume - self._current_volume
        self._fade_speed = volume_delta / duration if duration > 0 else 0

    def _stop_fade(self) -> None:
        """Stops the fade effect."""
        self._is_fading = False
        self._fade_direction = 0
        self._fade_speed = 0.0
