################################################
### Small mock network to run the unit tests ###
################################################

from algo_backend.data_structure import Route, Stop, Trip, map_index
from typing import List

def build_mock_data():
    """
    Generates a small network in order to test the following cases:
    - Direct path
    - Multiple possible paths
    - One path is quikcer than the other
    - Some stops are unreachable depending on your starting position.

    To get a clearer idea of the netork, you can draw the routes on a piece of paper:
    Route 1: A -> B -> C -> D
    Route 2: A -> E -> F
    Route 3: H -> E -> F -> D

    We thus have: 
    - Direct path from A -> D
    - Alternative path A -> F via R2 then F -> D via R3
        (this path may be quicker !)
    - No path from nodes B, C, D to other routes (because there is no backward trips)
    """

    # ===== STOPS =====
    stops: List[Stop] = [
        Stop(name="Stop A", id="A", lat=42.00, lon=42.00, min_transfer_time=2), # lat and lon don't matter here
        Stop(name="Stop B", id="B", lat=42.00, lon=42.00, min_transfer_time=2), # 2 minutes transfer times
        Stop(name="Stop C", id="C", lat=42.00, lon=42.00, min_transfer_time=2),
        Stop(name="Stop D", id="D", lat=42.00, lon=42.00, min_transfer_time=2),
        Stop(name="Stop E", id="E", lat=42.00, lon=42.00, min_transfer_time=2),
        Stop(name="Stop F", id="F", lat=42.00, lon=42.00, min_transfer_time=2),
        Stop(name="Stop G", id="G", lat=42.00, lon=42.00, min_transfer_time=2),
        Stop(name="Stop H", id="H", lat=42.00, lon=42.00, min_transfer_time=2),        
    ]

    map_index(stops)
    id_to_index = {s.id: s.index_in_list for s in stops}

    # ===== Route 1 =====
    r1_stop_ids = ["A", "B", "C", "D"]
    r1_stop_index_list = [id_to_index[sid] for sid in r1_stop_ids]

    route1 = Route(
        name="Route 1",
        id="R1",
        stop_list=r1_stop_ids,
        stop_index_list=r1_stop_index_list,
        trips=[]
    )

    # Trips for R1 -> very slow trips (10mn between each stop)
    route1.add_trip(
        Trip(
            id="R1_T1",
            departure_times=[10, 20, 30, 40],
            arrival_times=[10, 20, 30, 40],
        )
    )
    route1.add_trip(
        Trip(
            id="R1_T2",
            departure_times=[20, 30, 40, 50],
            arrival_times=[20, 30, 40, 50],
        )
    )

    # ===== Route 2 =====
    r2_stop_ids = ["A", "E", "F","G"]
    r2_stop_index_list = [id_to_index[sid] for sid in r2_stop_ids]

    route2 = Route(
        name="Route 2",
        id="R2",
        stop_list=r2_stop_ids,
        stop_index_list=r2_stop_index_list,
        trips=[]
    )

    # R2 trips: very fast train (2 minutes between stops)
    # Idea: go faster than route 1 by changing at stop F
    route2.add_trip(
        Trip(
            id="R2_T1",
            departure_times=[10, 12, 14, 16],
            arrival_times=[10, 12, 14, 16],
        )
    )

    route2.add_trip(
        Trip(
            id="R2_T2",
            departure_times=[12, 14, 16, 18],
            arrival_times=[12, 14, 16, 18],
        )
    )

    # ===== Route 3 =====
    r3_stop_ids = ["H", "E", "F","D"]
    r3_stop_index_list = [id_to_index[sid] for sid in r3_stop_ids]

    route3 = Route(
        name="Route 3",
        id="R3",
        stop_list=r3_stop_ids,
        stop_index_list=r3_stop_index_list,
        trips=[]
    )

    # Only one trip: can be caught with R2 by taking the second trip, not the first
    # Enable to check is the algorithm really finds the best solution (not trivial)
    route3.add_trip(
        Trip(
            id="R3_T1",
            departure_times=[10, 12, 13, 16],
            arrival_times=[485, 490, 495],
        )
    )

    # Combine routes and return dataset
    routes = [route1, route2, route3]
    map_index(routes)

    return {
        "stop_list": stops,
        "route_list": routes
    }