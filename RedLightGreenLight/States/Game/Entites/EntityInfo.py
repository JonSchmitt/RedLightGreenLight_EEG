

class EntityInfo:
    """Speichert Status einer einzelnen Entity"""
    def __init__(self, entity_id: str, entity_type: str, spawn_position: tuple[float,float]):
        self._entity_id = entity_id
        self._entity_type = entity_type  # "Player", "NPC", "Enemy"
        self._is_moving = False
        self._is_dead = False
        self._position = (0.0, 0.0)
        self._spawn_position = spawn_position

    def is_moving(self) -> bool:
        return self._is_moving

    def is_dead(self) -> bool:
        return self._is_dead

    def get_position(self) -> tuple[float,float]:
        return self._position

    def get_spawn_position(self) -> tuple[float,float]:
        return self._spawn_position

    def set_position(self, position: list[float]):
        self._position = position

    def set_spawn_position(self, spawn_position: list[float]):
        self._spawn_position = spawn_position

    def set_moving(self, is_moving: bool):
        self._is_moving = is_moving

    def set_dead(self, is_dead: bool):
        self._is_dead = is_dead

    def get_entity_type(self) -> str:
        return self._entity_type

    def get_entity_id(self) -> str:
        return self._entity_id

    def set_entity_type(self, entity_type: str):
        self._entity_type = entity_type

    def set_entity_id(self, entity_id: str):
        self._entity_id = entity_id