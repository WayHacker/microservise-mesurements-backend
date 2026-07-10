from typing import Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    gender: Literal["male", "female"] | None
    age: int | None
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(BaseModel):
    gender: Literal["male", "female"] | None
    age: int | None
