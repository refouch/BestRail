######################################################
### Main data objects used in the RAPTOR Algorithm ###
######################################################

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union

@dataclass
class Stop:
    """Object representing a particular stop in a route or trip"""
    name: str
    id: str
    lat: float
    lon: float
    min_transfer_time: int = 300 # in seconds (i.e 5mn)
    index_in_list: int = None


@dataclass
class Route:
    """Object representing a fixed route or itinerary"""
    name: str
    id: str
    stop_list: List[str] # all stops the route goes through. Represented the stop_id
    stop_index_list: List[int] = None # TO BE CONSTRUCTED
    index_in_list: int = None
    trips: List[Trip] = None # TO BE CONSTRUCTED / CAUTION: trips must be in chronological order!

    def add_trip(self,trip: Trip):
        if self.trips is None:
            self.trips = []
        self.trips.append(trip)

@dataclass
class Trip:
    """A particular instance of a route, with specific arrival times"""
    id: str
    arrival_times: List[float]
    departure_times: List[float]


def map_index(object_list: List[Union[Route,Stop]]):
    """Simple function mapping a route/stop to its index in the global list"""
    if object_list[0].index_in_list != None:
        return None
    
    for (i, object) in enumerate(object_list):
        object.index_in_list = i

def map_stop_to_routes(stop_list, route_list):
    """Function to generate a mapping linking every stop (by index in the list) to the routes traversing it"""
    map_index(stop_list)
    map_index(route_list)

    stop_to_routes = [[] for _ in range(len(stop_list))]

    # CAUTION: Construction of stop_index_list still to be implemented !!

    for route in route_list:
        for stop_index in route.stop_index_list:
            stop_to_routes[stop_index].append(route.index_in_list)

    return stop_to_routes