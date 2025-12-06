from mock_dataset import build_mock_data
from raptor import RAPTOR

dataset = build_mock_data()

stop_list = dataset.get("stop_list")
route_list = dataset.get("route_list")

source_stop = stop_list[1]
target_stop = stop_list[5]

tau = RAPTOR(source_stop,target_stop,0,stop_list,route_list)

print(f'{[line for line in tau]}\n')
