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

    @classmethod
    def to_json(cls, card: Card):
        # Return a JSON-serializable representation of the Player object954
        card = cls.from_card(card)
        return {"id": card.id, "idtype": card.idtype}
