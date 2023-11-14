from models.game import Player
from pydantic import BaseModel
from schemas.card import CardOut


class PlayerOut(BaseModel):
    id: int
    name: str
    round_position: int
    alive: bool
    role: str
    hand: list[CardOut] = []
    quarantine: bool

    @classmethod
    def from_player(cls, player: Player):
        # Crear una instancia de PlayerOut basada en una instancia de Player
        return cls(
            name=player.name,
            id=player.id,
            round_position=player.round_position,
            alive=player.alive,  # Agregar el campo 'alive'
            role=player.role,  # Agregar el campo 'role'
            hand=[
                CardOut.from_card(card) for card in player.hand
            ],  # Agregar el campo 'hand'
            quarantine=(player.quarantine > 0),
        )

    @classmethod
    def to_json(cls, player: Player):
        # Return a JSON-serializable representation of the Player object
        player = cls.from_player(player)
        return {
            "id": player.id,
            "name": player.name,
            "round_position": player.round_position,
            "alive": player.alive,
            "role": player.role,
            "hand": [card.to_json(card) for card in player.hand],
            "quarantine": player.quarantine,
        }
