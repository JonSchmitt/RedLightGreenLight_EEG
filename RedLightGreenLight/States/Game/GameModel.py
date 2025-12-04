from __future__ import annotations

from RedLightGreenLight.States.Game.Entites.Entity import Entity
from RedLightGreenLight.Resources.Spritesheets import SpriteSheetStruct
from RedLightGreenLight.States.Game.Entites.Player import Player
from RedLightGreenLight.States.Game.GameContext import GameContext
from RedLightGreenLight.States.Game.GamePhaseStates.GamePhaseState import GamePhaseState


class GameModel:
    def __init__(self,second_player: bool):
        # Entities
        self._entities = []
        self._second_player = second_player


    def load_entities(self):
        self._entities = []
        self._entities.append(Player("Player_1", (100, 720), (200, 500), 1, SpriteSheetStruct.PlayerEntity))
        if self._second_player:
            self._entities.append(Player("Player_2", (100, 320), (200, 500), 1, SpriteSheetStruct.PlayerEntity))

    def update_settings(self, second_player: bool, context:GameContext):
        if second_player is not self._second_player:
            if not second_player:
                context.remove_entity(self._entities[1].get_entity_id())
                self._entities.remove(self._entities[1])
            else:
                new_entity = Player("Player_2", (100, 320), (200, 500), 1, SpriteSheetStruct.PlayerEntity)
                self._entities.append(new_entity)
                new_entity.initialize(context)

        self._second_player = second_player

    def respawn_entities(self, context:GameContext):
        for e in self._entities:
            e.respawn(context)

    def respawn_player(self, context:GameContext):
        for player in self.get_players():
            player.respawn(context)


    def reset_entities_position(self):
        for entity in self._entities:
            entity.reset_position()

    def reset_players_position(self):
        for player in self.get_players():
            player.reset_position()

    def add_entity(self, entity:Entity):
        self._entities.append(entity)

    def get_entities(self) -> list[Entity]:
        return self._entities


    def remove_entity(self, entity:Entity):
        self._entities.remove(entity)

    def get_players(self)-> list[Entity] | None:
        players = []
        for e in self._entities:
            if e.is_player():
                players.append(e)
        if len(players) == 0:
            return None
        else:
            return players
