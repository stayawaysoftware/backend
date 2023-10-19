from models.room import User
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import validator

from .validators import EndpointValidators

# ======================= Input Schemas =======================


class Username(BaseModel):  # Used in create user
    username: str = Field(max_length=32)

    @validator("username", pre=True, allow_reuse=True)
    def apply_validators(cls, username):
        EndpointValidators.validate_username_not_exists(username)
        return username


class UserId(BaseModel):  # Used in delete user
    id: int = Field(gt=0)

    @validator("id", pre=True, allow_reuse=True)
    def apply_validators(cls, id):
        user_id = id  # Rename to reuse validator
        EndpointValidators.validate_user_exists(user_id)
        return id


# ======================= Output Schemas =======================


class UserOut(BaseModel):
    model_config = ConfigDict(title="User", from_attributes=True)

    id: int = Field(gt=0)
    username: str = Field(max_length=32)

    @classmethod
    def from_db(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
        )
