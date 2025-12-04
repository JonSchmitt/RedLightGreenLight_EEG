from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from RedLightGreenLight.States.Game.GameModel import GameModel


class GamePhaseState(ABC):
    """
    Abstract Base Class for all GamePhases
    """
    @abstractmethod
    def update(self, delta_time: float, game_model: GameModel) -> Optional[GamePhaseState]:
        pass

    def enter(self, game_model: GameModel) ->None:
        """
        Called upon entering the state.
        Prints Entry to console
        """
        print(f"[{self.__class__.__name__}] enter()")





