"""
A session to run the idea(s) on new setting
"""

import os
import json
import argparse
import logging
from typing import List
from collections import defaultdict, deque
import numpy as np

from new_setting import *
from stellar import perform_steller
from optimized_flow_chunk_competitor import flow_chunk_optimization

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def extract_information(config_path: str, filename: str):
    """Extracting the information from the configuration file."""
    # load the json to dict
    file_path = os.path.join(config_path, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        info_data = json.load(f)
    return info_data

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
    # optconfig_name = args.optconfig
    method_name = args.method

    # Extract the basic settings
    config_folder_path = os.path.join(base_path, config_foldername)
    optconfig_path = os.path.join(base_path, config_foldername) #, optconfig_name)
    info = extract_information(config_folder_path, config_name)

    flow_info = get_flow_info(info) # flow info in the order of each flow
    link_cap = info.get("link_capacities") # link capacities
    dependency_order = get_dependency_order(flow_info) # dep orders, e.g. {(1, 1): ['1'], (1, 2): ['3', '2'], (2, 3): ['4']}

    project_path = os.path.join(result_path, proj_name, method_name)
    os.makedirs(project_path, exist_ok = True)  #./new/toyExample/flowChunk
    if method_name == "flowChunk":
        result = flow_chunk_optimization(flow_info, link_cap, dependency_order)

    output_file = os.path.join(project_path, "result.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    logging.info("%s %s Done.", "*" * 15, proj_name)

if __name__ == "__main__":
    _main()