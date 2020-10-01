import csv
import json

from typing import List, Dict

ov_card: List[Dict[str, str]]  = []

with  open("data.csv") as csv_file:
    reader = csv.DictReader(csv_file, delimiter=";")
    ov_card = [i for i in reader]



crowdness_data: List[Dict[str, str]] = []
with open("data/OC_NS_20200929.csv") as csv_file:
    reader = csv.DictReader(csv_file, delimiter=",")
    crowdness_data = [i for i in reader if i['Occupancy']]



