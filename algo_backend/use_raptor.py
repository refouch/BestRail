from .mock_dataset import build_mock_data
from .raptor import RAPTOR, get_all_paths
from .postprocessing import rank_by_time, jsonify_paths

def print_matrix(tau):
    for line in tau:
        print(line)

dataset = build_mock_data()

stop_list = dataset.get("stop_list")
route_list = dataset.get("route_list")

source_stop = stop_list[0]
target_stop = stop_list[3]

tau, tau_star, parent = RAPTOR(source_stop,target_stop,0,stop_list,route_list)

paths = get_all_paths(parent,tau,3,5)
paths = rank_by_time(paths)

final_dict = jsonify_paths(paths,stop_list)

print(final_dict)
