from typing import Dict, Optional, List
from RedLightGreenLight.States.Game.Entites.EntityInfo import EntityInfo

class GameContext:
    """
    Shared Context für GamePhase und alle Entities.
    Verwaltet globale Regeln und pro-Entity Status.
    """

    def __init__(self):
        # Globale Phase-Regeln (gelten für alle Entities)
        self._movement_allowed = False
        self._movement_kills_player = False
        self._is_game_paused = False
        self._is_game_over = False

        # Pro-Entity Daten (entity_id -> EntityInfo)
        self._entities: Dict[str, EntityInfo] = {}

        # Statistiken
        self._total_entities = 0
        self._entities_alive = 0
        self._entities_moving = 0

        # Zeit
        self._time_in_phase = 0.0

    # ========== Phase-Regeln (global) ==========
    def update_from_phase(self, phase_name: str):
        """Setzt globale Spielregeln basierend auf Phase"""
        if phase_name == "GreenLightState":
            print("Context:Update from Phase: GreenLightState")
            self._movement_allowed = True
            self._movement_kills_player = False
            self._is_game_paused = False
        elif phase_name == "RedLightState":
            print("Context:Update from Phase: RedLightPhase")
            self._movement_allowed = True
            self._movement_kills_player = True
            self._is_game_paused = False
        elif phase_name == "PauseState":
            print("Context:Update from Phase: PausePhase")
            self._movement_allowed = False
            self._movement_kills_player = False
            self._is_game_paused = True
        elif phase_name == "GameOverState":
            print("Context:Update from Phase: GameOverPhase")
            self._movement_allowed = False
            self._movement_kills_player = False
            self._is_game_over = True

    def is_movement_allowed(self) -> bool:
        return self._movement_allowed

    def is_movement_kills_player(self) -> bool:
        return self._movement_kills_player

    def is_game_paused(self) -> bool:
        return self._is_game_paused

    def is_game_over(self) -> bool:
        return self._is_game_over

    # ========== Entity-Verwaltung ==========
    def register_entity(self, entity_id: str, entity_type: str, spawn_position: tuple[float,float]):
        """Registriert eine neue Entity"""
        self._entities[entity_id] = EntityInfo(entity_id, entity_type,spawn_position)
        self._total_entities += 1
        self._entities_alive += 1
        print(f"  [Context] Entity registriert: {entity_id} ({entity_type})")

    def update_entity(self, entity_id: str, is_moving: bool, is_dead: bool, position: tuple[float,float]):
        """Aktualisiert Status einer spezifischen Entity"""
        if entity_id not in self._entities:
            return

        entity_info = self._entities[entity_id]

        # Zustandsänderungen tracken
        was_dead = entity_info.is_dead
        was_moving = entity_info.is_moving

        # Update Entity Info
        entity_info.is_moving = is_moving
        entity_info.is_dead = is_dead
        entity_info.position = position

        # Update Statistiken
        if not was_dead and is_dead:
            self._entities_alive -= 1
            print(f"  [Context] {entity_id} gestorben! Verbleibend: {self._entities_alive}")

        if not was_moving and is_moving:
            self._entities_moving += 1
        elif was_moving and not is_moving:
            self._entities_moving -= 1

    def remove_entity(self, entity_id: str):
        """Entfernt eine Entity"""
        if entity_id in self._entities:
            del self._entities[entity_id]
            self._total_entities -= 1
            self._entities_alive -= 1
            print(f"  [Context] Entity entfernt: {entity_id}")

    # ========== Spezielle Abfragen ==========
    def is_player_dead(self) -> bool:
        """Check if any player is dead"""
        for entity_id, info in self._entities.items():
            if info.get_entity_type() == "Player" and info.is_dead:
                return True
        return False

    def all_players_dead(self) -> bool:
        """Check if all players are dead"""
        for entity_id, info in self._entities.items():
            if info.get_entity_type() == "Player" and not info.is_dead:
                return False
        return True

    def get_alive_count(self) -> int:
        return self._entities_alive

    def get_moving_count(self) -> int:
        return self._entities_moving


    def reset(self):
        """Reset für neues Spiel"""
        self.__init__()