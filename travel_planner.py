from typing import Dict, List
from datetime import datetime
import networkx as nx
import os
import matplotlib.pyplot as plt


try:
    from .nsapi  import NsApi
except ImportError:
    from nsapi  import NsApi


try:
    from .csv_convert import ov_card, crowdness_data
except ImportError:
    from csv_convert import ov_card, crowdness_data

key = os.environ['NS_KEY']


ns = NsApi(key)
places = ns.stations

def get_trip(trip: str, date: datetime = None) -> List[Dict[str, str]]:
    f = (t for t in crowdness_data if t["JourneyNumber"] == trip)
    if date is not None:
        f = (t for t in f if t["OperatingDay"] == f"{date.year}-{date.month}-{date.day}")
    return list(f)

def normalize_name(name:str) -> str:
    return name.upper().replace("-", "").replace(" ", "").replace("'", "")




def get_routes(start_station: str, destination_station: str):
    g = nx.Graph()
    attributes = {}

    trip_ids = {}
    

    def calc_weight(u, v, d):
        node_u = g.nodes[u]
        node_v = g.nodes[v]
        if node_u.get("trip_id", 0) > node_v.get("trip_id", 0):
            return 2^32
        node_u_wt = node_u.get("weight", -1)
        node_v_wt = node_v.get("weight", -1)
        if node_u_wt < 0 or node_v_wt < 0:
            return 2^32
        edge_wt = d.get("weight", 1)
        return node_u_wt / 2 + node_v_wt / 2 + edge_wt
    ns_trip = ns.trip(start_station, destination_station, datetime(2020, 10, 1, 16,00))
    for station in places:
        n:str
        g.add_node(station["code"], names=[normalize_name(n) for n in station["namen"].values()], station=station)

    for t_id, trip in enumerate(ns_trip):
        for leg in trip["legs"]:
            code = leg["product"]["number"]
            planned = leg["origin"]["plannedDateTime"].split("T")[0]
            for stop_id,stop in enumerate((t for t in crowdness_data if t["JourneyNumber"] == code and t["OperatingDay"] == planned)):
                node_name = str(t_id) + "-" + stop["JourneyNumber"] + "-" + stop["UserStopCodeEnd"]
                departure_station = g.nodes[stop["UserStopCodeBegin"]]
                arrival_station = g.nodes[stop["UserStopCodeEnd"]]
                departure =[s for s in leg["stops"] if normalize_name(s["name"]) in departure_station["names"]]
                arrival = [s for s in leg["stops"]  if normalize_name(s["name"]) in arrival_station["names"]]
                #g.add_node(node_name, { "weight": int(stop["Occupancy"]) - 1, "trip_id": t_id, "occupation": int(stop["Occupancy"]) })
                if not departure or not arrival:
                    g.add_node(node_name, weight= int(stop["Occupancy"]) - 1, trip_id=t_id, occupation=int(stop["Occupancy"]), journey_number=stop["JourneyNumber"])
                else:
                    formatting = "%Y-%m-%dT%H:%M:%S%z"
                    try:
                        length = ( datetime.strptime(departure[0]["plannedDepartureDateTime"], formatting) - datetime.strptime(arrival[0]["plannedDepartureDateTime"], formatting)).total_seconds() / 60
                        g.add_node(node_name, weight=length * (int(stop["Occupancy"]) - 1), trip_id=t_id, occupation=int(stop["Occupancy"]), journey_number=stop["JourneyNumber"], departure=departure[0], arrival=arrival[0], length=length)
                    except:
                        # print(departure[0], arrival[0])
                        pass
                g.add_edge(stop["UserStopCodeBegin"], node_name,  weight=1)
                g.add_edge(node_name,  stop["UserStopCodeEnd"],  weight=1)
                prev = str(t_id) + "-" + stop["JourneyNumber"] + "-" + stop["UserStopCodeBegin"] 
                if prev in g:
                    g.add_edge(prev, node_name, weight=0)


                
    # nx.set_node_attributes(g, "trip_id", attributes)
    for n in (g.nodes[n] for n in nx.shortest_path(g, start_station, destination_station, weight=calc_weight)):
        try:
            print(n["departure"])
        except:
            pass
    route = nx.shortest_path(g, start_station, destination_station, weight=calc_weight)
    route_info = []
    nodes = [g.nodes[k] for k in route]
    i = 0
    while i < len(nodes) - 1:
        start = nodes[i]
        start_index = i
        i += 1
        while "station" not in nodes[i]:
            i += 1
            print(i)
        destination = nodes[i]
        destination_index = i
        
        
        route_info.append({
            "start": start["station"]["namen"]["lang"],
            "destination": destination["station"]["namen"]["lang"],
            "departure": "",
            "arrival": "",
            "type": "train"
        })
           
        
    return route_info
    #return (nx.shortest_path(g, start_station, destination_station, weight=calc_weight), nx.shortest_path_length(g, start_station, destination_station, weight=calc_weight))
        

if __name__ == "__main__":
    print(get_routes("ED", "VS"))
