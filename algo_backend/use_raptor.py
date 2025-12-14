from .mock_dataset import build_mock_data
from .raptor import RAPTOR, reconstruct_path

def print_matrix(tau):
    for line in tau:
        print(line)

dataset = build_mock_data()

stop_list = dataset.get("stop_list")
route_list = dataset.get("route_list")

source_stop = stop_list[0]
target_stop = stop_list[3]

tau, tau_star, parent = RAPTOR(source_stop,target_stop,0,stop_list,route_list)

path1 = reconstruct_path(parent,tau,3,1)

path2 = reconstruct_path(parent,tau,3,2)

print_matrix(tau)
print("=============")
print(tau_star)
print('===============')
print_matrix(parent)
print('============')
print(path1)
print(path2)
