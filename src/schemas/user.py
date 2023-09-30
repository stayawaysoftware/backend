"""User schemas"""
from pydantic import BaseModel


class UserOut(BaseModel):
    """User schema for output only"""

    id: int
    username: str

    class Config:
        """Pydantic configuration"""

        from_attributes = True
