import os
import math
import logging
from typing import List
import numpy as np
import cvxpy as cp
import time
#print(cp.installed_solvers())

from generic import (
    BaseContainer,
    FlowLinkSendHolder,
    CollectiveGroupContainer,
    FlowCGHolder,
)
from utils import save_alloc_solutions
from opt_utils import get_group_flows

def get_bottleneck_link_capacity(fl_s_holder: FlowLinkSendHolder, flow_idx): # 找到bottleneck link的capacity
    link_capacity = min([c for c in fl_s_holder.capacity_matrix[flow_idx] if c!=0])
    if not link_capacity:
        return 0
    return link_capacity

def flow_chunk_optimization(
    flow_container: BaseContainer,
    link_container: BaseContainer,
    fl_s_holder: FlowLinkSendHolder,
    cg_container: CollectiveGroupContainer,
    fcg_holder: FlowCGHolder,
    opt_config: dict,
):
    """
    将每个流拆成若干块：
      1. 每条流(k,n,i,j) 的数据量 F(k,n,i,j) 被拆成数据量/bottleneck流量个parts
      2. 同一流的块 p 必须在块 p-1 完成之后才能发送
      3. Objective：最小化各 collective 的average completion time
    """
    start_time = time.time()
    logging.info("**** Start Flow Chunk Optimization ****")
    save_path = opt_config.get("model_path", "./")
    os.makedirs(save_path, exist_ok=True)

    # 1 Basic settings
    K = cg_container.K             # collective 数量
    Nks = cg_container.Nks         # 每个 collective 的 group 数量
    F = fl_s_holder.fl_holder.F    # 流的总数 (原始 flow)
    E = fl_s_holder.fl_holder.E    # link数量
    flow_objs = flow_container.item_objs
    link_objs = link_container.item_objs

    # 2. 设定vars: X(k,n,i,j,o,t)
    x = {}
    f2l = fl_s_holder.fl_holder.f2l_mapper
    flow_datas = np.array([flow.data_volume for flow in flow_objs]) #[150  50  50 100]

    constraints = []
    edge_record = {}
    link_constraint_check_list = {}
    for flow_idx, flow in enumerate(fcg_holder.matrix):
        k = flow[0]
        n = flow[1]
        order = flow[2]
        flow_key = fl_s_holder.fl_holder.flow_ids[flow_idx]
        source_link, dest_link = f2l[flow_key][0], f2l[flow_key][-1]
        num_part = math.ceil(flow_datas[flow_idx]/get_bottleneck_link_capacity(fl_s_holder, flow_idx))
        edge_record[(k, n, source_link, dest_link, order)] = fl_s_holder.f2l_mapper[f"{k}-{n}-{flow_idx + 1}"] # f2l_mapper={'1-1-1': [1, 2, 3, 4], '1-2-2': [5, 6, 2, 7, 9], '1-2-3': [5, 10, 11], '2-3-4': [12, 10, 11]}

    for flow_idx, flow in enumerate(fcg_holder.matrix): #array([[1, 1, 0], [1, 2, 0], [1, 2, 1],[2, 3, 0]]))
        k = flow[0]
        n = flow[1]
        order = flow[2]
        flow_key = fl_s_holder.fl_holder.flow_ids[flow_idx]
        source_link, dest_link = f2l[flow_key][0], f2l[flow_key][-1]
        num_part = math.ceil(flow_datas[flow_idx]/get_bottleneck_link_capacity(fl_s_holder, flow_idx))
        key1 = (k, n, source_link, dest_link, order) #当前的key
        # edge_record[key1] = fl_s_holder.f2l_mapper[f"{k}-{n}-{flow_idx + 1}"]
        for part in range(1, int(num_part) + 1):
            x[(k, n, source_link, dest_link, order, part)] = cp.Variable(nonneg=True, name=f"x_k{k}_n{n}_i{source_link}_j{dest_link}_o{order}_p{part}")
            for key2 in edge_record: #check其他的flow有没有和当前flow有一样的edge
                if key1 != key2:
                    common_elements = set(edge_record[key1]) & set(edge_record[key2])
                    if common_elements:
                        #print(f"key1:{key1},key2:{key2}")
                        if key2 not in link_constraint_check_list:
                            # link_constraint_check_list.setdefault(key2, set()).add(key1 + (part,))  # 用集合避免重复
                            link_constraint_check_list[key2] = []
                            link_constraint_check_list[key2].append(key1 + (part,))
                        else:
                            # link_constraint_check_list.setdefault(key2, set()).add(key1 + (part,))  # 用集合避免重复
                            link_constraint_check_list[key2].append(key1 + (part,))
    # print(link_constraint_check_list)

    #print(f"x example:{x[(1,1,1,4,0,1)]}")
    # 3. Objective function: min sum(T_k), where T_k >=X(k, n, i, j , p) for all n, i, j, p
    T = {} # Construct a set of helper variables (T_k >= 第k个collective里最后被发出去的流的时间)
    for k_idx in range(K):
        T[k_idx + 1] = cp.Variable(nonneg=True, name=f"T_k{k_idx + 1}")
    current_k, current_n, current_order = 0, 0, 0 # just initialize
    for (k, n, i, j, o, p), x_var in x.items(): # (1 1 1 4 0 0): k, n, i, j, o, p
        constraints.append(x_var >= 1) # sending completion constraint (trivial)
        constraints.append(T[k] >= x_var) # helper for objective function
        # if p == 1:
        #     current_record = x_var # 记录一下当前时间的x_var
        if p >= 2:
            prev_var = x[(k, n, i, j, o, p-1)]
            constraints.append(x_var == prev_var + 1) # 新的时刻（下一秒）一定大于上一秒那块流被发送的时刻：>= or =?流一定要连着嘛
            # current_record = x_var
        b = [cp.Variable(boolean=True) for _ in range(100)]
        M = 1000
        count = 0
        if (k, n, i, j, o) in link_constraint_check_list:
            if link_constraint_check_list[(k, n, i, j, o)] != []:
                #print(f"x var now is:{x_var}")
                for var in link_constraint_check_list[(k, n, i, j, o)]:
                    #print(f"each var:{var}")
                    constraints.append((x_var - x[var]) >= 1 - M*(1-b[count]))
                    constraints.append((x_var - x[var]) <= -1 + M*b[count])
                    count += 1

        if o == 0:
            current_order = 0
            current_k, current_n = k, n
            # current_dependency_var = x[(k, n, i, j, o, p)] #Dependence constraint: 0先走 1后走
            current_dependency_var = x[(k, n, i, j, o, 1)] #Dependence constraint: 1先走 0后走

        if o > current_order:
            #print("now k,n,i,j,p:", (k,n,i,j,o,p))
            if k == current_k and n == current_n:
                # constraints.append(x_var >= current_dependency_var + 1) # Dependence constraint: 0先走1后走
                constraints.append(x_var + 1 <= current_dependency_var) # Dependence constraint, 1先走0后走

                if (k, n, i, j, o, p+1) not in x:
                    current_order = o

    objective = cp.Minimize(cp.sum([T[k] for k in range(1, K+1)])) # minimize所有collective的完成时间

    # Solve
    prob = cp.Problem(objective, constraints)
    logging.info("-----> Building MILP for chunk-based scheduling done, start solving...")
    solver_name = opt_config.get("solver", "HIGHS")  # 可以换成"CBC"或者"GLPK_MI"啥的(?
    # prob.solve(solver=solver_name)
    prob.solve()
    # print("b values:", [b_i.value for b_i in b])

    if prob.status == cp.OPTIMAL:
        print("\n========= Var Values =========")
    for (k, n, i, j, o, p), var in x.items():
        print((k, n, i, j, o, p))
        print(f"Flow(k={k}, n={n}, order={o}, part={p}) Starting time: {var.value:.1f}")
    objective_value = prob.value / K
    end_time = time.time()
    time_cost = end_time - start_time
    logging.info(f"Solver status: {prob.status}, objective value: {objective_value}, time cost: {time_cost}")
    return objective_value, time_cost
