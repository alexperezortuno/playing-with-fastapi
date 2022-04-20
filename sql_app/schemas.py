from pydantic import BaseModel


class CarBase(BaseModel):
    id: int | None = None
    brand: str
    model: str
    description: str | None = None
    type: str
    color: str | None = None
    year: int | None = None
