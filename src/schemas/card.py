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

    def json(self, card: Card):
        # Return a JSON-serializable representation of the Player object
        cls = CardOut.from_card(card)
        return {"id": cls.id, "idtype": cls.idtype}
