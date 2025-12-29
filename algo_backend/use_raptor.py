from .raptor import RAPTOR, paths_in_time_range, get_unique_paths
from .mock_dataset import build_mock_data
from .postprocessing import rank_by_time, jsonify_paths
from .preprocessing import load_gtfs_data

def print_matrix(tau):
    for line in tau:
        print(line)

gtfs_dir = 'gtfs_sncf'

dataset = build_mock_data()

stop_list = dataset['stop_list']
route_list = dataset['route_list']

source_stop = stop_list[0]
target_stop = stop_list[3]

tau, tau_star, parent = RAPTOR(source_stop,target_stop,0,stop_list,route_list)

paths = get_unique_paths(parent,tau,3,5)

paths = rank_by_time(paths)

final_dict = jsonify_paths(paths,stop_list)

print(paths)
print(final_dict)
