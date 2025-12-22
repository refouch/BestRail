from .raptor import RAPTOR, get_all_paths
from .postprocessing import rank_by_time, jsonify_paths
from .preprocessing import load_gtfs_data

def print_matrix(tau):
    for line in tau:
        print(line)

gtfs_dir = 'gtfs_sncf'

stop_list, route_list = load_gtfs_data(gtfs_dir)

source_stop = stop_list[2932]
target_stop = stop_list[2822]

tau, tau_star, parent = RAPTOR(source_stop,target_stop,0,stop_list,route_list)

paths = get_all_paths(parent,tau,2822,5)
paths = rank_by_time(paths)

final_dict = jsonify_paths(paths,stop_list)

print(final_dict)
