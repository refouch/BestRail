import pytest
from algo_backend.raptor import RAPTOR, get_unique_paths 
from algo_backend.mock_dataset import build_mock_data


@pytest.fixture
def dataset():
    return build_mock_data()


def run_raptor(dataset, source_id, target_id, departure_time, max_rounds=6):
    stops = dataset["stop_list"]
    routes = dataset["route_list"]

    source = next(s for s in stops if s.id == source_id)
    target = next(s for s in stops if s.id == target_id)

    tau_matrix, tau_star, parent = RAPTOR(
        source_stop=source,
        target_stop=target,
        departure_time=departure_time,
        stop_list=stops,
        route_list=routes,
        max_rounds=max_rounds
    )
    return tau_matrix, tau_star, parent

# Direct trip via R1
def test_direct_trip(dataset):
    tau, tau_star, parent = run_raptor(dataset, "A", "D", departure_time=0)
    assert tau[3][1] == 40 # Result for stop D at round 1 is arrival time = 40

def test_multiple_trips(dataset):
    tau, tau_star, parent = run_raptor(dataset, "A", "D", departure_time=0)
    tauD = sorted(tau[3])
    assert tauD[0] != float('inf') and tauD[1] != float('inf')

def test_faster_trip(dataset):
    tau, tau_star, parent = run_raptor(dataset, "A", "D", departure_time=0)
    tauD = tau[3]
    tauD_star = min(tauD)
    assert tauD_star == 24 and tauD.index(tauD_star) == 2 # Best time is achieved in 24 minutes at round 2

def test_impossible_trip(dataset):
    tau, tau_star, parent = run_raptor(dataset, "B", "G", departure_time=0) # B -> D is impossible 
    assert all(time == float('inf') for time in tau[6])

def test_backtracking(dataset):
    tau, tau_star, parent = run_raptor(dataset, "A", "D", departure_time=0)
    paths = get_unique_paths(parent,tau,3,5)
    assert paths[0] == [{'stop': 3, 'route_id': 'R1', 'trip_id': 'R1_T1', 'board_stop': 0, 'board_time': 10, 'arrival_time': 40}]
