"""
A session to run the experiments of the paper.
"""

import os
import json
import argparse
import logging
from typing import List

import numpy as np

from stellar import extract_information, perform_steller
from competitors import (
    data_aware_allocation,
    baseline_factory,
    barrier_aware_allocation,
)

from generic import BaseContainer, FlowCGHolder, CollectiveGroupContainer
from opt_utils import get_group_flows
from flow_chunk_competitor import flow_chunk_optimization

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def add_bps_config(
    config_path: str,
    filename: str,
    optimized_kn_rates: List[np.ndarray],
    flow_container: BaseContainer,
    fcg_holder: FlowCGHolder,
    cg_container: CollectiveGroupContainer,
    model_path: str,
):
    """Add the bps term (flow rate) to each flow of the config."""
    file_path = os.path.join(config_path, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        info_data = json.load(f)

    K = cg_container.K
    Nks = cg_container.Nks

    for k in range(K):
        for n in range(Nks[k]):
            bps_mb = optimized_kn_rates[k][n]
            # bps = bps_mb * 1000000
            bps = round(bps_mb * 8 * 1024 * 1024)
            flow_indxes = get_group_flows(k, n, fcg_holder.matrix, cg_container)
            for idx in flow_indxes:
                flow_id = flow_container.item_obj(idx).id
                # Add the flow rate of each flow
                info_data[flow_id]["bps"] = bps

    # Save the new configuration to the result
    filename = os.path.basename(filename)
    result_path = os.path.join(model_path, f"Optimized-{filename}")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(info_data, f, indent=4)

    logging.info("%sOptimized %s saved at %s", "*" * 15, filename, result_path)


def _main():
    """Run the experiment."""
    # Extract the parse arguments
    parser = argparse.ArgumentParser(description="Process some files.")
    # Define the -b and -c arguments
    parser.add_argument(
        "-r", "--results", type=str, required=True, help="Path to results"
    )
    parser.add_argument(
        "-c", "--config", type=str, required=True, help="Path to config file"
    )
    parser.add_argument(
        "-o",
        "--optconfig",
        type=str,
        required=True,
        help="Path to config file for the optimization",
    )
    parser.add_argument(
        "-p",
        "--project",
        type=str,
        required=True,
        help="Path to config file for the optimization",
    )
    parser.add_argument(
        "-m",
        "--method",
        type=str,
        required=True,
        help="Method used to optimize the flow rates",
    )

    # Get the directory of the current script
    script_path = os.path.abspath(__file__)
    base_path = os.path.dirname(script_path)
    config_foldername = "configs"

    # Parse the arguments
    args = parser.parse_args()
    result_path = args.results
    proj_name = args.project
    config_name = args.config
    optconfig_name = args.optconfig
    method_name = args.method

    # Extract the basic settings
    config_folder_path = os.path.join(base_path, config_foldername)
    optconfig_path = os.path.join(base_path, config_foldername, optconfig_name)
    info = extract_information(config_folder_path, config_name)

    # Extract the config for the optimization
    with open(optconfig_path, "r", encoding="utf-8") as f:
        opt_parameters = json.load(f)

    project_path = os.path.join(result_path, proj_name, method_name)
    opt_parameters["model_path"] = project_path
    os.makedirs(opt_parameters["model_path"], exist_ok=True)

    if method_name == "steller":
        # Obtained the optimized flow rates for groups of collectives
        # len(optimized_kn_rates) == K, where K is the number of collectives
        # len(optimized_kn_rates[k]) == Nk, where Nk is the number of groups in the k-th collective
        optimized_kn_rates, time_cost = perform_steller(
            flow_container=info[0],
            link_container=info[1],
            fl_s_holder=info[2],
            cg_container=info[3],
            fcg_holder=info[4],
            opt_config=opt_parameters,
        )

    if method_name == "barrierAwareAlloc":
        optimized_kn_rates, time_cost = barrier_aware_allocation(
            flow_container=info[0],
            link_container=info[1],
            fl_s_holder=info[2],
            cg_container=info[3],
            fcg_holder=info[4],
            opt_config=opt_parameters,
        )

    if method_name == "dataAwareAlloc":
        optimized_kn_rates, time_cost = data_aware_allocation(
            flow_container=info[0],
            link_container=info[1],
            fl_s_holder=info[2],
            cg_container=info[3],
            fcg_holder=info[4],
            opt_config=opt_parameters,
        )

    if method_name == "flowChunk":
        objective_value, time_cost = flow_chunk_optimization(
            flow_container=info[0],
            link_container=info[1],
            fl_s_holder=info[2],
            cg_container=info[3],
            fcg_holder=info[4],
            opt_config=opt_parameters,
        )

    if method_name != "flowChunk":
        add_bps_config(
            config_folder_path,
            config_name,
            optimized_kn_rates,
            info[0],
            info[4],
            info[3],
            opt_parameters["model_path"],
        )

    # Save the time cost of the optimization under results
    with open(
        os.path.join(opt_parameters["model_path"], "time_cost.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump({"time_cost": time_cost}, f, indent=4)

    logging.info("%s %s Done.", "*" * 15, proj_name)


if __name__ == "__main__":
    _main()
