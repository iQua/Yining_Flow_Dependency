"""
New flow information setting, replacement of generic.py
"""

import os
import json
import argparse
import logging
from typing import List
from collections import defaultdict, deque
import numpy as np

def get_flow_info(info):
    """
    Summarize most of the flow information from the json file and store in a dict
    """
    flow_idx = [key for key in info if key.isdigit()]
    flow_info = {}
    link_cap = {}
    for flow in flow_idx:
        flow_info[flow] = {}
        flow_info.get(flow)['collective'] = info.get(flow)['collective_id']
        flow_info.get(flow)['group'] = info.get(flow)['group_id']
        flow_info.get(flow)['source'] = info.get(flow)['src']
        flow_info.get(flow)['dest'] = info.get(flow)['dst']
        flow_info.get(flow)['data_size'] = info.get(flow)['total']/1024/1024/8
        flow_info.get(flow)['links'] = set(info.get(flow)['links'])
    return flow_info

def dfs(current_flow, visited, graph, order):
    if current_flow in visited:
        return
    visited.add(current_flow)
    for depenency in graph[current_flow]:
        dfs(depenency, visited, graph, order)
    order.append(current_flow)
    return order

def get_dependency_order(flow_info):
    """
    Get each flow group's dependency order
    output -> {(1,1): ['1'], (1,2): ['3','2'], (2,3): ['4']}
    """
    groups = defaultdict(dict)
    for flow_id, flow in flow_info.items():
        groups[(flow["collective"], flow["group"])][flow_id] = flow

    dependency_orders = {}
    # key: (collective, group) value: flows
    for group_key, flows in groups.items(): # e.g. (k=1, n=2), {'1': {'collective': 1, 'group': 1, 'source': 1, 'dest': 10, 'data_size': 150.0, 'links': {1, 2, 3, 4}, 'dependency_order': []}})
        # Construct graph
        graph = {flow_id: [] for flow_id in flows}
        for flow_id, flow in flows.items():
            for dep in flow.get("dependency_order", []):
                # print("222: ", flow_id, dep)
                dep_str = str(dep)  # keep the keys as the same type
                if dep_str in flows:
                    graph[flow_id].append(dep_str) # ex_graph = {'2': ['4'], '3': ['5'], '4': ['3'], '5': []}
        visited = set()
        order = []
        for flow in graph:
            if flow not in visited:
                dfs(flow, visited, graph, order)
        dependency_orders[group_key] = order[::-1]

    return dependency_orders

def fid_to_order(dependency_orders):
    """
    input -> {(1,1): ['1'], (1,2): ['3','2'], (2,3): ['4']}
    output -> {'1': 1, '2': 2, '3': 1, '4': 1}
    """
    dep = {}
    for key, values in dependency_orders.items():
        for flow in values:
            dep.setdefault(flow, []).append(values.index(flow) + 1)
    return dep

            






# visited = set()
# order = []
# dependency_orders = {}

# ex_graph = {'2': ['4'], '3': ['5'], '4': ['3'], '5': []}
# for u in ex_graph:
#     if u not in visited:
#         dfs(u, visited, ex_graph, order)
# dependency_orders = order[::-1]
# print(dependency_orders)
