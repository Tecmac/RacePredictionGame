import json
from pydantic import BaseModel


class PlayerDTO(BaseModel):
    gamertag: str
    name: str
    forename: str
    password: str
