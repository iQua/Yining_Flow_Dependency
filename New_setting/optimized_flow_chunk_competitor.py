import os
import math
import logging
from typing import List
import numpy as np
import cvxpy as cp
import operator
from collections import defaultdict
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

def get_flows_with_same_links(flow_info): # for a non-concurrent setting
    edge_record = {}
    for idx_i, flow_i in flow_info.items():
        for idx_j, flow_j in flow_info.items():
            if idx_i < idx_j: # only check once
                common_links = flow_i['links'] & flow_j['links']
                if common_links:
                    print(idx_i, idx_j)
                    edge_record[idx_i] = idx_j
    return edge_record

def find_candidate_last_key(x_dict):
    """
    find the time variable that we send the last part of a flow
    """
    candidate_key = max(x_dict.keys(), key=lambda k: k[6])
    return candidate_key


def flow_chunk_optimization(flow_info, link_cap, depency_order):
    start_time = time.time()
    logging.info('**** Start Flow Chunk Optimization ****')
    last_key = next(reversed(flow_info))
    K = flow_info[last_key]['collective']
    
    # Create Variables X(k,n,i,j,o,p)
    x = {}
    x_record = {} # for recording each flow's variable
    constraints = []
    for flow_id, flow in flow_info.items():
        # print(flow)
        num_part = math.ceil(flow["data_size"]/get_bottleneck_link_capacity(link_set=flow["links"], link_cap=link_cap))
        k = flow['collective']
        n = flow['group']
        source = flow['source']
        dest = flow['dest']
        order = depency_order[(k,n)].index(flow_id) + 1
        # print(f"flow:{flow}, order:{order}")
        for part in range(1, num_part + 1):
            x[(flow_id, k, n, source, dest, order, part)] = cp.Variable(nonneg = True, name = f"x_fid_{flow_id}_k{k}_n{n}_i{source}_j{dest}_o{order}_p{part}")
            if flow_id not in x_record:
                x_record[flow_id] = {}
            key_tuple = (flow_id, k, n, source, dest, order, part)
            x_record[flow_id].setdefault(key_tuple, []).append(x[(flow_id, k, n, source, dest, order, part)])

            # constraints.append(x[(k, n, source, dest, order, part)] >= 1)


    # Objective function: min sum(T_k), where T_k >=X(k, n, i, j, o, p) for all n, i, j, o, p
    T = {} # Construct a set of helper variables (T_k >= The time we send the last part of the flow in collective k)
    edge_record = get_flows_with_same_links(flow_info) # Non-concurrent constraints

    for k_idx in range(K):
        T[k_idx + 1] = cp.Variable(nonneg=True, name=f"T_k{k_idx + 1}")
    current_k, current_n, current_order = 0, 0, 0 # just initialize

    for (fid, k, n, i, j, o, p), x_var in x.items(): # (1 1 1 4 0 0): k, n, i, j, o, t
        constraints.append(x_var >= 1) # sending completion constraint (trivial)
        constraints.append(T[k] >= x_var) # helper for objective function

        # if p == 1:
        #     current_record = x_var # record x_var at current time
        if p >= 2:
            prev_var = x[(fid, k, n, i, j, o, p-1)]
            constraints.append(x_var == prev_var + 1) # 新的时刻（下一秒）一定大于上一秒那块流被发送的时刻：>= or =?流一定要连着嘛


    # Dependency Constraints: first part of the current flow should be later than the last part of the previous flow
    for flow_id, flow in flow_info.items():
        k = flow['collective']
        n = flow['group']
        order = depency_order[(k,n)].index(flow_id) + 1
        # flow['dependency_order'] = order
        if order > 1: 
            k = flow['collective']
            n = flow['group']
            source = flow['source']
            dest = flow['dest']
            prev_flow_id = depency_order[(k, n)][order - 2] # get id of the last flow based on depency_order
            candidate_key = find_candidate_last_key(x_record[prev_flow_id]) # find the last part of the flow as a key from the previous flow
            current_key = (flow_id, k, n, source, dest, order, 1)
            constraints.append(x[current_key] >= x[candidate_key] + 1)

    # b = [cp.Variable(boolean=True) for _ in range(50)]
    # M = 1000
    # count = 0
    # for fid in edge_record:
    #     for flow in edge_record[fid]:
    #         print(f"each flow:{flow}")
    #         print(x_record[fid][0], x_record[flow][0])
    #         constraints.append((x_record[fid][0] - x_record[flow][0]) >= 1 - M*(1 - b[count]))
    #         # print(x_record)
    #         constraints.append((x_record[fid][0] - x_record[flow][0]) <= -1 + M*b[count])
    #         count += 1

    edge_record = get_flows_with_same_links(flow_info)
    M = 1000  
    for fid, other_list in edge_record.items():
        # find the first part and the last part for flow fid
        i_keys = list(x_record[fid].keys())
        i_start_key = min(i_keys, key=lambda k: k[6])
        i_finish_key = max(i_keys, key=lambda k: k[6])
        i_start = x[i_start_key]
        i_finish = x[i_finish_key]
        for other_flow in other_list:
            j_keys = list(x_record[other_flow].keys())
            j_start_key = min(j_keys, key=lambda k: k[6])
            j_finish_key = max(j_keys, key=lambda k: k[6])
            j_start = x[j_start_key]
            j_finish = x[j_finish_key]
            
            # Big M trick
            b = cp.Variable(boolean=True, name=f"order_{fid}_{other_flow}")
            # if y==1，current flow should be sent earlier than other_flow，where i_finish + 1 <= j_start
            # if y==0，other flow should be sent earlier than current flow，where j_finish + 1 <= i_start
            constraints.append(i_finish + 1 <= j_start + M*(1 - b))
            constraints.append(j_finish + 1 <= i_start + M*b)

    objective = cp.Minimize(cp.sum([T[k] for k in range(1, K+1)])) # minimize所有collective的完成时间
    
    # Solve
    prob = cp.Problem(objective, constraints)
    logging.info("-----> Building MILP for chunk-based scheduling done, start solving...")
    #solver_name = opt_config.get("solver", "HIGHS")  # 可以换成"CBC"或者"GLPK_MI"啥的(?
    # prob.solve(solver=solver_name)
    prob.solve()
    # print("b values:", [b_i.value for b_i in b])

    if prob.status == cp.OPTIMAL:
        print("\n========= Var Values =========")
    for (fid, k, n, i, j, o, p), var in x.items():
        print((fid, k, n, i, j, o, p))
        print(f"Flow(k={k}, n={n}, order={o}, part={p}) Starting time: {var.value:.1f}")
    objective_value = prob.value / K
    end_time = time.time()
    time_cost = end_time - start_time
    logging.info(f"Solver status: {prob.status}, objective value: {objective_value}, time cost: {time_cost}")
    return objective_value, time_cost