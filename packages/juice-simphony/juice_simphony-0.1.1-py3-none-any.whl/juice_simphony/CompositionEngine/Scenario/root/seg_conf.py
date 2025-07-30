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
from jinja2 import Template
import os
import json

from juice_simphony.CompositionEngine.Scenario.common.fileTemplate import fileTemplate
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName

def replace_in_file(file_path, target_word, replacement):
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace the target word
    updated_content = content.replace(target_word, replacement)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)


def update_eps_file(input_file_path, resfile, new_file_path):
    updated_lines = []

    with open(input_file_path, 'r') as f:
        if resfile == 'brf':
            for line in f:
                if line.startswith("Resource: DOWNLINK_RATE"):
                    parts = line.split('"')
                    if len(parts) >= 3:
                        parts[1] = new_file_path  # Replace file path
                        line = '"'.join(parts)
                updated_lines.append(line)

        if resfile == 'eff':
            for line in f:
                if line.startswith("Resource: PM_SA_CELL_EFFICIENCY"):
                    parts = line.split('"')
                    if len(parts) >= 3:
                        parts[1] = new_file_path  # Replace file path
                        line = '"'.join(parts)
                updated_lines.append(line)

        if resfile == 'count' and new_file_path != '#':
            for line in f:
                if line.startswith("Resource: PM_SA_CELL_COUNT"):
                    parts = line.split('"')
                    if len(parts) >= 3:
                        parts[1] = new_file_path  # Replace file path
                        line = '"'.join(parts)
                updated_lines.append(line)


    with open(input_file_path, 'w') as f:
        f.writelines(updated_lines)

def find_key(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                result = find_key(value, target_key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, target_key)
            if result is not None:
                return result
    return None

class seg_conf(fileName):
    def __init__(self, path, params=0):
        self.path = path
        self.params = params
        self.params["prefix"]  = "CFG"
        self.params["type"]    = "OSVE"
        self.params["desc"]    = ""
        self.params["version"] = 0
        self.params["ext"]     = "json"
        self.fileName = ""
        self.template = 0
        fileName.__init__(self, params)

    def buildRelPath(self, path, refPath):
        return os.path.relpath(path, refPath).replace("\\","/")

    def gen(self, structure_inputs):

        #------------------------------------------------
        # Update EPS configuration file with crema values
        #------------------------------------------------

        # Reference EPS configuration
        epsfile = structure_inputs["configuration"]["epsCfg"]["epsCfgFile"]
        base_path = os.path.join(structure_inputs["path"], "CONFIG/EPS")

        # Replace BRF
        resfile = 'brf'
        destFile = structure_inputs["environment"]["ops"]["brf"]
        brf_file = os.path.relpath(destFile, start=base_path)
        update_eps_file(epsfile, resfile, brf_file)

        # Replace cell efficiency
        resfile = 'eff'
        destFile = structure_inputs["environment"]["ops"]["saCellsEff"]
        eff_file = os.path.relpath(destFile, start=base_path)
        update_eps_file(epsfile, resfile, eff_file)

        # Replace cell count
        resfile = 'count'
        destFile = structure_inputs["environment"]["ops"]["saCellsCount"]
        if destFile != '#':
            count_file = os.path.relpath(destFile, start=base_path)
            update_eps_file(epsfile, resfile, count_file)


        #------------------------------------------------
        # Create OSVE configuration file
        #------------------------------------------------
        self.fileName = self.params["prefix"] + "_" + self.params["type"] + "_" + self.params["scenarioID"]+ "." + self.params["ext"]
        destFilePath = os.path.join(self.path, "CONFIG/OSVE", self.fileName)
        
        seg_importer_cfg = {}
        base_path = self.path
        
        # session_cfg
        seg_importer_cfg.update(sessionConfiguration={})
        session_cfg = seg_importer_cfg["sessionConfiguration"]
        session_cfg["sessionID"] = structure_inputs["main_folder_name"]
        session_cfg["version"]   = "1.0.0"

        # simulation_cfg
        session_cfg.update(simulationConfiguration={})
        simulation_cfg = session_cfg["simulationConfiguration"]
        simulation_cfg["timeStep"]       = 5
        simulation_cfg["outputTimeStep"] = 5
        simulation_cfg["resizePtrBlocks"] = False
        simulation_cfg["simulateTimeline"] = True
        
        #att_sim_cfg
        session_cfg.update(attitudeSimulationConfiguration={})
        att_sim_cfg = session_cfg["attitudeSimulationConfiguration"]

        metakernel = self.params["source"]["spice_info"]["kernels"]["metakernel"]
        skd_version = self.params["source"]["spice_info"]["kernels"]["skd_version"]

        # Strip the version suffix if it's at the end of the string
        if metakernel.endswith(f"_{skd_version}"):
            base_name = metakernel[: -len(skd_version) - 1]  # remove "_" + skd_version
        else:
            base_name = metakernel  # fallback if version not found

        metakernel_local = f"{base_name}_local.tm"

        att_sim_cfg["kernelsList"] = {
            #"baselineRelPath": os.path.join(self.params["spice_info"]["spice_kernels_abs_path"], "mk"),
            "baselineRelPath": "{KERNELS_JUICE}",
            "fileList": [
                {
                    "fileRelPath": metakernel_local  # Ensure this variable is defined earlier
                }
            ]
        }

        att_baselineRelPath = self.buildRelPath(structure_inputs["configuration"]["agmCfg"]["path"], structure_inputs["path"])
        att_sim_cfg["baselineRelPath"]     = os.path.join("{JUICE_SCENARIO_DIR}", att_baselineRelPath)
        att_sim_cfg["ageConfigFileName"] = os.path.basename(structure_inputs["configuration"]["agmCfg"]["agmXMLConfig"])
        att_sim_cfg["fixedDefinitionsFile"] = os.path.basename(structure_inputs["configuration"]["agmCfg"]["fixedDefinition"])
        att_sim_cfg["predefinedBlockFile"]  = os.path.basename(structure_inputs["configuration"]["agmCfg"]["agmPreBlocks"])
        att_sim_cfg["eventDefinitionsFile"]  = os.path.basename(structure_inputs["configuration"]["agmCfg"]["eventDefinition"])

        #att_sim_cfg["predefinedBlockFile"] = self.buildRelPath(structure_inputs["configuration"]["agmCfg"]["fixedDefinition"], structure_inputs["configuration"]["agmCfg"]["path"])

        #inst_sim_cfg
        session_cfg.update(instrumentSimulationConfiguration={})
        inst_sim_cfg = session_cfg["instrumentSimulationConfiguration"]
        inst_baselineRelPath = self.buildRelPath(structure_inputs["configuration"]["epsCfg"]["path"], structure_inputs["path"])
        inst_sim_cfg["baselineRelPath"]        = os.path.join("{JUICE_SCENARIO_DIR}", inst_baselineRelPath)
        ######inst_sim_cfg["baselineRelPath"]        = self.buildRelPath(structure_inputs["configuration"]["epsCfg"]["path"], structure_inputs["root_path"])
        inst_sim_cfg["unitFileName"]           = "units.def"
        inst_sim_cfg["configFileName"]         = self.buildRelPath(structure_inputs["configuration"]["epsCfg"]["epsCfgFile"], structure_inputs["configuration"]["epsCfg"]["path"])
        #inst_sim_cfg["edfFileName"]            = self.buildRelPath(structure_inputs["modelling"]["toplevelEdf"], structure_inputs["configuration"]["epsCfg"]["path"])
        inst_sim_cfg["eventDefFileName"]       = self.buildRelPath(structure_inputs["configuration"]["epsCfg"]["evtDefFile"], structure_inputs["configuration"]["epsCfg"]["path"])
        #inst_sim_cfg["observationDefFileName"] = self.buildRelPath(structure_inputs["observations"]["topLevelObsDefFile"], structure_inputs["configuration"]["epsCfg"]["path"])
        #inst_sim_cfg["observationDefFileName"] = None


        # -------------------------------
        # Add inputFiles section
        # -------------------------------
        session_cfg.update(inputFiles={})
        input_files_cfg = session_cfg["inputFiles"]
        input_files_cfg["baselineRelPath"] = "{JUICE_SCENARIO_DIR}"
        input_files_cfg["xmlPtrPath"] = os.path.relpath(structure_inputs["attitude"]["xmlAttitudeFile"], base_path)
        input_files_cfg["segmentTimelineFilePath"] = os.path.basename(structure_inputs["toplevelItl"])
        top_level_path = find_key(self.params, 'obsDefTopLevel')
        input_files_cfg["modellingConfiguration"] = {
            "baselineRelPath": "MODELLING",
            "edfFileName": "EDF_JUICE.edf",
            "observationDefFileName": os.path.relpath(top_level_path, os.path.join(base_path, "MODELLING")),
        }
        input_files_cfg["eventTimelineFilePath"] = os.path.basename(structure_inputs["toplevelEvf"])


        # -------------------------------
        # Add outputFiles section
        # -------------------------------
        session_cfg["outputFiles"] = {
            "baselineRelPath": "{JUICE_SCENARIO_DIR}/OUTPUT",
            "simOutputFilesPath": "eps_output",
            "ckAttitudeFilePath": "PTR_SOC_RESOLVED.bc",
            "ckConfig": {
                "ckFrameId": -28001,
                "ckTimeStep": 5
            },
            "mgaDataFilePath": "PTR_SOC_MGA.csv",
            "attitudeXmlPtr": "PTR_SOC_RESOLVED.ptx",
            "dataPacks": [
                {
                    "filePath": "osve_datapack.csv",
                    "timeStep": 5,
                    "precision": 10,
                    "type": "CSV",
                    "fields": [
                        {
                            "type": "time",
                            "label": "TIME",
                            "format": "utc"
                        },
                        {
                            "type": "MAPPS",
                            "overlayId": "AGM_SA_ROT_ANG",
                            "label": "AGM_SA_ROT_ANG"
                        }
                    ]
                }
            ]
        }

        # -------------------------------
        # Add logging section
        # -------------------------------
        session_cfg["logging"] = {
            "stdOutLogLevel": "INFO",
            "jsonLogFile": "log.json"
        }

        with open(destFilePath, 'w') as outfile:
            json.dump(seg_importer_cfg, outfile, indent=2)

        return destFilePath