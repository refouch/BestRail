from .mock_dataset import build_mock_data
from .raptor import RAPTOR

def print_tau_matrix(tau):
    for line in tau:
        print(line)

dataset = build_mock_data()

stop_list = dataset.get("stop_list")
route_list = dataset.get("route_list")

source_stop = stop_list[0]
target_stop = stop_list[3]

tau = RAPTOR(source_stop,target_stop,0,stop_list,route_list)

print_tau_matrix(tau)
