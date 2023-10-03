from models.game import Card
from pydantic import BaseModel


class CardOut(BaseModel):
    id: int
    idtype: int

    @classmethod
    def from_card(cls, card: Card):
        return cls(
            id=card.id,
            idtype=card.idtype,
        )
