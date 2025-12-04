##########################################################
### "Homemade" implementation of the RAPTOR algorithm. ###
### Following this article: https://www.microsoft.com/en-us/research/wp-content/uploads/2012/01/raptor_alenex.pdf
##########################################################

from data_structure import Stop, Route, Trip, map_stop_to_routes
from typing import Dict, List, Optional

def earliest_trip_at_stop(route: Route, stop_rank: int, time_at_stop: float) -> Optional[Trip]:
    """Function to determine the first trip that can be caught for a given stop and in the route and a given time
    (define as 'et' in the paper)"""

    for trip in route.trips:
        train_leave_time = trip.departure_times[stop_rank]

        if time_at_stop <= train_leave_time:
            return trip # trip can be caught.
        
    return None

def check_earlier_stops(queue: List[(Route,Stop)], route: Route, stop: Stop) -> Optional[List[(Route,Stop)]]:
    """Function to check if there is an earlier stop we can catch on a given route"""
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

    stops_to_routes = map_stop_to_routes(stop_list,route_list)

    route_queue = list()
    marked_stops = list()

    marked_stops.add(source_stop.index_in_list)

    for k in range(1, max_rounds):

        route_queue.clear()

        for stop_index in marked_stops:

            stop = stop_list[stop_index]

            for route_index in stops_to_routes[stop_index]:

                route = route_list[route_index]

                update_queue = check_earlier_stops(route_queue,route,stop)

                if type(update_queue) == list:
                    route_queue = update_queue
                
                else:
                    route_queue.append((route,stop))
            
            marked_stops.remove(stop_index)
                 
        for route, first_stop in route_queue:

            current_trip = None

            stop_rank = route.stop_list.index(first_stop.id)

            for rank, stop_index in enumerate(route.stop_index_list[stop_rank+1:], start=stop_rank+1):

                stop = stop_list[stop_index]

                if current_trip is not None:
                    arrival_time = current_trip.arrival_times[rank] 
                    if arrival_time < min(tau_matrix[stop_index][k],tau_star[target_stop.index_in_list]):
                        tau_matrix[stop_index][k] = arrival_time
                        tau_star[stop_index] = arrival_time
                        marked_stops.append(stop_index)

                # Can we catch an earlier train
                time_at_stop = tau_matrix[stop_index][k-1] + stop.min_transfer_time

                current_trip = earliest_trip_at_stop(route,rank,time_at_stop)

        # Stopping criterion
        if not marked_stops:
            return tau_matrix


