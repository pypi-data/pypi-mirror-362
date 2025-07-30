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
from datetime import datetime
import re
from importlib import resources

from juice_simphony.CompositionEngine.Scenario.common import utils
from juice_simphony.CompositionEngine.Scenario.environment.trajectory import trajectory

base_package = (__package__ or "").split(".")[0]
config_file_path = resources.files(base_package) / "data"

def find_file_with(directory, filestring):
    for filename in os.listdir(directory):
        if filestring in filename:  # case-insensitive
            return os.path.join(directory, filename)

    return None

def replace_in_file(file_path, target_word, replacement):
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace the target word
    updated_content = content.replace(target_word, replacement)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)


def parse_custom_config(file_path):
    config = {
        "Mission": None,
        "Planning_periods": [],
        "Resolve_to_event": None,
        "Power_algorithm": None,
        "Power_model": {},
        "Resources": [],
        "Output_format": []
    }

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("Mission:"):
                config["Mission"] = line.split(":", 1)[1].strip()

            elif line.startswith("Planning_periods:"):
                parts = line.split(":", 1)[1].strip().split()
                config["Planning_periods"] = parts

            elif line.startswith("Resolve_to_event:"):
                config["Resolve_to_event"] = line.split(":", 1)[1].strip()

            elif line.startswith("Power_algorithm:"):
                config["Power_algorithm"] = line.split(":", 1)[1].strip()

            elif line.startswith("Power_model:"):
                parts = line.split(":", 1)[1].strip().split(maxsplit=1)
                key = parts[0]
                value = parts[1] if len(parts) > 1 else None
                config["Power_model"][key] = value

            elif line.startswith("Resource:"):
                parts = line.split(":", 1)[1].strip().split()
                # Example structure:
                # ['PM_SA_CELL_COUNT', '23560', '"cfg_eps_res_sa_cells_count.asc"']
                resource = {
                    "name": parts[0],
                    "value": parts[1] if len(parts) > 1 else None,
                    "file": parts[2].strip('"') if len(parts) > 2 and parts[2].startswith('"') else None,
                    "type": parts[3] if len(parts) > 3 else None,
                    "rate": float(parts[4]) if len(parts) > 4 and parts[4].replace('.', '', 1).isdigit() else None,            
                    "units": parts[5] if len(parts) > 5 else None,
                    "brfile": parts[6].strip('"') if len(parts) > 6 and parts[6].startswith('"') and parts[6].endswith('.brf"') else None,
                    "id": int(parts[7]) if len(parts) > 7 and parts[7].isdigit() else None,
                    "raw": parts                    # store full token list for debugging/reference
                }
                config["Resources"].append(resource)

            elif line.startswith("Output_format:"):
                parts = line.split(":", 1)[1].strip().split()
                config["Output_format"].append(parts)

    return config


class environment:

    def __init__(self, root_path, parameters=0, mapps=False):
        self.root_path = root_path
        self.parameters = parameters
        self.mainFolderPath = ""
        self.structure = dict()
        self.mapps = mapps

    def build(self):
        self.mainFolderPath = self.createMainFolder('ENVIRONMENT')
        self.structure["path"]       = self.mainFolderPath
        self.structure["ops"]        = self.addOpsSection('OPS')
        self.structure["events"]     = self.addEventsSection('EVENTS')
        #self.structure["segmentation"] = self.addSegmentationSection('SEGMENTATION')
        if self.mapps == True:
            self.structure["trajectory"] = self.addTrajectorySection('TRAJECTORY')
        return self.structure

    def createMainFolder(self, folderName):
        return utils.createFolder(self.root_path, folderName)


    def trim_downlink_events_file(self, file_path, start_time_str, end_time_str, output_path):
        time_format_iso = "%Y-%m-%dT%H:%M:%S"
        start_time = datetime.strptime(start_time_str, time_format_iso)
        end_time = datetime.strptime(end_time_str, time_format_iso)

        output_lines = []
        keep_block = False
        current_block = []

        with open(file_path, 'r') as file:
            for line in file:
                line = line.rstrip()

                # Start of a new block
                if line.startswith("# DL_ segment start"):
                    current_block = [line]
                    keep_block = False  # Reset flag for new block

                elif "MAL_DL_START" in line:
                    match = re.match(r"(\d{2}-[A-Za-z]{3}-\d{4}_\d{2}:\d{2}:\d{2})\s+MAL_DL_START", line)
                    if match:
                        dt_str = match.group(1)
                        dt_obj = datetime.strptime(dt_str, "%d-%b-%Y_%H:%M:%S")
                        if start_time <= dt_obj <= end_time:
                            keep_block = True
                    current_block.append(line)

                elif line.startswith("# DL_ segment end"):
                    current_block.append(line)
                    if keep_block:
                        output_lines.extend(current_block)
                        output_lines.append("")  # Add empty line after each block
                    current_block = []  # Reset for next block

                else:
                    current_block.append(line)

        # Write filtered result to output file
        with open(output_path, 'w') as out_file:
            for line in output_lines:
                out_file.write(line + '\n')

    import re
    from datetime import datetime

    def trim_geopipeline_event_file(self, input_path, start_time_str, end_time_str, output_path):
        time_format_input = "%d-%b-%Y_%H:%M:%S"
        time_format_iso = "%Y-%m-%dT%H:%M:%S"

        # Convert ISO strings to datetime objects
        start_time = datetime.strptime(start_time_str, time_format_iso)
        end_time = datetime.strptime(end_time_str, time_format_iso)

        output_lines = []

        with open(input_path, "r") as infile:
            for line in infile:
                line = line.rstrip()

                if line.startswith("#"):
                    # Always keep comments
                    output_lines.append(line)
                    continue

                # Try to extract the timestamp (must be the first "word" on the line)
                match = re.match(r"(\d{2}-[A-Za-z]{3}-\d{4}_\d{2}:\d{2}:\d{2})", line)
                if match:
                    dt_str = match.group(1)
                    try:
                        dt_obj = datetime.strptime(dt_str, time_format_input)
                        if start_time <= dt_obj <= end_time:
                            output_lines.append(line)
                    except ValueError:
                        # Skip malformed datetime entries
                        continue

        # Write output
        with open(output_path, "w") as outfile:
            for line in output_lines:
                outfile.write(line + "\n")

    def addEventsSection(self, folderName):
        print("Add ENVIRONMENT section")
        structure = dict()
        structure["path"] = utils.createFolder(self.mainFolderPath, folderName)

        geometryPath = utils.createFolder(structure["path"], "GEOMETRY")
        structure["geometryPath"] = geometryPath
        scenario_id = self.parameters['scenarioID']
        crema_version = self.parameters['cremaVersion'].upper()
        crema_id = crema_version.strip().replace('CREMA_', '')
        desc = self.parameters['shortDesc']
        start = self.parameters["startTime"]
        end = self.parameters['endTime']
        juice_conf = self.parameters['conf_repo']['juice_conf']

        # GEOPIPELINE file
        geo_evt_params = {}
        geo_evt_params["version"] = ""
        geo_evt_params["scenarioID"] = scenario_id
        fileName = f"EVT_EPS_FORMAT_GEOPIPELINE_{crema_id}.EVF"
        filePath = os.path.normpath(os.path.join(juice_conf, "internal/geopipeline/output", crema_version, fileName))
        fileNameOutput = os.path.join(geometryPath, f"EVT_{scenario_id}_GEOPIPELINE.evf")
        self.trim_geopipeline_event_file(filePath, start, end, fileNameOutput)
        structure["geopipelineEvents"] = fileNameOutput

        # DOWNLINK file
        fileName = "downlink.evf"
        fileNameOutput = f"EVT_{scenario_id}_DOWNLINK.evf"
        refFile = os.path.normpath(os.path.join(juice_conf, "internal/timeline/output", crema_version, "eps_package/instrument_type", fileName))
        destFile = os.path.join(geometryPath, fileNameOutput)
        self.trim_downlink_events_file(refFile, start, end, destFile)
        structure["downlinkEvents"] = destFile

        # MISSION TIMELINE event file
        fileName = "downlink.evf"
        fileNameOutput = f"MISSION_TIMELINE_EVENT_FILE_{scenario_id}_{desc}.csv"
        refFile = os.path.normpath(os.path.join(juice_conf, "internal/timeline/output", crema_version, "eps_package/instrument_type", fileName))
        destFile = os.path.join(geometryPath, fileNameOutput)
        utils.copyFile(refFile, destFile)
        structure["missionEvf"] = destFile

        return structure


    def addOpsSection(self, folderName):
        structure = dict()
        structure["path"] = utils.createFolder(self.mainFolderPath, folderName)
        dest_folder = structure["path"]
        root_path = self.root_path
        crema_version = self.parameters['cremaVersion'].upper()
        scenario_id = self.parameters['scenarioID']
        juice_conf = self.parameters['conf_repo']['juice_conf']

        # SA cell count
        mypath = os.path.normpath(os.path.join(juice_conf, "internal/geopipeline/output", crema_version))
        filestr = "count"
        pm_sa_cell_count_file = find_file_with(mypath, filestr)

        structure["saCellsCount"] = "#"
        if pm_sa_cell_count_file:
            src_file = os.path.join(mypath, pm_sa_cell_count_file)
            os.makedirs(dest_folder, exist_ok=True)
            dest_file = os.path.join(dest_folder, os.path.basename(src_file))

            if os.path.abspath(src_file) != os.path.abspath(dest_file):
                shutil.copyfile(src_file, dest_file)
                structure["saCellsCount"] = dest_file

        # Cell efficiency
        filestr = "EFFICIENCY"
        mypath = os.path.normpath(os.path.join(juice_conf, "internal/geopipeline/output", crema_version))
        pm_sa_cell_eff_file = find_file_with(mypath, filestr)
        src_file = os.path.join(mypath, pm_sa_cell_eff_file)
        dest_file = os.path.join(dest_folder, os.path.basename(src_file))

        structure["saCellsEff"] = "#"
        if os.path.abspath(src_file) != os.path.abspath(dest_file):
            shutil.copyfile(src_file, dest_file)
            structure["saCellsEff"] = dest_file

        # Bitrate file
        filestr = "BRF_MAL"
        #mypath = os.path.join(config_file_path, "templates", crema_version)
        mypath = os.path.normpath(os.path.join(juice_conf, "internal/geopipeline/output"))
        downlink_brf_file = find_file_with(mypath, filestr)
        src_file = os.path.join(config_file_path,"templates", crema_version, downlink_brf_file)
        dest_file = os.path.join(dest_folder, os.path.basename(src_file))

        structure["brf"] = "#"
        if os.path.abspath(src_file) != os.path.abspath(dest_file):
            shutil.copyfile(src_file, dest_file)
            structure["brf"] = dest_file

        return structure

    def addTrajectorySection(self,folderName):
        structure = dict()
        structure["path"] = utils.createFolder(self.mainFolderPath, folderName)
        confParams = self.parameters
        confParams["scenarioStructure"] = self.structure
        traj = trajectory(structure["path"], confParams)
        return traj.build()
