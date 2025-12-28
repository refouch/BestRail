#########################################################################
### Module to tranform RAPTOR results into usable data for the server ###
#########################################################################

from typing import List, Dict
from .data_structure import Stop
import json
import re 

def rank_by_time(paths: List[List[Dict]]) -> List[List[Dict]]:
    """Function to rerank paths in the list according to arrival time rather than number of rounds
        Simple imlementation using Merge Sort.
        """
    
    if len(paths) <= 1:
        return paths

    mid = len(paths) // 2
    left = rank_by_time(paths[:mid])
    right = rank_by_time(paths[mid:])

    return merge(left, right)


def merge(left: List[List[Dict]], right: List[List[Dict]]) -> List[List[Dict]]:
    """Merge fucntion for Merge Sort"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][-1].get('arrival_time') <= right[j][-1].get('arrival_time'):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def extract_train_info(trip_id: str) -> str:
    """
    Extract the train type and train number from complex GTFS ID
    Ex: "OCESN863040..." -> ("TER", "863040")
    """
    
    # Extraction of the number
    # Regex : look for the begining (^) followed by letters ([A-Z]+) 
    # then capture the numbers that follow (\d+)
    match_num = re.search(r'^[A-Z]+(\d+)', trip_id)
    numero = match_num.group(1) if match_num else "Inconnu"

    # Extraction of the kind of trian 
    
    type_train = "Train"
    
    if ":OUI:" in trip_id:
        type_train = "TGV INOUI"
    elif ":OGO:" in trip_id:
        type_train = "OUIGO"
    elif ":TER:" in trip_id:
        type_train = "TER"
    elif ":COR:" in trip_id or ":IC:" in trip_id: 
        type_train = "Intercités"
    elif "TGV" in trip_id: 
        type_train = "TGV"

    return f"{type_train} n°{numero}"


def jsonify_paths(paths: List[List[Dict]], stop_list: List[Stop]) -> Dict:
    """Final formatting of the results to be sent to the frontend"""

    final_list = []

    for k, path in enumerate(paths):

        if path:
            segments = []

            for i in range(len(path)): # for each segment in path

                stop1 = stop_list[path[i].get('board_stop')]
                stop2 = stop_list[path[i].get('stop')]

                board_time = path[i].get('board_time')
                arrival_time = path[i].get('arrival_time')

                trip = path[i].get('trip_id')
                trip = extract_train_info(trip)
                route = path[i].get('route_id')

                segments.append({
                    "from": stop1.name,
                    "to": stop2.name,
                    "dep_coor": (float(stop1.lat), float(stop1.lon)),
                    "arr_coor": (float(stop2.lat), float(stop2.lon)),
                    "board_time": board_time,
                    "arrival_time": arrival_time,
                    "trip": trip,
                    "route": route
                })

            final_list.append({
                "departure_stop": stop_list[path[0].get('board_stop')].name,
                "arrival_stop": stop_list[path[-1].get('stop')].name,
                "segments": segments
            })
    
    # return json.dumps(final_list,indent=2)
    return final_list