from models.game import Player
from pydantic import BaseModel


class PlayerOut(BaseModel):
    id: int
    name: str
    round_position: int
    alive: bool
    role: str

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
        )
