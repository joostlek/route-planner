from typing import List 
from datetime import datetime
from pydantic import BaseModel

class Trip(BaseModel):
    start: str
    end: str 
    type: str 


    
class Advice(BaseModel):
    start: str
    destination: str
    steps: List[Trip]
    points: int 
    


class Train(BaseModel):
    number: str
    length: int
    busy_score: str
    stops: str
    destination: str

class Station(BaseModel):
    name: str 
    






