import pytest
from algo_backend.raptor import RAPTOR, get_unique_paths 
from algo_backend.mock_dataset import build_mock_data
from algo_backend.postprocessing import rank_by_time, extract_train_info, jsonify_paths

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

def test_rerank(dataset):
    tau, tau_star, parent = run_raptor(dataset, "A", "D", departure_time=0)
    paths = get_unique_paths(parent,tau,3,5)
    paths = rank_by_time(paths)
    assert paths[0] == [{'stop': 4, 'route_id': 'R2', 'trip_id': 'R2_T1', 'board_stop': 0, 'board_time': 10, 'arrival_time': 12}, {'stop': 3, 'route_id': 'R3', 'trip_id': 'R3_T1', 'board_stop': 4, 'board_time': 14, 'arrival_time': 24}]

def test_info_extraction():
    train_id = 'OCESN117777F1187_F:TER:FR:Line::B10C45A0-C32C-4232-85F2-4BB81B810084::87713040:87723197:10:2044:20260621'
    info = extract_train_info(train_id)
    assert info == 'TER n°117777'

def test_formatting(dataset):
    tau, tau_star, parent = run_raptor(dataset, "A", "D", departure_time=0)
    paths = get_unique_paths(parent,tau,3,5)
    json = jsonify_paths(paths,dataset['stop_list'])

    assert type(json) == list
    assert json[0].get('departure_stop') == 'Stop A'
    assert len(json[0].get('segments')) == 1

def test_duplicate(dataset):
    tau, tau_star, parent = run_raptor(dataset, "A", "D", departure_time=0)
    paths = get_unique_paths(parent,tau,3,5)

    paths2 = paths.copy()
    paths.extend(paths2)

    json = jsonify_paths(paths,dataset['stop_list'])

    assert len(paths) == 4
    assert len(json) == 2

