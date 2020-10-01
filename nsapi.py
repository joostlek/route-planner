from typing import Dict, List
import requests as req
import json
import datetime


class NsApi:
    
    def __init__(self, key: str):
        self.key: str = key
        self._stations: List[Dict[str, str]] = None

    
    def __request(self, uri: str, query: Dict[str, str] = []):
        response = req.request(
            "GET", 
            f"https://gateway.apiportal.ns.nl{uri}", 
            params=query,
            headers= {"Ocp-Apim-Subscription-Key": self.key}
        )
        return response.json()


    def trip(self, start: str, destination: str, dt: datetime.datetime = None):
        query = {"fromStation": start, "toStation": destination}
        if dt is not None:
            query["dateTime"] = dt.isoformat()
        return self.__request("/reisinformatie-api/api/v3/trips", query)["trips"]

    @property
    def stations(self) -> List[Dict[str, str]]:
        if self._stations is None:
            self._stations = self.__request("/reisinformatie-api/api/v2/stations")
        return self._stations["payload"]


    @property
    def ov_bikes(self):
        pass


if __name__ == "__main__":
    ns = NsApi("609622c391014b43bba1d102e7855a14")
    