##########################################################
### "Homemade" implementation of the RAPTOR algorithm. ###
### Following this article: https://www.microsoft.com/en-us/research/wp-content/uploads/2012/01/raptor_alenex.pdf
##########################################################

from algo_backend.data_structure import Stop, Route, Trip, map_stop_to_routes
from typing import Dict, List, Optional, Tuple

def earliest_trip_at_stop(route: Route, stop_rank: int, time_at_stop: float) -> Optional[Trip]:
    """Function to determine the first trip that can be caught for a given stop and in the route and a given time
    (define as 'et' in the paper)"""

    for trip in route.trips:
        train_leave_time = trip.departure_times[stop_rank]

        if time_at_stop <= train_leave_time:
            return trip # trip can be caught.
        
    return None

def check_earlier_stops(queue: List[Tuple[Route,Stop]], route: Route, stop: Stop) -> Optional[List[Tuple[Route,Stop]]]:
    """Function to check if there is an earlier stop already in the queue"""
    for i, (route_in_Q, stop_in_Q) in enumerate(queue):
        if route_in_Q.id == route.id:

            if route.stop_list.index(stop.id) < route_in_Q.stop_list.index(stop_in_Q.id):
                queue[i] = (route,stop)
            return queue
    
    return None

def RAPTOR(source_stop: Stop, target_stop: Stop, 
           departure_time: float, 
           stop_list: List[Stop], route_list: List[Route], max_rounds: int = 5) -> Dict:

    ### First part: Initialization
    num_stops = len(stop_list)
    tau_matrix = [[float('inf')] * (max_rounds + 1) for _ in range(num_stops)] # represents τi for each stop in the paper
    tau_star = [float('inf') for _ in range(num_stops)]

    tau_matrix[source_stop.index_in_list][0] = departure_time #τ0(ps) = τ
    tau_star[source_stop.index_in_list] = departure_time

    parent = [[None] * (max_rounds + 1) for _ in range(num_stops)] # Store parent stop/trip for each better stop in order to backtrack the path
    parent[source_stop.index_in_list][0] = { # Initialize first stop
    "prev_stop": None,
    "route_id": None,
    "route": None,
    "trip_id": None,
    "board_stop": None, # The stop we boarded the trip in
    "board_time": None
}

    stops_to_routes = map_stop_to_routes(stop_list,route_list)

    route_queue = list()
    marked_stops = set()

    marked_stops.add(source_stop.index_in_list)

    for k in range(1, max_rounds + 1):

        route_queue.clear()

        current_marked = marked_stops.copy()
        marked_stops.clear()

        for stop_index in current_marked:

            stop = stop_list[stop_index]

            for route_index in stops_to_routes[stop_index]:

                route = route_list[route_index]

                update_queue = check_earlier_stops(route_queue,route,stop)

                if type(update_queue) == list:
                    route_queue = update_queue
                
                else:
                    route_queue.append((route,stop))
            
        for route, first_stop in route_queue:

            current_trip = None

            first_stop_rank = route.stop_list.index(first_stop.id)

            for rank, stop_index in enumerate(route.stop_index_list[first_stop_rank:], start=first_stop_rank):

                stop = stop_list[stop_index]

                if current_trip is not None:

                    arrival_time = current_trip.arrival_times[rank] 

                    if arrival_time < tau_star[stop_index]:
                        tau_matrix[stop_index][k] = arrival_time
                        tau_star[stop_index] = arrival_time
                        marked_stops.add(stop_index)

                        parent[stop_index][k] = {
                            "prev_stop": route.stop_index_list[rank - 1] if rank > first_stop_rank else None,
                            "route": route.index_in_list,
                            "route_id": route.id,
                            "trip_id": current_trip.id,
                            "board_stop": first_stop.index_in_list,
                            "board_time": current_trip.departure_times[first_stop_rank]
                        }

                # Can we catch an earlier train
                if stop_index == source_stop.index_in_list:
                    ready_time = departure_time
                else:
                    ready_time = tau_matrix[stop_index][k-1] + stop.min_transfer_time

                # Can we board a new trip?
                if current_trip is None or ready_time <= current_trip.departure_times[rank]:
                    current_trip = earliest_trip_at_stop(route, rank, ready_time)

        # Stopping criterion
        if not marked_stops:
            return tau_matrix, tau_star, parent


def reconstruct_path(parent: List[List[Dict]], tau_matrix: List[List[int]], target_idx: int, round: int) -> List[Dict]:
    """Function to reconstruct the path leading to the target stop for a given round usging RAPTOR results"""
    path = []
    current_stop = target_idx
    k = round

    while True:
        label = parent[current_stop][k]
        if label is None:
            break

        path.append({
            "stop": current_stop,
            "route_id": label["route_id"],
            "route": label["route"],
            "trip_id": label["trip_id"],
            "board_stop": label["board_stop"],
            "board_time": label['board_time'],
            "arrival_time": tau_matrix[current_stop][k],
        })

        if label["board_stop"] is None:
            break

        current_stop = label["board_stop"]
        k = k-1

    path.reverse()
    return path

def get_all_paths(parent: List[List[Dict]], tau_matrix: List[List[int]], target_idx: int, max_rounds: int) -> List[List[Dict]]:
    """Helper function to reconstruct all valid paths leading to the target stop"""

    paths = []

    for k in range(1, max_rounds + 1):

        path = reconstruct_path(parent,tau_matrix,target_idx,k)

        if not path:
            break
        
        paths.append(path)
    
    return paths
