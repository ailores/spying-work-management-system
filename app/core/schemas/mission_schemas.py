from pydantic import BaseModel, ConfigDict, Field

from app.core.schemas.cat_schemas import SpyCatModelResponse


class TargetCreateSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    country: str = Field(min_length=2, max_length=50)


class TargetUpdateSchema(BaseModel):
    notes: str | None = Field(min_length=2, max_length=250)
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class TargetResponseSchema(BaseModel):
    id: int
    name: str
    country: str
    notes: str | None
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class MissionCreateSchema(BaseModel):
    targets: list[TargetCreateSchema]


class MissionModelResponse(BaseModel):
    id: int
    is_completed: bool = False
    assigned_spy_cat: SpyCatModelResponse | None
    targets: list[TargetResponseSchema]

    model_config = ConfigDict(from_attributes=True)


class MissionResponse(BaseModel):
    message: str
    data: MissionModelResponse
