from pydantic import BaseModel

class Shoe(BaseModel):
    image: str
    size: float
    brand: str
    model: str
    offer: bool
    color: str

