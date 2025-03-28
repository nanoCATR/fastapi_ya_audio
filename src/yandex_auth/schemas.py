from pydantic import BaseModel, RootModel
from datetime import date

class Insurancerate(BaseModel):
    id: int
    date: date
    cargo_type: str 
    rate: float

class Rate(BaseModel):
    declared_value: float
    cargo_type: str 
    date: date

class RateItem(BaseModel):
     cargo_type: str 
     rate: float 

class RatesInput(RootModel): 
    root: dict[date, list[RateItem]]