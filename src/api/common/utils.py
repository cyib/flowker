from collections import defaultdict
from itertools import groupby

def compare_versions(version1, version2):
    v1 = list(map(int, version1.split('.')))
    v2 = list(map(int, version2.split('.')))
    
    for i in range(3):
        if v1[i] > v2[i]:
            return version1
        elif v1[i] < v2[i]:
            return version2

    return version1

def filter_nodes_by_version(nodes, groupers):
    node_dict = defaultdict(list)

    for node in nodes:
        key = tuple(getattr(node, grouper) for grouper in groupers)
        node_dict[key].append(node)

    unique_nodes = []

    for node_list in node_dict.values():
        max_node = max(node_list, key=lambda node: node.nodeVersion)
        unique_nodes.append(max_node)

    return unique_nodes

def groupByKey(arr, key):
    arr.sort(key=lambda x: x[key])
    return {k: list(v) for k, v in groupby(arr, key=lambda x: x[key])}

def mergeDicts(*args):
    result = {}
    for dictionary in args:
        result = {**result, **dictionary}
    return result