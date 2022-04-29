from pydantic import BaseModel
from typing import Optional


class RequestCar(BaseModel):
    brand: str
    model: str
    description: Optional[str] = None
    type: str
    color: Optional[str]
    year: Optional[int]

    class Config:
        orm_mode = True


class ResponseCar(RequestCar):
    id: int
