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
from pathlib import Path
import textwrap
from importlib import resources
import shutil

base_package = (__package__ or "").split(".")[0]
config_file_path = resources.files(base_package) / "data"


from juice_simphony.CompositionEngine.Scenario.common import utils
from juice_simphony.CompositionEngine.Scenario.config.epsFile import epsFile
from juice_simphony.CompositionEngine.Scenario.config.agmCfgFiles import agmCfgFile
from juice_simphony.CompositionEngine.Scenario.config.agmIniFile import agmIniFile
from juice_simphony.CompositionEngine.Scenario.config.mappsIniFile import mappsIniFile
from juice_simphony.CompositionEngine.Scenario.config.epsEvtDefFile import epsEvtDefFile


class configuration:

    def __init__(self, root_path, parameters=0, mapps=False):
        self.root_path = root_path
        self.parameters = parameters
        self.mapps = mapps
        self.mainFolderPath = ""
        self.iniAbsPath = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.root_path))), self.parameters["iniAbsolutePath"]))
        self.structure = {}

    def build(self):
        print("Add CONFIG section")
        self.structure["path"]     = self.createMainFolder('CONFIG')
        self.structure["agmCfg"]   = self.addAgmSection('AGM')
        self.structure["epsCfg"]   = self.addEpsSection('EPS')
        self.structure["osveCfg"] = self.addOsveSection('OSVE')
        if self.mapps == True:
            self.structure["mappsCfg"] = self.addMappsSection('MAPPS')
        return self.structure

    def createMainFolder(self, folderName):
        self.mainFolderPath = utils.createFolder(self.root_path, folderName)
        return self.mainFolderPath


    def addAgmSection(self, folderName):
        structure = {}
        folderPath = utils.createFolder(self.mainFolderPath, folderName)
        structure["path"] = folderPath
        juice_conf = self.parameters['conf_repo']['juice_conf']

        # Setup AGM config common parameters
        # {prefix}_{scenarioID}_{type}_{desc}_{version}
        agm_cfg_params = {}
        agm_cfg_params["prefix"]     = "CFG"
        agm_cfg_params["type"]       = "AGM"
        agm_cfg_params["scenarioID"] = self.parameters["scenarioID"]

        # OSVE XML Config
        # -----------------
        # {prefix}_{scenarioID}_{type}_{desc}_{version}
        agm_xml_config = agmCfgFile(folderPath, agm_cfg_params)
        fileName = "cfg_agm_jui.xml"    # --> CFG_AGM_S008_01.xml
        filePath = os.path.normpath(os.path.join(juice_conf,"internal/phs/agm", fileName))
        structure["agmXMLConfig"] = agm_xml_config.genFile(filePath)

        # Fixed definitions
        # -----------------
        agm_cfg_params["desc"] = "FIXED_DEFS_MLB"
        agm_fixed_defs = agmCfgFile(folderPath, agm_cfg_params)
        fileName = "cfg_agm_jui_fixed_definitions.xml"  # --> CFG_AGM_FIXED_DEFS_MLB_S008_01.xml
        filePath = os.path.normpath(os.path.join(juice_conf,"internal/phs/agm", fileName))
        structure["fixedDefinition"] = agm_fixed_defs.genFile(filePath)

        # Event definitions
        # -----------------
        agm_cfg_params["desc"] = "EVENT_DEFINITIONS"
        agm_event_defs = agmCfgFile(folderPath, agm_cfg_params)
        fileName = "cfg_agm_jui_event_definitions.xml"  # --> CFG_AGM_EVENT_DEFINITIONS_S008_01.xml
        filePath = os.path.normpath(os.path.join(juice_conf,"internal/phs/agm", fileName))
        structure["eventDefinition"] = agm_event_defs.genFile(filePath)

        # Predefined blocks
        # -----------------
        # {prefix}_{scenarioID}_{type}_{desc}_{version}
        agm_cfg_params["desc"] = "PREDEF_BLOCKS_MLB"
        agm_pre_blocks = agmCfgFile(folderPath, agm_cfg_params)
        fileName = "cfg_agm_jui_predefined_block.xml"  # --> CFG_AGM_PREDEF_BLOCKS_MLB_S008_01.xml
        filePath = os.path.normpath(os.path.join(juice_conf,"internal/phs/agm", fileName))
        structure["agmPreBlocks"] = agm_pre_blocks.genFile(filePath)

        # Default block
        # -------------
        agm_cfg_params["desc"] = "DEF_BLOCK_" + self.parameters["main_target"].upper()
        agm_cfg_params["body"] = self.parameters["main_target"].capitalize()
        agm_def_block = agmCfgFile(folderPath, agm_cfg_params)
        fileName = "cfg_agm_jui_default_pointing_def.xml"    # --> CFG_AGM_DEF_BLOCK_JUPITER_S008_01.xml
        filePath = os.path.normpath(os.path.join(juice_conf,"internal/phs/agm", fileName))
        output = os.path.join(folderPath, "CFG_AGM_DEF_BLOCK_" + self.parameters["main_target"].upper() + "_" + self.parameters["scenarioID"] + ".xml")
        shutil.copyfile(filePath, output)

        with open(output, 'r', encoding='utf-8') as file:
            content = file.read()

        replacement = self.parameters["main_target"].upper()
        content = content.replace("{{agm.defaultPointing.centralBody}}", replacement)
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)

        structure["defaultPointingDef"] = output
        #structure["defaultPointingDef"] = agm_def_block.genFile(filePath)

        # AGM MAPPS ini
        # -------------
        if self.mapps == True:
            agmCfgParams = dict()
            agmCfgParams["scenarioID"] = self.parameters["scenarioID"]
            agmCfgParams["AGMConfig"] = {}

            agmCfgParams["AGMConfig"]["Integration"] = {}
            agmCfgAbsPath = os.path.normpath(os.path.join(self.iniAbsPath, "CONFIG"))
            agmCfgParams["AGMConfig"]["Integration"]["fixedDefsFileName"] = self.buildRelPath(structure["fixedDefinition"],agmCfgAbsPath)
            agmCfgParams["AGMConfig"]["Integration"]["userDefsFileName"] = ""
            agmCfgParams["AGMConfig"]["Integration"]["predefBlocksFileName"] = self.buildRelPath(structure["agmPreBlocks"],agmCfgAbsPath)
            agmCfgParams["AGMConfig"]["Integration"]["eventDefsFileName"] = ""

            agmCfgParams["AGMConfig"]["Parameters"] = {}
            agmCfgParams["AGMConfig"]["Parameters"]["AC_rw_wmm_ggt_tgt_obj"] = self.parameters["main_target"]

            agmCfg = agmIniFile(folderPath, agmCfgParams)
            fileName = "CFG_TPL0001A_AGM_" + self.parameters["main_target"] + ".ini"
            filePath = os.path.normpath(os.path.join(config_file_path, "templates/MAPPS_CONF/AGM", fileName))
            structure["agmCfgFile"] = agmCfg.genFile(filePath)

        return structure

    def addEpsSection(self, folderName):
        structure = dict()
        folderPath = utils.createFolder(self.mainFolderPath, folderName)
        structure["path"] = folderPath
        juice_conf = self.parameters['conf_repo']['juice_conf']

        # Generate EPS config file
        epsCfgParams = dict()
        epsCfgParams["scenarioID"]   = self.parameters["scenarioID"]
        epsGfgRefFolder = folderPath

        if self.parameters["scenarioStructure"]["environment"]["ops"]["brf"]:
            epsCfgParams["bitrateFile"]  = self.buildRelPath(self.parameters["scenarioStructure"]["environment"]["ops"]["brf"], epsGfgRefFolder)

        if self.parameters["scenarioStructure"]["environment"]["ops"]["saCellsCount"] != "#":
            epsCfgParams["saCellsCount"] = self.buildRelPath(self.parameters["scenarioStructure"]["environment"]["ops"]["saCellsCount"], epsGfgRefFolder)

        if self.parameters["scenarioStructure"]["environment"]["ops"]["saCellsEff"]:
            epsCfgParams["saCellsEff"]   = self.buildRelPath(self.parameters["scenarioStructure"]["environment"]["ops"]["saCellsEff"], epsGfgRefFolder)

        epsCfg = epsFile(folderPath, epsCfgParams)
        filePath = os.path.normpath(os.path.join(juice_conf,"internal/phs/eps", "cfg_eps.cfg"))
        structure["epsCfgFile"] = epsCfg.genFile(filePath)

        # Generate EPS JSOC event definition file
        epsEvtParams = dict()
        epsEvtParams["desc"] = "JSOC"
        epsEvtParams["scenarioID"] = self.parameters["scenarioID"]

        epsEvtDef = epsEvtDefFile(folderPath, epsEvtParams)
        #filePath = os.path.normpath(os.path.join(self.parameters["scenario_generator"]["ref_scenario_abs_path"]  , R"CONFIG/EPS/EVD_TPL0001A_EPS.def"))
        fileName = "cfg_eps_jsoc_evd.def"
        filePath = os.path.normpath(os.path.join(juice_conf,"internal/phs/eps", fileName))
        structure["evtDefFile"] = epsEvtDef.genFile(filePath)

        # Generate EPS JMOC event definition file
        epsEvtParams["desc"] = "JMOC"
        #print(epsEvtParams)
        #{'desc': 'JMOC', 'scenarioID': 'S008_01', 'prefix': 'EVD', 'type': 'EPS', 'version': '', 'ext': 'def', 'addScenarioID': True}
        epsEvtDef = epsEvtDefFile(folderPath, epsEvtParams)
        fileName = "cfg_eps_jmoc_evf.def"
        filePath = os.path.normpath(os.path.join(juice_conf,"internal/phs/eps", fileName))
        structure["evtDefFile"] = epsEvtDef.genFile(filePath)

        # Copy units, and planning period files
        refFilePath  = os.path.normpath(os.path.join(juice_conf,"internal/phs/eps", "cfg_eps_units.def"))        
        destFilePath = os.path.normpath(os.path.join(folderPath, R"units.def"))
        utils.copyFile (refFilePath, destFilePath)

        # Copy json schema file
        refFilePath  = os.path.normpath(os.path.join(juice_conf,"internal/phs/osve/schemas", "jsoc-itl-schema.json"))
        destFilePath = os.path.normpath(os.path.join(folderPath, R"jsoc-itl-schema.json"))
        utils.copyFile (refFilePath, destFilePath)

        if self.mapps == True:
            refFilePath = os.path.normpath(os.path.join(config_file_path, "templates/MAPPS_CONF/EPS", "planning_mtp_mapping.def"))
            destFilePath = os.path.normpath(os.path.join(folderPath, R"planning_mtp_mapping.def"))
            utils.copyFile (refFilePath, destFilePath)

            refFilePath = os.path.normpath(os.path.join(config_file_path, "templates/MAPPS_CONF/EPS", "planning_period_def.xml"))
            destFilePath = os.path.normpath(os.path.join(folderPath, R"planning_period_def.xml"))
            utils.copyFile (refFilePath, destFilePath)

        # Generate EPS Event Definition Aggregator File
        scenario = self.parameters["scenarioID"]
        file_name = f"EVD_EPS_{scenario}.def"
        file_path = os.path.join(folderPath, file_name)

        content = textwrap.dedent(f"""\
            #
            # EPS Events Definition File for {scenario}
            #
            #
            Include_file: EVD_EPS_JMOC_{scenario}.def
            Include_file: EVD_EPS_JSOC_{scenario}.def
            """)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        structure["evtDefFile"] = file_path

        return structure

    def addOsveSection(self, folderName):
        structure = dict()
        folderPath = utils.createFolder(self.mainFolderPath, folderName)
        structure["path"] = folderPath

        # Setup OSVE config common parameters
        # {prefix}_{scenarioID}_{type}_{desc}_{version}
        osve_cfg_params = {}
        osve_cfg_params["prefix"]     = "CFG"
        osve_cfg_params["type"]       = "OSVE"
        osve_cfg_params["scenarioID"] = self.parameters["scenarioID"]

        return structure

    def addMappsSection(self, folderName):
        structure = dict()
        folderPath = utils.createFolder(self.mainFolderPath, folderName)
        structure["path"] = folderPath

        # Generate MAPPS ini file
        mappsCfgParams = dict()
        mappsCfgParams["scenarioID"] = self.parameters["scenarioID"]
        mappsCfgParams = self.setMappsSectionParameters(mappsCfgParams)
        mappsfg = mappsIniFile(folderPath, mappsCfgParams)
        fileName = "CFG_TPL0001A_" + self.parameters["main_target"] + "_MAPPS.ini"
        #filePath = os.path.normpath(os.path.join(self.parameters["scenario_generator"]["ref_scenario_abs_path"]  , R"CONFIG/MAPPS",fileName))
        filePath = os.path.normpath(os.path.join(config_file_path, "templates/MAPPS_CONF/MAPPS", fileName))
        structure["mappsCfgFile"] = mappsfg.genFile(filePath)

        return structure


    def setMappsSectionParameters(self, mappsCfgParams):
        #print("------------------------------------------------------------")
        #print("------------------------STRUCTURE --------------------------")
        #print("------------------------------------------------------------")
        #print(json.dumps(self.parameters["scenarioStructure"], indent = 4))

        # [DataPaths]
        mappsCfgParams["DataPaths"]={}
        mappsCfgParams["DataPaths"]["absMAPPSRootDir"]="TMP"
        mappsCfgParams["DataPaths"]["relAGMInitConfigPath"] = self.buildRelPath(self.structure["agmCfg"]["path"], self.iniAbsPath)
        mappsCfgParams["DataPaths"]["relCmdDataDir"]=""
        mappsCfgParams["DataPaths"]["relConfigDataDir"]="CONFIG"
        mappsCfgParams["DataPaths"]["relDataCacheDir"]="CACHE"
        mappsCfgParams["DataPaths"]["relEDFDataDir"] = self.buildRelPath(self.parameters["scenarioStructure"]["modelling"]["path"], self.iniAbsPath)
        configPath = os.path.normpath(os.path.join(self.iniAbsPath, mappsCfgParams["DataPaths"]["relConfigDataDir"]))
        mappsCfgParams["DataPaths"]["absCfgPath"] = configPath
        mappsCfgParams["DataPaths"]["relEPSConfigPath"] = self.buildRelPath(self.structure["epsCfg"]["path"], configPath)
        mappsCfgParams["DataPaths"]["relEPSDataDir"] = self.buildRelPath(self.structure["epsCfg"]["path"], configPath)
        mappsCfgParams["DataPaths"]["relEVFOutputDir"]=""
        mappsCfgParams["DataPaths"]["relFECSDataDir"]=""
        mappsCfgParams["DataPaths"]["relGPTRDataDir"]=""
        mappsCfgParams["DataPaths"]["relGraphicsDir"]=""
        mappsCfgParams["DataPaths"]["relImageMapsDir"]="CONFIG/MAPS"
        mappsCfgParams["DataPaths"]["relMPCLDataDir"]=""
        mappsCfgParams["DataPaths"]["relManualsDir"]="CONFIG/MANUALS"
        mappsCfgParams["DataPaths"]["relObsDataDir"] = self.buildRelPath(self.parameters["scenarioStructure"]["definitions"]["path"], self.iniAbsPath)
        mappsCfgParams["DataPaths"]["relOutputDataDir"]=""
        mappsCfgParams["DataPaths"]["relPTROutputDir"]=""
        mappsCfgParams["DataPaths"]["relPTSLDir"]=""
        mappsCfgParams["DataPaths"]["relSFLUDataDir"]=""
        mappsCfgParams["DataPaths"]["relScenariosDir"] = self.buildRelPath(self.parameters["scenarioStructure"]["path"],self.iniAbsPath)
        mappsCfgParams["DataPaths"]["relSimDataDir"]   = self.buildRelPath(self.parameters["scenarioStructure"]["environment"]["trajectory"]["path"],self.iniAbsPath)

        # [ControlPanel]
        mappsCfgParams["ControlPanel"]={}

        # [ControlPanel]\InputData
        mappsCfgParams["ControlPanel"]["InputData"]={}

        # [ControlPanel]\InputData\ExperimentTimeline
        mappsCfgParams["ControlPanel"]["InputData"]["ExperimentTimeline"]={}
        mappsCfgParams["ControlPanel"]["InputData"]["ExperimentTimeline"]["obsSequencesDir"]=self.buildRelPath(self.parameters["scenarioStructure"]["path"],self.iniAbsPath)
        mappsCfgParams["ControlPanel"]["InputData"]["ExperimentTimeline"]["obsSequencesFile"]=os.path.basename(self.parameters["scenarioStructure"]["toplevelItl"])
        mappsCfgParams["ControlPanel"]["InputData"]["ExperimentTimeline"]["timelineSource"]="OBSSchedule"
        mappsCfgParams["ControlPanel"]["InputData"]["ExperimentTimeline"]["useObservationProfiles"]="true"
        mappsCfgParams["ControlPanel"]["InputData"]["ExperimentTimeline"]["expandActivities"]="true"
        mappsCfgParams["ControlPanel"]["InputData"]["ExperimentTimeline"]["expandObservations"]="true"

        # [ControlPanel]\InputData\OrbitData
        simAbsPath = os.path.normpath(os.path.join(self.iniAbsPath, mappsCfgParams["DataPaths"]["relSimDataDir"]))
        mappsCfgParams["ControlPanel"]["InputData"]["OrbitData"]={}
        mappsCfgParams["ControlPanel"]["InputData"]["OrbitData"]["gsVisPeriodsFile"]=self.buildRelPath(self.parameters["scenarioStructure"]["environment"]["trajectory"]["groundStationFile"], simAbsPath)
        mappsCfgParams["ControlPanel"]["InputData"]["OrbitData"]["operationPeriodsFile"]=""
        mappsCfgParams["ControlPanel"]["InputData"]["OrbitData"]["orbitDataFile"]=self.buildRelPath(self.parameters["scenarioStructure"]["environment"]["trajectory"]["trajectoryFile"], simAbsPath)
        mappsCfgParams["ControlPanel"]["InputData"]["OrbitData"]["orbitDefFile"]=self.buildRelPath(self.parameters["scenarioStructure"]["environment"]["trajectory"]["periodDefinitionFile"], simAbsPath)
        mappsCfgParams["ControlPanel"]["InputData"]["OrbitData"]["orbitSource"]="OrbitFiles"
        
        # [ControlPanel]\InputData\TimelineEvents
        mappsCfgParams["ControlPanel"]["InputData"]["TimelineEvents"]={}
        mappsCfgParams["ControlPanel"]["InputData"]["TimelineEvents"]["eventInputDir"]=self.buildRelPath(self.parameters["scenarioStructure"]["path"],self.iniAbsPath)
        mappsCfgParams["ControlPanel"]["InputData"]["TimelineEvents"]["eventInputFile"]=os.path.basename(self.parameters["scenarioStructure"]["toplevelEvf"])
        mappsCfgParams["ControlPanel"]["InputData"]["TimelineEvents"]["exportXMLFormatEvents"]="false"
        mappsCfgParams["ControlPanel"]["InputData"]["TimelineEvents"]["resolveEvents"]="true"
        mappsCfgParams["ControlPanel"]["InputData"]["TimelineEvents"]["useAbsoluteTime"]="true"

        # [DataFiles]
        mappsCfgParams["DataFiles"]={}
        mappsCfgParams["DataFiles"]["agmInitConfigFile"] = os.path.basename(self.structure["agmCfg"]["agmCfgFile"])
        mappsCfgParams["DataFiles"]["configManualStartPage"]="CM/generated/MAPPSConfigurationManual.html"
        mappsCfgParams["DataFiles"]["datapackConfigIniFile"]="datapackConfig.ini"
        mappsCfgParams["DataFiles"]["datapackPanelIniFile"]="datapackPanel.ini"
        agmCfgAbsPath = os.path.normpath(os.path.join(self.iniAbsPath, "CONFIG"))
        mappsCfgParams["DataFiles"]["defaultPointingDefFile"] = self.buildRelPath(self.structure["agmCfg"]["defaultPointingDef"], agmCfgAbsPath) 
        mappsCfgParams["DataFiles"]["edfFile"]="EDF_JUICE.edf"
        mappsCfgParams["DataFiles"]["epsConfigFile"] = os.path.basename(self.structure["epsCfg"]["epsCfgFile"])
        mappsCfgParams["DataFiles"]["eventsDefFile"] = os.path.basename(self.structure["epsCfg"]["evtDefFile"])
        mappsCfgParams["DataFiles"]["gsVisPeriodsFile"] = os.path.basename(self.parameters["scenarioStructure"]["environment"]["trajectory"]["groundStationFile"])
        mappsCfgParams["DataFiles"]["gsVisPeriodsMethod"]="FromFile"
        mappsCfgParams["DataFiles"]["jplEphemerisDataFile"]="ENVIRONMENT/j2000.dat"
        mappsCfgParams["DataFiles"]["landersFile"]="LISTS/landers.asc"
        mappsCfgParams["DataFiles"]["landmarksFile"]="LISTS/landmarks.asc"
        mappsCfgParams["DataFiles"]["loadResourceProfile"]="false"
        mappsCfgParams["DataFiles"]["manualsCollection"]="mapps_1_5.qhc"
        mappsCfgParams["DataFiles"]["miraResourceProfile"]=""
        mappsCfgParams["DataFiles"]["observationDefFile"] = os.path.basename(self.parameters["scenarioStructure"]["definitions"]["observations"]["obsDefTopLevel"])
        mappsCfgParams["DataFiles"]["operationPeriodsFileTemplate"]=""
        mappsCfgParams["DataFiles"]["orbitDataFile"] = os.path.basename(self.parameters["scenarioStructure"]["environment"]["trajectory"]["trajectoryFile"])
        mappsCfgParams["DataFiles"]["orbitDefinitionFile"] = os.path.basename(self.parameters["scenarioStructure"]["environment"]["trajectory"]["periodDefinitionFile"])
        
        # [Overlays]
        mappsCfgParams["Overlays"]={}
        #removed due to timeline/tms
        #mappsCfgParams["Overlays"]["ExtList"] = self.parameters["elements"]["overlays"]["externals"]["list"]
        
        # [OverlayDataFiles]
        mappsCfgParams["OverlayDataFiles"]={}
        # removed due to timeline/tms
        #mappsCfgParams["OverlayDataFiles"]["fileList"] = self.parameters["elements"]["overlays"]["externals"]["fileList"]

        # [SimObjects]
        mappsCfgParams["SimObjects"]={}
        simObjAbsPath = os.path.normpath(os.path.join(self.iniAbsPath, mappsCfgParams["DataPaths"]["relConfigDataDir"]))
        trajParams = self.parameters["scenarioStructure"]["environment"]["trajectory"]

        # [SimObjects]\Europa
        mappsCfgParams["SimObjects"]["Europa"]={}
        mappsCfgParams["SimObjects"]["Europa"]["dataFileName"]   = self.buildRelPath(trajParams["europaTrjFile"], simObjAbsPath)
        
        # [SimObjects]\Ganymede
        mappsCfgParams["SimObjects"]["Ganymede"]={}
        mappsCfgParams["SimObjects"]["Ganymede"]["dataFileName"] = self.buildRelPath(trajParams["ganymedeTrjFile"], simObjAbsPath)
        
        # [SimObjects]\Callisto
        mappsCfgParams["SimObjects"]["Callisto"]={}
        mappsCfgParams["SimObjects"]["Callisto"]["dataFileName"] = self.buildRelPath(trajParams["callistoTrjFile"], simObjAbsPath)

        return mappsCfgParams

    def buildRelPath(self, path, refPath):
        return os.path.relpath(path, refPath).replace("\\","/")