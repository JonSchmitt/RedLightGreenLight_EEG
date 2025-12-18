from enum import Enum


class Actions(Enum):
    """
    Enum for possible Entity actions.
    """
    MOVE = "move"
    IDLE = "idle"
    NONE = "none"