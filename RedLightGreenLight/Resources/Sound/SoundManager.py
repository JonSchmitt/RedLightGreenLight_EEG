import pygame


class MusicManager:
    def __init__(self):
        self._current_track = None
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
        Spielt einen Musik-Track ab

        Args:
            music_file: Pfad zur Musikdatei
            loop: Ob Track geloopt werden soll
            volume: Ziel-Lautstärke (0.0 - 1.0)
            fade_in: Ob Track mit Fade-In starten soll
            fade_in_time: Dauer des Fade-In in Sekunden
            restart_track: Erzwingt Neustart auch wenn Track bereits läuft
        """
        self._target_volume = volume

        # Prüfe ob Track neu geladen werden muss
        track_changed = self._current_track != music_file
        should_restart = track_changed or restart_track

        if should_restart:
            # Lade und starte Track
            pygame.mixer.music.load(music_file)

            if fade_in and fade_in_time > 0:
                # Starte bei Lautstärke 0 und fade in
                pygame.mixer.music.set_volume(0.0)
                self._current_volume = 0.0
                self._start_fade_in(volume, fade_in_time)
            else:
                # Starte direkt mit Ziel-Lautstärke
                pygame.mixer.music.set_volume(volume)
                self._current_volume = volume
                self._stop_fade()

            pygame.mixer.music.play(loops=-1 if loop else 0)
            self._current_track = music_file
        else:
            # Track läuft bereits - nur Fade-In wenn gewünscht
            if fade_in and fade_in_time > 0 and self._current_volume < volume:
                self._start_fade_in(volume, fade_in_time)

    def stop(self, fade_out: bool = False, fade_out_time: float = 0.0) -> None:
        """
        Stoppt die Musik

        Args:
            fade_out: Ob mit Fade-Out gestoppt werden soll
            fade_out_time: Dauer des Fade-Out in Sekunden
        """
        if fade_out and fade_out_time > 0 and pygame.mixer.music.get_busy():
            self._start_fade_out(fade_out_time)
        else:
            pygame.mixer.music.stop()
            self._current_track = None
            self._stop_fade()

    def pause(self) -> None:
        """Pausiert die Musik"""
        pygame.mixer.music.pause()

    def unpause(self) -> None:
        """Setzt pausierte Musik fort"""
        pygame.mixer.music.unpause()

    def get_current_track(self) -> str:
        """Gibt den aktuell spielenden Track zurück"""
        return self._current_track

    def set_volume(self, volume: float, fade_time: float = 0.0) -> None:
        """
        Setzt die Lautstärke

        Args:
            volume: Ziel-Lautstärke (0.0 - 1.0)
            fade_time: Dauer des Übergangs in Sekunden (0 = sofort)
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
        Muss in jedem Frame aufgerufen werden für Fade-Effekte

        Args:
            delta_time: Zeit seit letztem Frame in Sekunden
        """
        if not self._is_fading:
            return

        # Berechne neue Lautstärke
        volume_change = self._fade_speed * delta_time
        new_volume = self._current_volume + volume_change

        # Prüfe ob Ziel erreicht
        if self._fade_direction > 0:  # Fade in
            if new_volume >= self._fade_target_volume:
                new_volume = self._fade_target_volume
                self._stop_fade()
        else:  # Fade out
            if new_volume <= self._fade_target_volume:
                new_volume = self._fade_target_volume
                self._stop_fade()

                # Stoppe Musik wenn auf 0
                if new_volume <= 0.0:
                    pygame.mixer.music.stop()
                    self._current_track = None

        # Setze neue Lautstärke
        self._current_volume = max(0.0, min(1.0, new_volume))
        pygame.mixer.music.set_volume(self._current_volume)

    def is_fading(self) -> bool:
        """Gibt zurück ob gerade ein Fade-Effekt läuft"""
        return self._is_fading

    def get_current_volume(self) -> float:
        """Gibt die aktuelle Lautstärke zurück"""
        return self._current_volume

    # Private Helper-Methoden

    def _start_fade_in(self, target_volume: float, duration: float) -> None:
        """Startet Fade-In Effekt"""
        self._is_fading = True
        self._fade_direction = 1
        self._fade_target_volume = target_volume
        self._fade_start_volume = self._current_volume

        # Berechne Geschwindigkeit: (Ziel - Start) / Zeit
        volume_delta = target_volume - self._current_volume
        self._fade_speed = volume_delta / duration if duration > 0 else 0

    def _start_fade_out(self, duration: float, stop_at_end: bool = True) -> None:
        """Startet Fade-Out Effekt"""
        self._is_fading = True
        self._fade_direction = -1
        self._fade_target_volume = 0.0 if stop_at_end else self._target_volume
        self._fade_start_volume = self._current_volume

        # Berechne Geschwindigkeit
        volume_delta = self._fade_target_volume - self._current_volume
        self._fade_speed = volume_delta / duration if duration > 0 else 0

    def _stop_fade(self) -> None:
        """Stoppt Fade-Effekt"""
        self._is_fading = False
        self._fade_direction = 0
        self._fade_speed = 0.0