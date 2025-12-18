from enum import Enum


class EntityStatesEnum(Enum):
    """
    Enum for Entity States.
    """
    IDLE = "Idle"
    WALKING = "Walking"
    DEAD = "Dead"