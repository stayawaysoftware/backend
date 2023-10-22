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

    @classmethod
    def from_player(cls, player: Player):
        # Crear una instancia de PlayerOut basada en una instancia de Player
        return cls(
            name=player.name,
            id=player.id,
            round_position=player.round_position,
            game_id=player.game.id,  # Asumiendo que Player tiene una relación con Game
            alive=player.alive,  # Agregar el campo 'alive'
            role=player.role,  # Agregar el campo 'role'
            hand=[
                CardOut.from_card(card) for card in player.hand
            ],  # Agregar el campo 'hand'
        )

    @classmethod
    def json(self, player: Player):
        # Return a JSON-serializable representation of the Player object
        cls = PlayerOut.from_player(player)
        return {
            "id": cls.id,
            "name": cls.name,
            "round_position": cls.round_position,
            "alive": cls.alive,
            "role": cls.role,
            "hand": [card.json(card) for card in cls.hand],
        }
