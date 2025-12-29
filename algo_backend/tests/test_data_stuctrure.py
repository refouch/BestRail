import pytest

from algo_backend.data_structure import *

@pytest.fixture
def setup_data():
    # Stops
    stop1 = Stop(id="A", name="Stop A", lat=48.85, lon=2.35)
    stop2 = Stop(id="B", name="Stop B", lat=48.86, lon=2.36)
    stop3 = Stop(id="C", name="Stop C", lat=48.87, lon=2.37)
    stop_list = [stop1, stop2, stop3]

    # Route
    route = Route(id="R1", stop_list=["A","B","C"])
    route_list = [route]

    # Build stop_index_list
    stop_id_to_index = {stop.id: i for i, stop in enumerate(stop_list)}
    route.stop_index_list = [stop_id_to_index[sid] for sid in route.stop_list]

    # Trip
    trip = Trip(id="T1", arrival_times=[0,10,20], departure_times=[0,11,21])
    route.add_trip(trip)

    return stop_list, route_list, route, trip

def test_map_index(setup_data):
    stop_list, route_list, _, _ = setup_data
    # Clear indices
    for stop in stop_list:
        stop.index_in_list = None
    map_index(stop_list)
    map_index(route_list)
    assert [s.index_in_list for s in stop_list] == [0,1,2]
    assert [r.index_in_list for r in route_list] == [0]

def test_stop_to_routes(setup_data):
    stop_list, route_list, _, _ = setup_data
    stop_to_routes = map_stop_to_routes(stop_list, route_list)
    # Each stop is only on route 0
    assert stop_to_routes[0] == [0]
    assert stop_to_routes[1] == [0]
    assert stop_to_routes[2] == [0]

def test_trip_linked_to_route(setup_data):
    _, _, route, trip = setup_data
    assert trip in route.trips
    # Arrival/departure times must match number of stops
    assert len(trip.arrival_times) == len(route.stop_index_list)
    assert len(trip.departure_times) == len(route.stop_index_list)

def test_stop_index_list(setup_data):
    _, _, route, _ = setup_data
    assert route.stop_index_list == [0,1,2]
