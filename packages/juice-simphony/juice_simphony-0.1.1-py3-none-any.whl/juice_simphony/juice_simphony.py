# *************************************************************************** #
# This file is subject to the terms and conditions defined in the             #
# file 'LICENSE.txt', which is part of this source code package.              #
#                                                                             #
# No part of the package, including this file, may be copied, modified,       #
# propagated, or distributed except according to the terms contained in       #
# the file 'LICENSE.txt'.                                                     #
#                                                                             #
# (C) Copyright European Space Agency, 2025                                   #
# *************************************************************************** #
import os
import json
from pathlib import Path
import shutil
from importlib import resources
from juice_simphony.CompositionEngine.Scenario.scenario import scenario
from juice_simphony.CompositionEngine.SegmentationImporter.restApiPlan import RestApiPlan


base_package = (__package__ or "").split(".")[0]
config_file_path = resources.files(base_package) / "data"
default_config_path = config_file_path / "config_scenario.json"

def expand_paths(config):
    """Recursively expand user (~) and environment variables ($VAR) in string paths"""
    if isinstance(config, dict):
        return {k: expand_paths(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [expand_paths(item) for item in config]
    elif isinstance(config, str):
        return os.path.expandvars(os.path.expanduser(config))
    else:
        return config

def load_parameters(file_name):
    with open(file_name) as json_file:
        raw_config = json.load(json_file)
    return expand_paths(raw_config)

def prepare_app_params(config, mapps=False, zip=False):
    # Resolve segment ID
    if "segment_id" in config:
        segment_id = config["segment_id"]
    elif "trajectory" in config and "mnemonic" in config:
        apiPlan = RestApiPlan("https://juicesoc.esac.esa.int/rest_api/")
        events_plan = apiPlan.get_trajectory(config["trajectory"], config["mnemonic"])
        if events_plan and isinstance(events_plan, list) and "id" in events_plan[0]:
            segment_id = events_plan[0]["id"]
        else:
            raise ValueError("No valid segment ID found in API response.")
    else:
        raise KeyError("Either 'segment_id' or both 'trajectory' and 'mnemonic' must be specified.")

    # Expand environment variables
    juice_conf = os.path.expandvars(config["juice_conf"])
    scenario_output = os.path.expandvars(config["output_folder"])
    kernel_path = os.path.expandvars(config["kernel_abs_path"])

    # Build full parameter dictionary
    return {
        "conf_repo": {"juice_conf": juice_conf},
        "scenario_generator": {"output_folder": scenario_output},
        "spice_info": {
            "kernel_abs_path": kernel_path,
            "spice_kernels_abs_path": kernel_path,
            "spice_tmp_abs_path": f"{scenario_output}/spice_kernels"
        },
        "scenario_id": config["scenario_id"],
        "main_target": config["main_target"],
        "segmentID": segment_id,
        "shortDesc": config["shortDesc"],
        "startTime": config["startTime"],
        "endTime": config["endTime"],
        "iniAbsolutePath": config["iniAbsolutePath"]
    }

def main(config, mapps=False, zip=False):
    appParams = prepare_app_params(config, mapps, zip)

    print(f"Segment ID: {appParams['segmentID']}")
    print("MAPPS mode enabled" if mapps else "MAPPS mode not enabled")

    scen = scenario(
        appParams["scenario_generator"]["output_folder"],
        appParams,
        True,
        mapps=mapps,
        zip = zip
    )

    scenario_path = scen.buildScenario()
    print()
    print(f"Scenario built at: {scenario_path}")

    spice_tmp_folder = appParams["spice_info"]["spice_tmp_abs_path"]
    if os.path.exists(spice_tmp_folder):
        shutil.rmtree(spice_tmp_folder)

