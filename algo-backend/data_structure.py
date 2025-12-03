######################################################
### Main data objects used in the RAPTOR Algorithm ###
######################################################

from dataclasses import dataclass
from typing import List

@dataclass
class Stop:
    """Object representing a particular stop in a route or trip"""
    name: str
    id: str
    lat: float
    lon: float
    min_transfer_time: int = 300 # in seconds
    routes: List[str] = None

    def add_route(self, route_id):
        if self.routes is None:
            self.routes = []
        self.routes.append(route_id)

@dataclass
class Route:
    """Object representing a fixed route or itinerary"""
    name: str
    id: str
    stop_list: List[str] # contains the stop ids

@dataclass
class Trip:
    """A particular instance of a route, with specific arrival times"""
    id: str
    parent_route: str # route id
    arrival_times: List[float]
    departure_times: List[float]