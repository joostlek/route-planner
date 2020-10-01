import enum
from typing import Optional, List
from fastapi import FastAPI



try:
    from .ovapi import OvApi
except ImportError:
    from ovapi import OvApi
try: 
    from .models import Train, Advice, Trip
except ImportError:
    from models import Train, Advice, Trip

try: 
    from .travel_planner import get_routes
except ImportError:
    from travel_planner import get_routes


app = FastAPI()




@app.get("/dev/advice")
def generate_advice(start: str, destination: str) -> List[Advice]:
    return get_routes(start, destination)

@app.get("/advice")
def generate_advice(start: str, destination: str) -> List[Advice]:    
    return [
        {
            "start": "Ede-Wageningen",
            "destination": "Utrecht, Heidelberglaan",
            "date": "2020-10-01",
            "points": 0,
            "trips": [
                {
                    "start": "Ede-Wageningen",
                    "destination": "Utrecht Centraal",
                    "departure": "07:26",
                    "arrival": "07:50",
                    "type": "train"
                },
                {
                    "start": "Utrecht Centraal",
                    "destination": "Heidelberglaan",
                    "departure": "07:55",
                    "arrival": "08:10",
                    "type": "Tram"
                }
            ]
        },
        {
            "start": "Ede-Wageningen",
            "destination": "Utrecht, Heidelberglaan",
            "date": "2020-10-01",
            "points": 1,
            "trips": [
                {
                    "start": "Ede-Wageningen",
                    "destination": "Utrecht Centraal",
                    "departure": "07:26",
                    "arrival": "07:50",
                    "type": "train"
                },
                {
                    "start": "Utrecht Centraal",
                    "destination": "Heidelberglaan",
                    "departure": "07:55",
                    "arrival": "08:15",
                    "type": "Bus"
                }
            ]
        },
        {
            "start": "Ede-Wageningen",
            "destination": "Utrecht, Heidelberglaan",
            "date": "2020-10-01",
            "points": 5,
            "trips": [
                {
                    "start": "Ede-Wageningen",
                    "destination": "Utrecht Centraal",
                    "departure": "07:11",
                    "arrival": "07:35",
                    "type": "train"
                },
                {
                    "start": "Utrecht Centraal",
                    "destination": "Heidelberglaan",
                    "departure": "07:40",
                    "arrival": "07:55",
                    "type": "Tram"
                }
            ]
        },
        {
            "start": "Ede-Wageningen",
            "destination": "Utrecht, Heidelberglaan",
            "date": "2020-10-01",
            "points": 4,
            "trips": [
                {
                    "start": "Ede-Wageningen",
                    "destination": "Driebergen-Zeist",
                    "departure": "07:26",
                    "arrival": "07:40",
                    "type": "train"
                },
                {
                    "start": "Driebergen-Zeist",
                    "destination": "Jordanlaan",
                    "departure": "07:45",
                    "arrival": "08:00",
                    "type": "Bus"
                },
                {
                    "start":"Jordanlaan",
                    "destination": "Driebergen-Zeist",
                    "departure": "08:05",
                    "arrival": "08:15",
                    "type": "Bus"
                }
            ]
        }
    ]
    

#@app.get("/trips")
#def trips():
#    pass




#@app.get("/stations")
#def station():
#    pass

#@app.get("/trains/{id}/capacity")
#def train(id: int) -> List[Train]:
#    pass
    