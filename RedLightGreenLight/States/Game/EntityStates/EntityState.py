from __future__ import annotations
from abc import ABC, abstractmethod

from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.StateResultsEnum import ENTITY_ACTION
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from RedLightGreenLight.States.Game.Entites.Entity import Entity

class EntityState(ABC):
    """
    Abstract Base Class for all EntityStates
    """
    @abstractmethod
    def update(self, entity: Entity, action: ENTITY_ACTION, context: GameContext) -> 'EntityState':
        pass


    def enter(self, entity: Entity, context: GameContext) -> None:
        """
        Called upon entering the state.
        Prints Entry to console
        """
        self.print_enter(entity)

    def exit(self, entity: Entity, context: GameContext) -> None:
        """
        Called upon exiting the state.
        Prints Exit to console
        """
        self.print_exit(entity)

    def print_enter(self, entity: Entity):
        """
        Prints entry to console
        """
        print(f"[{entity}] [{self.__class__.__name__}] enter()")

    def print_exit(self, entity: Entity):
        """
        Prints Exit to console
        """
        print(f"[{entity}] [{self.__class__.__name__}] exit()")