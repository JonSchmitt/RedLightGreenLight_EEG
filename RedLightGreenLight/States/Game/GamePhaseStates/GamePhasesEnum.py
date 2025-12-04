from enum import Enum


class GamePhasesEnum(Enum):
    RLS = "red_light"
    GLS = "green_light"
    GOS = "game_over"
    RES = "restart"
    PAU = "pause"

