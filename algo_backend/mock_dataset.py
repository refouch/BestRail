### AI-generated mock dataset to test the algorithm

from data_structure import Route, Stop, Trip, map_index
from typing import List

def build_mock_data():
    """
    Enhanced RAPTOR test network.
    
    Includes:
    - Branching routes
    - Multiple possible journeys
    - Non-reachable stops
    - Overtaking trips
    - Several transfer points
    - Different transfer times
    
    Network layout (stops):

         R1:  S0 -- S1 -- S2 -- S3
                   |
         R3:       S6 -- S7

         R2:       S2 -- S4 -- S5

         R4:  S8 -- S9   (completely isolated, unreachable)

         R5:  S3 -- S10 -- S11  (continuation of R1)

    """

    # -------- STOPS --------
    stops: List[Stop] = [
        Stop("Stop 0",  "S0", 48, 2, 0),
        Stop("Stop 1",  "S1", 48, 2, 2),
        Stop("Stop 2",  "S2", 48, 2, 3),
        Stop("Stop 3",  "S3", 48, 2, 1),
        Stop("Stop 4",  "S4", 48, 2, 0),
        Stop("Stop 5",  "S5", 48, 2, 0),
        Stop("Stop 6",  "S6", 48, 2, 2),
        Stop("Stop 7",  "S7", 48, 2, 0),
        Stop("Stop 8",  "S8", 48, 2, 1),
        Stop("Stop 9",  "S9", 48, 2, 1),
        Stop("Stop 10", "S10",48, 2, 2),
        Stop("Stop 11", "S11",48, 2, 0),
    ]

    map_index(stops)
    id2idx = {s.id: s.index_in_list for s in stops}

    routes = []

    # -------- ROUTE R1 (S0 → S3) --------
    R1_ids = ["S0","S1","S2","S3"]
    R1_idx = [id2idx[x] for x in R1_ids]

    R1 = Route("Route 1", "R1", R1_ids, R1_idx, trips=[])

    # Two trips — second arrives earlier at S3 → overtaking case
    R1.add_trip(Trip(
        "R1_T1",  # slow trip
        departure_times=[480, 485, 490, 500],  # 08:00 → 08:20
        arrival_times=[480, 485, 490, 500]
    ))
    R1.add_trip(Trip(
        "R1_T2",  # faster trip
        departure_times=[485, 487, 492, 497],  # 08:05 → 08:17
        arrival_times=[485, 487, 492, 497]
    ))
    routes.append(R1)

    # -------- ROUTE R2 (S2 → S5) --------
    R2_ids = ["S2","S4","S5"]
    R2_idx = [id2idx[x] for x in R2_ids]

    R2 = Route("Route 2", "R2", R2_ids, R2_idx, trips=[])

    R2.add_trip(Trip(
        "R2_T1",
        departure_times=[492, 498, 505],   # 08:12 from S2
        arrival_times=[492, 498, 505],
    ))
    R2.add_trip(Trip(
        "R2_T2",
        departure_times=[520, 526, 533],   # 08:40 from S2
        arrival_times=[520, 526, 533],
    ))
    routes.append(R2)

    # -------- ROUTE R3 (S1 → S7) --------
    R3_ids = ["S1","S6","S7"]
    R3_idx = [id2idx[x] for x in R3_ids]

    R3 = Route("Route 3", "R3", R3_ids, R3_idx, trips=[])

    R3.add_trip(Trip(
        "R3_T1",
        departure_times=[486, 493, 500],  # 08:06 from S1
        arrival_times=[486, 493, 500],
    ))
    routes.append(R3)

    # -------- ROUTE R4 (S8 → S9) - unreachable isolated route --------
    R4_ids = ["S8","S9"]
    R4_idx = [id2idx[x] for x in R4_ids]

    R4 = Route("Route 4", "R4", R4_ids, R4_idx, trips=[])

    R4.add_trip(Trip(
        "R4_T1",
        departure_times=[600, 610],
        arrival_times=[600, 610],
    ))
    routes.append(R4)

    # -------- ROUTE R5 (S3 → S11) continuation of R1 --------
    R5_ids = ["S3","S10","S11"]
    R5_idx = [id2idx[x] for x in R5_ids]

    R5 = Route("Route 5", "R5", R5_ids, R5_idx, trips=[])

    R5.add_trip(Trip(
        "R5_T1",
        departure_times=[501, 510, 520],  # connects nicely after R1_T1
        arrival_times=[501, 510, 520],
    ))
    R5.add_trip(Trip(
        "R5_T2",
        departure_times=[498, 508, 518],  # connects perfectly after R1_T2
        arrival_times=[498, 508, 518],
    ))
    routes.append(R5)

    # Index routes
    map_index(routes)

    return {
        "stop_list": stops,
        "route_list": routes
    }