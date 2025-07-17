from pydantic import BaseModel

class Coordinate(BaseModel):
    xCoord: float
    yCoord: float
    zCoord: float

class CoordinatesResponse(BaseModel):
    pathCoord: list[Coordinate]
    final_answer: str