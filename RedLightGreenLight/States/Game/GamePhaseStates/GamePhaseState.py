from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from RedLightGreenLight.States.Game.GameContext import GameContext


class GamePhaseState(ABC):
    """
    Abstract Base Class for all GamePhases
    """
    @abstractmethod
    def update(self, delta_time: float, context: GameContext) -> Optional[GamePhaseState]:
        pass

    def enter(self, context: GameContext) ->None:
        """
        Called upon entering the state.
        Prints Entry to console
        """
        self.print_enter()


    def exit(self, context: GameContext) -> None:
        """
        Called upon exiting the state.
        Prints Exit to console
        """
        self.print_exit()


    def print_enter(self):
        """
        Prints entry to console
        """
        print(f"[{self.__class__.__name__}] enter()")

    def print_exit(self):
        """
        Prints Exit to console
        """
        print(f"[{self.__class__.__name__}] exit()")


