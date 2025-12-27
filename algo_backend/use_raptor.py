from .raptor import RAPTOR, paths_in_time_range
from .postprocessing import rank_by_time, jsonify_paths
from .preprocessing import load_gtfs_data
import logging

logging.basicConfig(level=logging.INFO)

def print_matrix(tau):
    for line in tau:
        print(line)

gtfs_dir = 'gtfs_sncf'

stop_list, route_list, stop_dict = load_gtfs_data(gtfs_dir)
print(stop_dict['StopArea:OCE87726414'])
source_stop = stop_list[2932]
target_stop = stop_list[2822]

print(stop_list[2932].name)
print(stop_list[2822].name)

# tau, tau_star, parent = RAPTOR(source_stop,target_stop,0,stop_list,route_list)

# paths = get_all_paths(parent,tau,2822,5)
paths = paths_in_time_range(600,source_stop,target_stop,stop_list,route_list,rounds=5)
paths = rank_by_time(paths)

final_dict = jsonify_paths(paths,stop_list)

print(paths)
print(final_dict)
