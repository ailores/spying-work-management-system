from pydantic import BaseModel, Field, ConfigDict


class SpyCatSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    breed: str
    experience: int = Field(ge=0)
    salary: int = Field(gt=0)


class SpyCatUpdate(BaseModel):
    salary: int = Field(gt=0)

    def __str__(self) -> str:
        return f"salary: {self.salary}"


class SpyCatModelResponse(BaseModel):
    id: int
    name: str
    breed: str
    experience: int
    salary: int
    is_available: bool

    model_config = ConfigDict(from_attributes=True)


class SpyCatResponse(BaseModel):
    message: str
    data: SpyCatModelResponse
