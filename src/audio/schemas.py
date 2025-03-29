from pydantic import BaseModel, RootModel
from datetime import date

class Audio(BaseModel):
    id: int
    filename: str
    location: str 
    user_owner: int
