from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def enter(self):
        """ Called upon entering the state """
        pass

    @abstractmethod
    def exit(self):
        """ Called upon exiting the state """
        pass

    @abstractmethod
    def update(self, delta_time:float):
        """ Called every frame while in the state """
        pass

    @abstractmethod
    def handle_events(self,events):
        """ Called every frame while in the state """
        pass