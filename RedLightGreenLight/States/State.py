from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

import pygame

from RedLightGreenLight.Inputs.KeysEnum import KEY


class State(ABC):
    """
    Base class for all states in the Moore Machine.
    Each state autonomously decides state transitions based on inputs and time.
    Implements the Observer pattern for settings changes (when inherited).
    """

    @abstractmethod
    def update(self,delta_time:float,keys:list[list[KEY]]) -> Optional[State]:
        """
        Called every frame.
        Decides the next state.

        Args:
            delta_time (float): Time since last frame in seconds.
            keys (list[list[KEY]]): List of pressed keys.

        Returns:
            Optional[State]: The next state or None if remaining in current state.
        """
        pass


    def enter(self,screen:pygame.Surface = None) ->None:
        """
        Called when entering this state.

        Args:
            screen (pygame.Surface, optional): The screen to draw on.
        """
        self.print_enter()


    def exit(self) -> None:
        """
        Called when exiting this state.
        Can be used for cleanup tasks.
        """
        self.print_exit()


    def print_enter(self):
        """Logs state entry to console."""
        print(f"[{self.__class__.__name__}] enter()")

    def print_exit(self):
        """Logs state exit to console."""
        print(f"[{self.__class__.__name__}] exit()")


