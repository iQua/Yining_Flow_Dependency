import os
import math
import logging
from typing import List
import numpy as np
import cvxpy as cp
import operator
import time
#print(cp.installed_solvers())

from utils import save_alloc_solutions
from opt_utils import get_group_flows

def get_bottleneck_link_capacity(link_set, link_cap): # 找到bottleneck link的capacity
    # print(f"link set is:{link_set}")
    min_key, bottleneck = min(((str(key), link_cap[str(key)]) for key in link_set), key=lambda x: x[1])
    if not bottleneck:
        return 0
    return bottleneck/1024/1024/8

def flow_chunk_optimization(flow_info, link_cap, depency_order):
    start_time = time.time()
    logging.info('**** Start Flow Chunk Optimization ****')
    last_key = next(reversed(flow_info))
    K = flow_info[last_key]['collective']

    # Step 1: Create Variables X(k,n,i,j,o,t)
    x = {}
    constraints = []
    for flow in flow_info:
        num_part = math.ceil(flow_info[flow]["data_size"]/get_bottleneck_link_capacity(link_set=flow_info[flow]["links"], link_cap=link_cap))
        k = flow_info[flow]['collective']
        n = flow_info[flow]['group']
        source = flow_info[flow]['source']
        dest = flow_info[flow]['dest']
        order = depency_order[(k,n)].index(flow) + 1
        print(f"flow:{flow}, order:{order}")
        for part in range(1, num_part + 1):
            x[(k, n, source, dest, order, part)] = cp.Variable(nonneg = True, name = f"x_k{k}_n{n}_i{source}_j{dest}_o{order}_t{part}")

