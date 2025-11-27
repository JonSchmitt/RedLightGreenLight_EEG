from __future__ import annotations

from RedLightGreenLight.Game.Entity import Entity
from RedLightGreenLight.Resources.Spritesheets import SpriteSheetStruct


class GameModel:
    """Model for the game."""
    def __init__(self, switch_time: int, warning_time: int):
        # Game Phases
        self._gamephase1 = "GreenLight"
        self._gamephase2 = "RedLight"
        self._current_gamephase = self._gamephase1
        self._is_paused = False

        # Time
        self._time_passed = 0
        self._switch_time = switch_time
        self._warning_time = warning_time

        # Entities
        self._entities = []
        self.load_entities()

        # Game over
        self._game_over = False
        self._game_over_start_time = 0
        self._game_over_duration = 5

    ####
    # Game phases
    ####

    def get_current_gamephase(self):
        return self._current_gamephase

    def set_current_gamephase(self, gamephase):
        self._current_gamephase = gamephase

    def switch_gamephase(self):
        if self._current_gamephase == self._gamephase1:
            self._current_gamephase = self._gamephase2
        else:
            self._current_gamephase = self._gamephase1

    def is_red_light(self):
        return self._current_gamephase == self._gamephase2

    def is_green_light(self):
        return self._current_gamephase == self._gamephase1

    def is_pause(self):
        return self._is_paused

    def set_pause(self,pause:bool):
        self._is_paused = pause

    def _restart_game(self):
        self._time_passed = 0
        self._current_gamephase = self._gamephase1
        self.reset_entities_position()

    def start_game_over(self, start_time):
        self._game_over = True
        self._game_over_start_time = start_time
        self._is_paused = True

    def evaluate_game_over(self,dt):
        """Call this every frame"""
        print("Game over: ", self._game_over)
        if self._game_over:
            elapsed = dt - self._game_over_start_time
            print("Elapsed time: ", elapsed, " | Duration: ", self._game_over_duration)
            if elapsed >= self._game_over_duration:
                self.end_game_over()


    def end_game_over(self):
        self._game_over = False
        self._is_paused = False
        self._restart_game()

    def is_game_over(self):
        return self._game_over

    def get_game_over_elapsed_time(self,current_time):
        if self._game_over:
            return current_time - self._game_over_start_time
        else:
            return 0

    def get_game_over_duration(self):
        return self._game_over_duration

    ####
    # Time
    ####

    def update_settings(self, switch_time: int, warning_time: int):
        self._switch_time = switch_time
        self._warning_time = warning_time
        self.update_time(0)
        print(f"Switch time: {self._switch_time} | Warning time: {self._warning_time} | Time passed: {self._time_passed} | Current gamephase: {self._current_gamephase}")

    def update_time(self, delta_time: float):
        if not self._is_paused:
            self._time_passed += delta_time
            if self._time_passed >= self._switch_time:
                self.switch_gamephase()
                self._time_passed = 0

    def get_remaining_warning_time(self):
        remaining_time = self._switch_time - self._time_passed
        if self._current_gamephase == self._gamephase1 and remaining_time <= self._warning_time:
            return remaining_time
        else:
            return None

    def get_remaining_in_phase_time(self):
        return self._switch_time - self._time_passed

    ####
    # Entities
    ####

    def load_entities(self):
        self._entities = []
        self._entities.append(Entity(True, (100, 520), (200, 500), 1, SpriteSheetStruct.player_sprite_sheets))
    def move_entities(self):
        for entity in self._entities:
            entity.move()

    def reset_player_position(self):
        self.get_player().reset_position()

    def reset_entities_position(self):
        for entity in self._entities:
            entity.reset_position()

    def get_player_position(self):
        return self.get_player().get_position()


    def add_entity(self, entity:Entity):
        self._entities.append(entity)

    def get_entities(self) -> list[Entity]:
        return self._entities


    def remove_entity(self, entity:Entity):
        self._entities.remove(entity)

    def get_player(self)->Entity|None:
        n = 0
        while n<len(self._entities):
            if self._entities[n].is_player():
                return self._entities[n]
            n += 1
        return None

    def set_player_moving(self,direction:tuple[int,int]=None):
        player = self.get_player()
        if player:
            if direction:
                self.get_player().set_movement_direction(direction)
            else:
                self.get_player().set_movement_direction((0,0))
        else:
            print("No player found")

    def is_player_moving(self):
        return self.get_player().get_movement_direction() != (0,0)


    def is_player_dead(self,current_time):
        # 2 is the time between "revival" and end of game_over
        return self._game_over and self._game_over_duration > 2 +  self.get_game_over_elapsed_time(current_time)