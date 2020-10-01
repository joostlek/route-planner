from typing import Dict, List
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt


try:
    from .nsapi  import NsApi
except ImportError:
    from nsapi  import NsApi


try:
    from .csv_convert import ov_card, crowdness_data
except ImportError:
    from csv_convert import ov_card, crowdness_data

key = open("api_key.txt").readline()


ns = NsApi(key)
places = ns.stations

def get_trip(trip: str, date: datetime = None) -> List[Dict[str, str]]:
    f = (t for t in crowdness_data if t["JourneyNumber"] == trip)
    if date is not None:
        f = (t for t in f if t["OperatingDay"] == f"{date.year}-{date.month}-{date.day}")
    return list(f)




def get_routes(start_station: str, destination_station: str):
    g = nx.MultiDiGraph()
    def weight(u, v, d):
        node_u = g.nodes[u]
        node_v = g.nodes[v]
        if node_u.get("trip_id", 0) > node_v.get("trip_id", 0):
            return 2^32

        node_u_wt = node_u.get("node_weight", 1)
        node_v_wt = node_v.get("node_weight", 1)

        edge_wt = d.get("weight", 1)
        return node_u_wt / 2 + node_v_wt / 2 + edge_wt


    ns_trip = ns.trip(start_station, destination_station, datetime(2020, 10, 1, 12,00))
   


    for p in places["payload"][0]["locations"]:
        g.add_node(p["stationCode"])
    for t_id, trip in enumerate(ns_trip):
        for leg in trip["legs"]:
            code = leg["product"]["number"]
            planned = leg["origin"]["plannedDateTime"].split("T")[0]
            for stop in (t for t in crowdness_data if t["JourneyNumber"] == code and t["OperatingDay"] == planned):
                node_name = str(t_id) + "-" + stop["JourneyNumber"] + "-" + stop["UserStopCodeEnd"]
                g.add_node(node_name, weight=int(stop["Occupancy"]) - 1, trip_id=t_id, occupation=int(stop["Occupancy"]))
                g.add_edge(stop["UserStopCodeBegin"], node_name,  weight=1)
                g.add_edge(node_name,  stop["UserStopCodeEnd"],  weight=1)
                prev = str(t_id) + "-" + stop["JourneyNumber"] + "-" + stop["UserStopCodeBegin"] 
                if prev in g:
                    g.add_edge(prev, node_name, weight=0)
    return (nx.shortest_path(g, start_station, destination_station, weight=weight), nx.shortest_path_length(g, start_station, destination_station, weight=weight))
        
        





if __name__ == "__main__":
    pass
