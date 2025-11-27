from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from RedLightGreenLight.States.StateFactory import StateFactory


class State(ABC):
    """
    Basisklasse für alle States im Moore-Automaten.
    Jeder State entscheidet autonom über Zustandsübergänge.
    """

    def __init__(self, *args, **kwargs):
        """Wird von konkreten States überschrieben"""
        self._factory: Optional[StateFactory] = None

    @abstractmethod
    def enter(self,delta_time:float) -> Optional[State]:
        """
        Called upon entering the state.
        Führt Entry-Aktionen aus und gibt sich selbst zurück.
        """
        pass


