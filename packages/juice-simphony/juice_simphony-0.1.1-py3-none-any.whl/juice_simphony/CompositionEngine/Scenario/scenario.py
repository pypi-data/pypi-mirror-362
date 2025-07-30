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
import re
import shutil
from pathlib import Path
from datetime import datetime
import pprint
from importlib import resources

from juice_simphony.CompositionEngine.Scenario.common import utils
from juice_simphony.CompositionEngine.Scenario.environment.environment import environment
from juice_simphony.CompositionEngine.Scenario.config.configuration import configuration
from juice_simphony.CompositionEngine.Scenario.modelling.modelling import modelling
from juice_simphony.CompositionEngine.Scenario.definitions.definitions import definitions
from juice_simphony.CompositionEngine.Scenario.timeline.timeline import timeline
from juice_simphony.CompositionEngine.Scenario.timeline.segmentation import segmentation
from juice_simphony.CompositionEngine.Scenario.root.toplevelItl import toplevelItl
from juice_simphony.CompositionEngine.Scenario.root.toplevelEvt import toplevelEvt
from juice_simphony.CompositionEngine.Scenario.graphicalPath import graphicalPath
from juice_simphony.CompositionEngine.Scenario.attitude.attitude import attitude
from juice_simphony.CompositionEngine.Scenario.root.seg_conf import seg_conf
from juice_simphony.CompositionEngine.SegmentationImporter.SegmentationImporter import segmentationTimeline

base_package = (__package__ or "").split(".")[0]
config_file_path = resources.files(base_package) / "data"


class scenario:

    def __init__(self, root_path, parameters, force=False, mapps=False, zip=False):
        self.root_path = root_path + "/SCENARIOS"
        self.params = parameters
        self.mapps = mapps
        self.zip = zip
        self.genRootFolder = False
        self.force = force
        self.mainFolderPath = ""
        self.structure = {}
        self.elements  = {}
        self.segTimeline = segmentationTimeline()
        self.ingestScenario()
        self.params['cremaVersion']   = self.segTimeline.getTrajectory()
        self.params['cremaVersionId'] = self.params['cremaVersion'].upper().strip().replace('CREMA_', '').replace('_', '')
        self.params['scenarioID'] = self.params['scenario_id']
        self.params['genScenarioID']  = self.getGenericScenarioID()
        startTime = self.params['startTime']


    def ingestScenario(self):
        self.segTimeline.ingestPlan(self.params["segmentID"], self.params["startTime"], self.params["endTime"])
        self.params["source"] = {}
        self.params["source"]["segmentation_info"] = self.segTimeline.get_segmentation_info()
        self.params["source"]["trajectory_info"]   = self.segTimeline.get_trajectory_info()
        self.params["source"]["spice_info"]        = self.segTimeline.get_spice_info()
        self.params["spice_if"] = self.segTimeline.spice

    def getGenericScenarioID(self):
        scenario = self.params['scenario_id'].split('_')[0]

        # Validate format: one letter followed by 3 digits
        if re.fullmatch(r'[A-Z]\d{3}', scenario, re.IGNORECASE):
            # Normalize to uppercase and return
            return scenario.upper()
        else:
            raise ValueError(
                f"Invalid scenario format: '{scenario}'. Expected format: 1 letter + 3 digits (e.g., 'E001').")

    def copy_and_process_templates(self, src_dir, dest_dir, replacement):
        src_dir = os.path.normpath(src_dir)
        dest_dir = os.path.normpath(dest_dir)

        os.makedirs(dest_dir, exist_ok=True)

        for filename in os.listdir(src_dir):
            src_file = os.path.join(src_dir, filename)

            if os.path.isfile(src_file):
                # Replace 'template' in filename
                new_filename = filename.replace("template", replacement)
                dest_file = os.path.join(dest_dir, new_filename)
                shutil.copy2(src_file, dest_file)

                # If it's a scenario file, replace 'template' in its content
                if "ODF_SCENARIO" in new_filename:
                    with open(dest_file, 'r', encoding='utf-8') as file:
                        content = file.read()

                    content = content.replace("template", replacement)
                    with open(dest_file, "w", encoding="utf-8") as f:
                        f.write(content)

    def buildScenario(self):

        if self.genRootFolder:
            self.mainFolderRootPath = self.createRootFolder(self.root_path,self.params["genScenarioID"])
            self.mainFolderPath = self.createMainFolder(self.mainFolderRootPath,self.params["scenarioID"])

        else:
            self.mainFolderPath = self.createMainFolder(self.root_path,self.params["scenarioID"])
            self.mainFolderRootPath = self.mainFolderPath

        self.structure["root_path"]        = self.root_path
        self.structure["main_folder_name"] = self.params["scenarioID"]
        self.structure["path"]             = self.mainFolderPath;
        self.structure["environment"]      = self.addEnvironmentSection()
        self.structure["modelling"]        = self.addModellingSection()
        self.structure["definitions"]      = self.addDefinitionsSection()
        self.structure["attitude"]         = self.addAttitudeSection()
        self.structure["segmentation"]     = self.addSegmentationSection()
        timelineOutput                     = self.addTimelineSection()
        self.structure["timeline"]         = timelineOutput["structure"]
        self.elements                      = timelineOutput["elements"]
        self.structure.update(self.addRootContent())
        self.structure["configuration"] = self.addConfigurationSection()
        self.structure.update(self.generateSegImporterCfgFile())

        folderName = self.params['scenario_id'] + '_' + \
                     self.params["shortDesc"].upper().replace(' ', '_') + '_' + \
                     self.params["startDate"] + '_' + \
                     self.params["endDate"]

        # copy OBSERVATIONS/JUI/SCENARIO
        obs_jui_scenario = os.path.normpath(os.path.join(self.structure["definitions"]["path"], "JUI/SCENARIO"))
        tmp_obs_jui_scenario = os.path.normpath(os.path.join(config_file_path, "templates/OBSERVATIONS/JUI/SCENARIO"))
        self.copy_and_process_templates(tmp_obs_jui_scenario, obs_jui_scenario, replacement=self.params['scenario_id'])

        # Create output zip file
        self.zipFileName = folderName

        self.generateScenarioStructure()
        parentRootPath = Path(self.root_path)
        output_filename = os.path.normpath(os.path.join(parentRootPath.parent.absolute(), "SCENARIOS", self.zipFileName))

        if self.zip == True:
            zip_folder = os.path.join(self.root_path, folderName)
            shutil.make_archive(output_filename, 'zip', zip_folder)
            output_filename = output_filename + ".zip"
            shutil.rmtree(zip_folder)

        return output_filename

    def createTopFolder(self):
        TopFolderName = self.scenarioID
        return utils.createFolder(self.root_path, TopFolderName)

    def createMainFolder(self, refPath, scenarioID):
        # Build folder name (S0003_01_21C13_CALLISTO_FB_320110_320112)
        self.params["startDate"] = datetime.fromisoformat(self.params["startTime"]).strftime("%y%m%d")
        self.params["endDate"]   = datetime.fromisoformat(self.params["endTime"]).strftime("%y%m%d")
        folderName = scenarioID + '_' + \
                     self.params["shortDesc"].upper().replace(' ', '_') + '_' + \
                     self.params["startDate"] + '_' + \
                     self.params["endDate"]
        if self.force:
            utils.removeFolderTree(os.path.join(self.root_path, folderName))

        main_folder_path = utils.createFolder(refPath, folderName)
        utils.createFolder(main_folder_path, "OUTPUT")

        return main_folder_path

    def createRootFolder(self, refPath, scenarioID):
        # Build folder name (S0003_01_21C13_CALLISTO_FB)
        self.params["startDate"] = datetime.fromisoformat(self.params["startTime"]).strftime("%y%m%d")
        self.params["endDate"]   = datetime.fromisoformat(self.params["endTime"]).strftime("%y%m%d")
        folderName = scenarioID + '_' + \
                     self.params["shortDesc"].upper().replace(' ', '_')
        if self.force:
            utils.removeFolderTree(os.path.join(self.root_path, folderName))
        return utils.createFolder(refPath, folderName)

    def addConfigurationSection(self, mapps=False):
        confParams = self.params
        confParams["scenarioStructure"] = self.structure;
        confParams["elements"]          = self.elements;
        conf = configuration(self.mainFolderPath, confParams, mapps=self.mapps)
        return conf.build()

    def addEnvironmentSection(self, mapps=False):
        envParams = self.params
        env = environment(self.mainFolderPath,envParams, mapps=self.mapps)
        return env.build()

    def addDefinitionsSection(self):
        defsParams = self.params
        defs = definitions(self.segTimeline, self.mainFolderPath, defsParams)
        return defs.build()

    def addModellingSection(self):
        modelParams = self.params
        mod = modelling(self.mainFolderPath, modelParams)
        return mod.build()

    def addAttitudeSection(self):
        attParams = self.params
        att = attitude(self.segTimeline, self.mainFolderPath, attParams)
        return att.build()

    def addTimelineSection(self):
        tmlParams = self.params
        tml = timeline(self.segTimeline, self.mainFolderPath, tmlParams)
        return tml.build()

    def addSegmentationSection(self):
        segParams = self.params
        seg = segmentation(self.segTimeline, self.mainFolderPath, segParams)
        return seg.build()

    def addRootContent(self):
        structure = dict()

        # Timeline top level
        # ------------------
        tlTmlParams = self.params
        tlTmlParams["timeline"] = {}
        tlTmlParams["timeline"]["version"]   = "V1"
        tlTmlParams["timeline"]["startTime"] = self.params["startTime"] + "Z"
        tlTmlParams["timeline"]["endTime"]   = self.params["endTime"] + "Z"
        includeList = []
        
        include_file = {}
        include_file["fileDescription"] = "Include Observation General ITL"
        include_file["filePath"] = self.structure["timeline"]["top_level_inst"]
        includeList.append(include_file)

        if "plat_timeline" in self.structure["timeline"]:
            include_file = {}
            include_file["fileDescription"] = "Include Platform Power ITL"
            include_file["filePath"] = self.structure["timeline"]["plat_timeline"] 
            includeList.append(include_file)

        include_file = {}
        include_file["fileDescription"] = "Include Communications ITL"
        include_file["filePath"] = self.structure["timeline"]["comms_timeline"]
        includeList.append(include_file)

        tlTml = toplevelItl(self.mainFolderPath, includeList, tlTmlParams)
        structure["toplevelItl"] = tlTml.genFile()

        tlTmlParams["prefix"] = "EVT"
        includeList = []

        include_file_1 = {"filePath": self.structure["environment"]["events"]["geopipelineEvents"]}
        includeList.append(include_file_1)
        include_file_2 = {"filePath": self.structure["environment"]["events"]["downlinkEvents"]}
        includeList.append(include_file_2)

        tlEvf = toplevelEvt(self.mainFolderPath, includeList, tlTmlParams)
        structure["toplevelEvf"] = tlEvf.genFile()

        return structure

    def generateScenarioStructure(self):
        structFilePath = os.path.normpath(os.path.join(self.mainFolderPath, "aareadme.rst"))
        with open(structFilePath, "w", encoding="utf-8") as structFile:
            # Header text
            structFile.write("JUICE SCENARIO DIRECTORY STRUCTURE\n")
            structFile.write("=================================\n\n")
            structFile.write("This file documents the structure of the scenario directory.\n\n")

            # Generate full tree
            paths = graphicalPath.make_tree(Path(self.mainFolderRootPath))

            for path in paths:
                structFile.write(path.displayable() + "\n")

    def generateSegImporterCfgFile(self):
        structure = {}
        seg_conf_file = seg_conf(self.mainFolderPath, self.params)
        structure["segCfgFile"] = seg_conf_file.gen(self.structure)
        return structure
