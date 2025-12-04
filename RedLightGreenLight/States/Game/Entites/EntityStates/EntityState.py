from __future__ import annotations
from abc import ABC, abstractmethod

from RedLightGreenLight.Inputs.KeysEnum import KEY
from RedLightGreenLight.States.Game.Entites.EntityModel import EntityModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from RedLightGreenLight.States.Game.GameModel import GameModel


class EntityState(ABC):
    """
    Abstract Base Class for all EntityStates
    """
    @abstractmethod
    def update(self, keys_pressed:list[list[KEY]], entity_model:EntityModel, game_model:GameModel) -> 'EntityState':
        pass


    def enter(self, keys_pressed:list[list[KEY]], entity_model:EntityModel, game_model:GameModel) -> None:
        """
        Called upon entering the state.
        Prints Entry to console
        """
        print(f"[{entity_model.get_entity_id()}] [{self.__class__.__name__}] enter()")

