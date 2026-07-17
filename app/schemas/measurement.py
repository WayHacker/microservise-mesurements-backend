from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator


class MeasurementCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    height: int | None = Field(None, gt=0)
    chest: int | None = Field(None, gt=0)
    waist: int | None = Field(None, gt=0)
    hips: int | None = Field(None, gt=0)
    shoulder_width: int | None = Field(None, gt=0)
    sleeve_lenght: int | None = Field(None, gt=0)
    inseam: int | None = Field(None, gt=0)


class MeasurementUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    height: int | None = Field(None, gt=0)
    chest: int | None = Field(None, gt=0)
    waist: int | None = Field(None, gt=0)
    hips: int | None = Field(None, gt=0)
    shoulder_width: int | None = Field(None, gt=0)
    sleeve_length: int | None = Field(None, gt=0)
    inseam: int | None = Field(None, gt=0)


class MeasurementResponse(BaseModel):
    id: int
    user_id: int
    is_public: bool
    share_token: str
    created_at: datetime
    updated_at: datetime
    name: str
    height: int | None = Field(None, gt=0)
    chest: int | None = Field(None, gt=0)
    waist: int | None = Field(None, gt=0)
    hips: int | None = Field(None, gt=0)
    shoulder_width: int | None = Field(None, gt=0)
    sleeve_length: int | None = Field(None, gt=0)
    inseam: int | None = Field(None, gt=0)
    model_config = ConfigDict(from_attributes=True)

    @field_validator("share_token", mode="before")
    @classmethod
    def convert_uuid_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class MeasurementListResponse(BaseModel):
    measurements: list[MeasurementResponse]


class MeasurementPublicRespone(BaseModel):
    created_at: datetime
    updated_at: datetime
    name: str
    height: int | None = Field(None, gt=0)
    chest: int | None = Field(None, gt=0)
    waist: int | None = Field(None, gt=0)
    hips: int | None = Field(None, gt=0)
    shoulder_width: int | None = Field(None, gt=0)
    sleeve_length: int | None = Field(None, gt=0)
    inseam: int | None = Field(None, gt=0)
    model_config = ConfigDict(from_attributes=True)
