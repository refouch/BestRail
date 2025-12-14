#########################################################################
### Module to tranform RAPTOR results into usable data for the server ###
#########################################################################

from typing import List, Dict
from .data_structure import Stop

def rank_by_time(paths: List[List[Dict]]) -> List[List[Dict]]:
    """Function to rerank paths in the list according to arrival time rather than number of rounds
        Simple imlementation using Merge Sort.
        """
    
    if len(paths) <= 1:
        return paths

    mid = len(paths) // 2
    left = rank_by_time(paths[:mid])
    right = rank_by_time(paths[mid:])

    print(left)

    return merge(left, right)


def merge(left: List[List[Dict]], right: List[List[Dict]]) -> List[List[Dict]]:
    """Merge fucntion for Merge Sort"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][-1].get('arrival_time') <= right[j][-1].get('arrival_time'):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def jsonify_paths(paths: List[List[Dict]], stop_list: List[Stop]):

    final_dict = {}

    for k, path in enumerate(paths):

        stops = []

        for label in path:

            stops.append(stop_list[label.get('stop')])

        departure_stop = stop_list[path[0].get('stop')]
        arrival_stop = stop_list[path[-1].get('stop')]

        final_dict[f'path {k}']