from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

import pygame

from RedLightGreenLight.Inputs.KeysEnum import KEY


class State(ABC):
    """
    Basisklasse für alle States im Moore-Automaten.
    Jeder State entscheidet autonom über Zustandsübergänge.
    """


    @abstractmethod
    def update(self,delta_time:float,keys:list[list[KEY]]) -> Optional[State]:
        """
        Called upon updating the state.
        """
        pass


    def enter(self,screen:pygame.Surface = None) ->None:
        """
        Called upon entering the state.
        Prints Entry to console
        """
        self.print_enter()


    def exit(self) -> None:
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


