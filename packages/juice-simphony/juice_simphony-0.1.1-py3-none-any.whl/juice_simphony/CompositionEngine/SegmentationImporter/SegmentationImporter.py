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
import xml.etree.ElementTree as et
from itertools import groupby
from operator import itemgetter
from datetime import datetime
import json

from .mapps_io import timeline
from .mapps_io import segDefinition
from .mapps_io import obsDefinition
from .mapps_io import toplevelObsDef
from .mapps_io import instToplevelObsDef
from .mapps_io import toplevelDefs
from .mapps_io import profileCsv
from juice_simphony.CompositionEngine.SegmentationImporter.shtRestClient import shtRestClient

import juice_simphony.spice_interface.spice_interface as spice_if
from juice_simphony.CompositionEngine.SegmentationImporter import segmentation_profiles as seg_prof

class segmentationTimeline(object):
    def __init__(self, *args, **kwargs):
        self.shtClient = shtRestClient(server="https://juicesoc.esac.esa.int")
        self.definitionsConfig = self.shtClient.getDefinitionsConfig()
        self.buildConfigMap()
        #self.dbConn    = self.initDb(R'Z:\Dev\Projects\Juice\juiceops\ScenarioGeneration\test.db')
        self.timeline      = 0
        self.origTimeline  = 0
        self.numOfSegments = 0
        self.segment_definitions       = {}
        self.observation_definitions   = {}
        self.traj_engineering_segments = []
        self.traj_platform_power_profile = []
        self.traj_eng_seg_defs = {}
        self.instProfile       = {}
        self.instTypeProfile   = {}
        self.validTimeline = False
        self.timeRange = {}
        self.unitConv = {}
        self.buildTableUnitConversions()
        self.spice = 0

        self.resources = seg_prof.timeline_resources()

        self.profile_category = {}
        self.profile_category["DATA_RATE"]   = "data"
        self.profile_category["DATA_VOLUME"] = "data"
        self.profile_category["POWER"]       = "power"
        self.profile_category["ENERGY"]      = "power"

    def initDb():
        #sqlite3.connect()
        #cursor = connection.cursor()
        """CREATE TABLE 'SegmentTimeline' (
                               'startTime' TIMESTAMP,
                               'endTime'   TIMESTAMP,
                               'close'   INTEGER,
                               'high'    INTEGER,
                               'low'     INTEGER,
                               'open'    INTEGER,
                               'volume'  INTEGER,
                               'symbol'  TEXT );"""

    def parseSpiceInfo(self, json_spice_info):

        # Parse spice info
        toolkit_version = json_spice_info['toolkit_version']
        spice = spice_if.instance(toolkit_version)
        json_kernels = json_spice_info['kernels']
        print("Spice skd_version:", json_kernels['skd_version'])
        seg_kernels_list = spice_if.kernels_list(toolkit_version,
                                                 json_kernels['skd_version'],
                                                 json_kernels['metakernel'])
        # Get the kernels
        for json_file in json_kernels['files']:
            seg_kernels_list.append(json_file['mnemonic'],
                                    json_file['name'],
                                    json_file['path'].replace("$KERNELS/",""))
        spice.kernels_list = seg_kernels_list

        return spice

    def ingestPlan(self,plan_id, startTime, endTime):

        # Download segmentation timeline
        self.report("Get segmentation timeline")
        
        self.origTimeline = self.getPlanTimeline(plan_id, startTime, endTime)
        #with open(R'Z:\VALIDATION\simphony\pcm\phs_pcm_test_001\segmentation_importer\timelines\Timeline_v13a.json') as json_file:
        #    self.origTimeline = json.load(json_file)
        self.timeline = self.origTimeline
        #with open(R'Z:\VALIDATION\simphony\pcm\phs_pcm_test_001\segmentation_importer\timelines\Timeline_v13a.json', 'w') as outfile:
        #   json.dump(self.origTimeline, outfile, indent=4)

        # Parse Spice Info 
        # Check "spice_info" node
        if 'spice_info' not in self.timeline:
            print ("Mandatory 'spice_info' field not found")
            return 0
        self.spice = self.parseSpiceInfo(self.timeline['spice_info'])

        # Get segmentation stats
        self.plan_id = plan_id
        self.timeline["segment_timeline"] = self.prepareTimeline(self.origTimeline["segment_timeline"], startTime, endTime)
        self.numOfSegments = self.getNumberOfSegments(self.timeline["segment_timeline"])
        self.report("Segments found: " + str(self.numOfSegments) + " Plan start time: " + str(self.timeRange["startTime"]) + " Plan end time: " + str(self.timeRange["endTime"]))
        
        self.xml_ptr = self.shtClient.getXmlPtrFilePath(self.plan_id, startTime="", endTime="")
        self.downloadXmlAttitude()

        # Get segment definitions
        self.report("Get segment definitions in timeline")
        self.segment_definitions   = self.getTimelineSegmDef(self.timeline["segment_timeline"])
        print ("Number of segment definitions: " + str(self.segment_definitions["numOfSegments"]))
        #self.segment_definitions = {}
        #self.segment_definitions["numOfSegments"] = 0

        # Get trajectory segment definitions
        self.report("Get segment definitions in trajectory")
        self.trajectory_segment_definitions = self.getTrajectorySegmDef(self.timeline["trajectory"], self.segment_definitions)
        print ("Number of trajectory segment definitions: " + str(self.trajectory_segment_definitions["numOfSegments"]))
        
        # Get observation definitionsn
        self.report("Get observation definitions in timeline")
        self.observation_definitions["global"]    = self.getObsDefs()
        print ("Number of global observation definitions: " + str(self.observation_definitions["global"]["numOfObservations"]))
        self.observation_definitions["scenario"]  = self.getTimelineObsDefsList(self.segment_definitions["list"], self.observation_definitions["global"])
        print ("Number of observation definitions: " + str(self.observation_definitions["scenario"]["numOfObservations"]))

        segment_definitions = {}
        segment_definitions["scenario"]   = self.segment_definitions
        segment_definitions["trajectory"] = self.trajectory_segment_definitions
        
        #with open(R'Z:\VALIDATION\simphony\pcm\profiles\phs_pcm_test_006\inputs\segment_timeline.json', 'w') as outfile:
        #   json.dump(self.timeline["segment_timeline"], outfile, indent=4)

        # Build resource profile
        self.report("Build resource profile")
        self.resources.generate_profiles(segment_definitions, self.timeline)

    def getPlanList(self, crema=""):
        if crema=="":
            planList = self.shtClient.getPlanList()
            if not planList:
                self.report("ERROR - Plan List is empty")
        else:
            planList = self.shtClient.getCremaPlanList(crema)
            if not planList:
                self.report("ERROR - Plan List is empty for " + crema)
        return (planList)

    def getPlanTimeline(self, plan_id, startTime, endTime):
        if (startTime!="" and endTime!=""):
            planTimeline = self.shtClient.genPlanTimeline(plan_id, startTime, endTime)
        else:
            planTimeline = self.shtClient.genPlanTimeline(plan_id)

        if not planTimeline:
            self.report("ERROR - Plan ID: " + str(plan_id) + " doesn't exist")
            return planTimeline
        #len(planTimeline["segments"])
        self.validTimeline = True
        return planTimeline

    def isValidTimeline(self):
        return self.validTimeline

    def get_segmentation_info(self):
        segmentation_info = {}
        segmentation_info["plan_id"]     = self.plan_id                 # 1
        segmentation_info["mnemonic"]    = self.timeline["mnemonic"]    # "CREMA_5_0_OPPORTUNITIES_v0"
        segmentation_info["name"]        = self.timeline["name"]        # "CREMA_5_0_OPPORTUNITIES_v0"
        segmentation_info["description"] = self.timeline["description"] # "1st run of opportunities generation (UC22), based on existing definitions of oppportunities (inherited from crema 3_0)"
        return segmentation_info

    def get_trajectory_info(self):
        trajectory_info = {}
        trajectory_info["trajectory"]  = self.timeline["trajectory"]  # "CREMA_5_0b23_1"
        return trajectory_info
        
    def get_spice_info(self):
        spice_info = self.timeline["spice_info"]
        return spice_info

    def getNumberOfSegments(self, segTimeline):
        return len(segTimeline)

    def size(self):
        return self.numOfSegments

    def prepareTimeline(self, segTimeline, startTime, endTime):
        listStart = []
        listEnd   = []
        filterTimeline = []
        timelineStartTime = datetime.strptime(startTime,"%Y-%m-%dT%H:%M:%S")
        timelineEndTime   = datetime.strptime(endTime,"%Y-%m-%dT%H:%M:%S")
        for segment in segTimeline:
            segment["startDatetime"]     = datetime.strptime(segment["start"],"%Y-%m-%dT%H:%M:%S.%fZ")
            segment["origStartDatetime"] = segment["startDatetime"]
            segment["endDatetime"]       = datetime.strptime(segment["end"],  "%Y-%m-%dT%H:%M:%S.%fZ")
            segment["origEndDatetime"]   = segment["endDatetime"]
            if segment["startDatetime"] <= timelineStartTime and timelineStartTime < segment["endDatetime"]:
                # Cut the timeline
                segment["startDatetime"] = timelineStartTime
                if segment["endDatetime"] >= timelineEndTime: segment["endDatetime"] = timelineEndTime
                # Append to the list
                listStart.append(segment["startDatetime"])
                listEnd.append(segment["endDatetime"])
                filterTimeline.append(segment)
            elif timelineStartTime < segment["startDatetime"] and segment["endDatetime"] < timelineEndTime:
                listStart.append(segment["startDatetime"])
                listEnd.append(segment["endDatetime"])
                filterTimeline.append(segment)
            elif segment["startDatetime"] < timelineEndTime and timelineEndTime <= segment["endDatetime"]:
                # Cut the timeline
                segment["endDatetime"] = timelineEndTime
                if segment["startDatetime"] <= timelineStartTime: segment["startDatetime"] = timelineStartTime
                # Append to the list
                listStart.append(segment["startDatetime"])
                listEnd.append(segment["endDatetime"])
                filterTimeline.append(segment)
        if bool(segTimeline) and (len(listStart)!=0) and (len(listEnd)!=0):
            self.timeRange["startTime"] = min(listStart)
            self.timeRange["endTime"]   = max(listEnd)
        else:
            self.timeRange["startTime"] = datetime.fromtimestamp(0.0)
            self.timeRange["endTime"]   = datetime.fromtimestamp(0.0)
        return filterTimeline

    def getTimelineStartEndTime(self, segTimeline):
        return self.timeRange
    
    def getTimelineSegmDef(self, segTimeline):
        segment_definitions = {}
        segment_definitions["list"] = {}
        for segment in segTimeline:
            if segment["segment_definition"] not in segment_definitions["list"]:
                segmentDefinition = self.shtClient.getSegmentDefintion(segment["segment_definition"])
                if not segmentDefinition:
                    self.report("ERROR - Segment definition: \"" + str(segment["segment_definition"]) + "\" doesn't exist")
                    continue
                
                if "pointing_request_file" in segmentDefinition: 
                    segmentDefinition["pointingText"] = self.shtClient.getFile(segmentDefinition["pointing_request_file"])

                instTargetMapList = []
                for inst in self.definitionsConfig["instruments"]:
                    instTargetMap = {}
                    instTargetMap["instName"] = inst["mnemonic"]
                    instTargetMap["target"] = ""
                    instTargetMapList.append(instTargetMap)
                segmentDefinition["instTargetMapList"] = instTargetMapList

                segment_definitions["list"][segment["segment_definition"]] = segmentDefinition

        segment_definitions["numOfSegments"] = len(segment_definitions["list"])
        return segment_definitions
    
    def getTrajectorySegmDef(self, trajectory, timeline_segments_definitions):
        tml_seg_defs_empty = timeline_segments_definitions["numOfSegments"] == 0
        trajectory_segment_definitions = {}
        trajectory_segment_definitions["list"] = {}
        traj_seg_defs_tmp = self.shtClient.getTrajSegmentDefinitions(trajectory)
        for segmentDefinition in traj_seg_defs_tmp:
            if segmentDefinition["mnemonic"] not in trajectory_segment_definitions["list"]:
                if not segmentDefinition:
                    self.report("ERROR - Segment definition: \"" + str(segmentDefinition["mnemonic"]) + "\" doesn't exist")
                    continue
                
                if "pointing_request_file" in segmentDefinition:
                    segmentDefinition["pointingText"] = self.shtClient.getFile(segmentDefinition["pointing_request_file"])

                instTargetMapList = []
                for inst in self.definitionsConfig["instruments"]:
                    instTargetMap = {}
                    instTargetMap["instName"] = inst["mnemonic"]
                    instTargetMap["target"] = ""
                    instTargetMapList.append(instTargetMap)
                segmentDefinition["instTargetMapList"] = instTargetMapList
                
                if tml_seg_defs_empty:
                   is_not_timeline_segment = True
                else:
                   is_not_timeline_segment = segmentDefinition["mnemonic"] not in timeline_segments_definitions["list"]

                if is_not_timeline_segment:
                   trajectory_segment_definitions["list"][segmentDefinition["mnemonic"]] = segmentDefinition

        trajectory_segment_definitions["numOfSegments"] = len(trajectory_segment_definitions["list"])
        return trajectory_segment_definitions

    def getNumOfTrajectorySegmDef(self):
       return self.trajectory_segment_definitions["numOfSegments"]
    
    def getNumOfTimelineSegmDef(self):
       return self.timeline_segment_definitions["numOfSegments"]

    def getTimelineObsDef(self, segDefList):
        observation_definitions = {}
        observation_definitions["list"] = {}
        for seg_def in segDefList.keys():
            if "observation_definitions" in segDefList[seg_def]:
                for obs_def in segDefList[seg_def]["observation_definitions"]:
                    if obs_def not in observation_definitions["list"]:
                        obsDefinition = self.shtClient.getObservationDefintion(obs_def)
                        if not obsDefinition:
                            self.report("ERROR - Observation definition: \"" + str(obs_def) + "\" doesn't exist")
                            continue

                        if "PTRSnippet_file" in obsDefinition: 
                            obsDefinition["pointingText"] = self.shtClient.getFile(obsDefinition["PTRSnippet_file"])

                        if "ITLSnippet_file" in obsDefinition: 
                            obsDefinition["timelineText"] = self.shtClient.getFile(obsDefinition["ITLSnippet_file"])
                        obsDefinition["isInSegTimeline"] = False
                        observation_definitions["list"][obs_def] = obsDefinition

        observation_definitions["numOfObservations"] = len(observation_definitions["list"])
        return observation_definitions

    def getTimelineObsDefsList(self, segDefList, obsDefList):
        observation_definitions = {}
        observation_definitions["list"] = {}
        for seg_def in segDefList.keys():
            if "observation_definitions" in segDefList[seg_def]:
                for obs_def in segDefList[seg_def]["observation_definitions"]:
                    if obs_def not in observation_definitions["list"]:
                        if obs_def not in obsDefList["list"]:
                            self.report("ERROR - Observation definition: \"" + str(obs_def) + "\" doesn't exist")
                            continue
                        observation_definitions["list"][obs_def] = obsDefList["list"][obs_def]
                        del obsDefList["list"][obs_def]
                        obsDefList["numOfObservations"] = obsDefList["numOfObservations"] - 1

        observation_definitions["numOfObservations"] = len(observation_definitions["list"])
        return observation_definitions

    def getObsDefs(self):
        observation_definitions = {}
        observation_definitions["list"] = {}
        observation_definitions_raw = []
        observation_definitions_raw = self.shtClient.getObservationDefintionsList()
        for obsDefinition in observation_definitions_raw:
            if "PTRSnippet_file" in obsDefinition:
                obsDefinition["pointingText"] = self.shtClient.getFile(obsDefinition["PTRSnippet_file"])

            if "ITLSnippet_file" in obsDefinition:
                obsDefinition["timelineText"] = self.shtClient.getFile(obsDefinition["ITLSnippet_file"])

            observation_definitions["list"][obsDefinition["mnemonic"]] = obsDefinition

        observation_definitions["numOfObservations"] = len(observation_definitions["list"])
        return observation_definitions

    def generateMappsfiles(self):
        test = test

    def generateObservationDefinitions(self, rootPath, path, scenarioID, instruments):
        obsDefInstruments = {}
        structure  = {}
        structure["path"] = path;
        structure["content"] = {};

        # Create the global observations
        globalFolderName = "GLOBAL"
        obsList = self.observation_definitions["global"]["list"]
        self.createObsDefFile(obsList, path, scenarioID, globalFolderName, structure["content"],instruments)

        # Create the scenario observations
        scenFolderName = "SCENARIO"
        obsList = self.observation_definitions["scenario"]["list"]
        self.createObsDefFile(obsList, path, scenarioID, scenFolderName, structure["content"],instruments)

        # TopLevel File
        structure["obsDefTopLevel"] = self.createTopLevelObsDefs(rootPath, path, scenarioID, structure["content"], instruments)
        #print ("STRUCTURE!!!!!!!!!!")
        #print ("===================")
        #print(json.dumps(structure, indent=4))
        return structure

    def createObsDefFile(self, obsList, path, scenarioID, subFolderName, contentStructure, instruments):
        # Iterate over the observations
        for obs in obsList:
            obsDef = obsList[obs]
            #print(obs, obsDef)
            if "payload" in obsDef:
                instrument = name2acronym(obsDef["payload"])
            else:
                print ("ERROR " + "\"payload\"" + " doesn't exist in obs: " + "\"" + obsDef["mnemonic"] + "\"" )
                continue

            if instrument in instruments:
               # ODF_3GM_SJS0001C30A_SXXPYY.def
               parameters = {}
               parameters["scenarioID"]= scenarioID
               parameters["prefix"]    = "ODF"
               parameters["type"]      = ""
               parameters["desc"]      = obsList[obs]["mnemonic"].upper().replace("-","_")
               parameters["startDate"] = ""
               parameters["endDate"]   = ""
               parameters["version"]   = "SXXPYY"
               parameters["ext"]       = "def"
               
               if obsDef["payload"] not in contentStructure:
                   contentStructure[instrument] = self.createFolderIfNotExist(path, instrument)
               
               if subFolderName not in contentStructure[name2acronym(obsDef["payload"])]:
                   contentStructure[instrument][subFolderName] = self.createFolderIfNotExist(contentStructure[instrument]["path"], subFolderName)

               # Create File
               obsDefGenerator = obsDefinition.obsDefinition(contentStructure[instrument][subFolderName]["path"], obsList[obs], parameters)
               contentStructure[instrument][subFolderName]["files"].append(obsDefGenerator.genFile())

            else: 
                print ("ERROR " + "Experiment " + obs + " not valid")

#    def createFolderIfNotExist(self, path, folderName):
#        # Create Folder
#        folderPath = os.path.join(path, folderName)
#        os.makedirs(folderPath, exist_ok=True)
#        structure = {}
#        structure["path"]  = folderPath
#        structure["files"] = []
#        print('Folder ' + folderName + ' created at ' + folderPath)
#        return structure

    def createFolderIfNotExist(self, path, folderName):
        folderPath = os.path.abspath(os.path.join(path, folderName))
    
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
            #print(f'Folder {folderName} created at: {folderPath}')
    
        return {
            "path": folderPath,
            "files": []
        }

    def createTopLevelExpObsDef(self, rootPath, path, scenarioID, exp, subFolderName, contentStructure):
         expParameters = {}
         expParameters["scenarioID"]   = scenarioID
         expParameters["experiment"]   = exp
         expParameters["type"]         = subFolderName
         expParameters["includeFiles"] = []
         if exp not in contentStructure:
            contentStructure[exp] = self.createFolderIfNotExist(path, exp)
         if subFolderName in contentStructure[exp]:
                 for fileItem in contentStructure[exp][subFolderName]["files"]:
                     includeFile = {}
                     includeFile["filePath"] = fileItem
                     if (subFolderName == "GLOBAL"):
                         includeFile["commented"] = True
                     else:
                         includeFile["commented"] = False
                     expParameters["includeFiles"].append(includeFile)
         else:
            contentStructure[exp][subFolderName] = self.createFolderIfNotExist(contentStructure[exp]["path"], subFolderName)
         includeFile = {}
         instTopFile = instToplevelObsDef.instToplevelObsDef(rootPath, contentStructure[exp][subFolderName]["path"], expParameters)
         includeFile["filePath"] = instTopFile.genFile()
         return includeFile
    
    def createTopLevelObsDefs(self, rootPath, path, scenarioID, contentStructure, instruments):
        topParameters = {}
        topParameters["scenarioID"]= scenarioID
        topParameters["includeFiles"] = []
        for exp in instruments:
            topParameters["includeFiles"].append(self.createTopLevelExpObsDef(rootPath, path, scenarioID, exp, "GLOBAL", contentStructure))
            topParameters["includeFiles"].append(self.createTopLevelExpObsDef(rootPath, path, scenarioID, exp, "SCENARIO",contentStructure))

        # Write Top Level Observation Definition file
        top = toplevelObsDef.toplevelObsDef(rootPath, path, topParameters)
        return top.genFile()
    
    def getNumOfTrajectorySegmDefs(self):
       return self.trajectory_segment_definitions["numOfSegments"]
    
    def getNumOfTimelineSegmDefs(self):
       return self.segment_definitions["numOfSegments"]

    def getNumOfSegmDefs(self):
       return self.trajectory_segment_definitions["numOfSegments"] + self.segment_definitions["numOfSegments"]

    def generateSegmentDefinitions(self, rootPath, scenarioID):
       structure  = {}
       structure["path"] = rootPath
       num_of_trajectory_segment_defs = self.getNumOfTrajectorySegmDefs()
       num_of_timeline_segment_defs   = self.getNumOfTimelineSegmDefs()

       if num_of_trajectory_segment_defs > 0:
          structure["segmentTrajectoryDefinitionFile"] = self.generateSegmentTrajectoryDefinitions(rootPath, scenarioID)

       if num_of_timeline_segment_defs > 0:
          structure["segmentTimelineDefinitionFile"]   = self.generateSegmentTimelineDefinitions  (rootPath, scenarioID)
       
       return structure

    def generateSegmentTrajectoryDefinitions(self, rootPath, scenarioID):
        parameters = {}
        parameters["scenarioID"]= scenarioID
        parameters["prefix"]    = "SDF"
        parameters["type"]      = "TRAJ"
        parameters["desc"]      = "SEGMENTS"
        parameters["startDate"] = ""
        parameters["endDate"]   = ""
        parameters["version"]   = 0
        parameters["ext"]       = "def"

        segDef = segDefinition.segDefinition(rootPath, self.trajectory_segment_definitions["list"], parameters)
        return segDef.genFile()

    def generateSegmentTimelineDefinitions(self, rootPath, scenarioID):
        parameters = {}
        parameters["scenarioID"]= scenarioID
        parameters["prefix"]    = "SDF"
        parameters["type"]      = ""
        parameters["desc"]      = "SEGMENTS"
        parameters["startDate"] = ""
        parameters["endDate"]   = ""
        parameters["version"]   = 0
        parameters["ext"]       = "def"

        segDef = segDefinition.segDefinition(rootPath, self.segment_definitions["list"], parameters)
        return segDef.genFile()

    def getInstrumentsTypes(self):
        self.instTypeDefs = self.shtClient.getInstrumentTypeDefs()
        #print(json.dumps(self.instTypeDefs, indent=4))

    def downloadXmlAttitude(self):
        self.xml_attitude = {}
        #self.timeline["ptr_file"] = "http://juicesoc.esac.esa.int/rest_api/file/trajectory%23CREMA_5_0.ptx/"
        if "ptr_file" in self.xml_ptr:
            xml_ptr_file = self.xml_ptr["ptr_file"]
            if xml_ptr_file != None:
               self.xml_attitude["xml_text"] = self.shtClient.downloadFile(xml_ptr_file)
               self.xml_attitude["xml_tree"] = et.fromstring(self.xml_attitude["xml_text"])
               self.xml_attitude["valid"]    = True
            return
        self.xml_attitude["valid"] = False

    def getXmlAttitude(self):
        return self.xml_attitude

    def getInstruments(self):
        self.instruments = self.shtClient.getInstruments()
        #print(json.dumps(self.instruments, indent=4))

    def generateDefinitions(self, rootPath, scenarioID, parameters):
        top = toplevelDefs.toplevelDefs(rootPath, rootPath, parameters)
        return top.genFile()

    def getTrajectoryEngSeg(self, crema_id):
        self.traj_engineering_segments = self.shtClient.getTrajEngSegments(crema_id)
        #with open(R'Z:\VALIDATION\simphony\pcm\data\tmp_files\eng_segments_timeline.json') as json_file:
        #    self.traj_engineering_segments = json.load(json_file)
    
    def getTrajEngSegTypes(self, crema_id):
        traj_eng_seg_defs = []
        traj_eng_seg_defs = self.shtClient.getTrajEngSegmentTypes(crema_id)
        #with open(R'Z:\VALIDATION\simphony\pcm\data\tmp_files\engineering_segment_types.json') as json_file:
        #    traj_eng_seg_defs = json.load(json_file)
        for traj_eng_seg_def in traj_eng_seg_defs:
            self.traj_eng_seg_defs[traj_eng_seg_def["mnemonic"]] = traj_eng_seg_def

    def intersectTimeRange(self, startTime, endTime, xml_seg_start_time, xml_seg_end_time, cut_block = True):
        cutted_block = False
        if endTime <= xml_seg_start_time: # st et xml_st xml_et
            return (False, cutted_block, xml_seg_start_time, xml_seg_end_time)
        else: 
            if xml_seg_end_time <= startTime: # xml_st xml_et st et 
              return (False, cutted_block, xml_seg_start_time, xml_seg_end_time)
            else: 
                if cut_block:
                   if endTime < xml_seg_end_time:  # xml_st et xml_et
                      # Cut block end time
                      xml_seg_end_time = endTime
                      cutted_block = True
                   if startTime > xml_seg_start_time:  # xml_st st xml_et
                      # Cut block start time
                      xml_seg_start_time = startTime
                      cutted_block = True
                return (True, cutted_block, xml_seg_start_time, xml_seg_end_time)

    def genPlatformPowerProfile(self, startTime, endTime):
        self.getTrajEngSegTypes ("CREMA_5_0")
        self.getTrajectoryEngSeg("CREMA_5_0")

        for engineering_segment in self.traj_engineering_segments:
            eng_start_time = engineering_segment["start"]
            eng_end_time   = engineering_segment["end"]
            intersect, cutted_block, xml_cut_start_time_dt, xml_cut_end_time_dt = self.intersectTimeRange(startTime, endTime, eng_start_time, eng_end_time)
            if intersect:
                power_entry = {}
                power_entry["abs_time"] = xml_cut_start_time_dt
                
                # Get segment definition from cache
                segment_definition   = self.traj_eng_seg_defs[engineering_segment["segment_type_raw"]]
                power_entry["value"] = segment_definition["power"]
                power_entry["desc"]  = segment_definition["description"]
                
                # Add the profile entry to the platform profile
                self.traj_platform_power_profile.append(power_entry)
        return self.traj_platform_power_profile

    def generateSegmentTimeline(self,rootPath, scenarioID):
        parameters = {}
        parameters["scenarioID"] = scenarioID
        parameters["prefix"]     = "ITL"
        parameters["type"]       = ""
        parameters["desc"]       = "SEGMENTS"
        parameters["startDate"]  = ""
        parameters["endDate"]    = ""
        parameters["version"]    = 0
        parameters["ext"]        = "itl"
        parameters["timelineStartTime"] = datetime.strftime(self.timeRange["startTime"],"%Y-%m-%dT%H:%M:%SZ")
        parameters["timelineEndTime"]   = datetime.strftime(self.timeRange["endTime"],  "%Y-%m-%dT%H:%M:%SZ")

        segDef = timeline.timeline(rootPath, self.timeline["segment_timeline"], parameters)
        #structure  = {}
        #structure["path"] = rootPath;

        # REMOVED SEGMENTS!
        structure = segDef.genFile()
        return structure

    def generateProfileCsv(self,rootPath, scenarioID):
        overlays = {}
        print("Run SegmentationImporter")
        # Set parameter for file generation
        parameters = {}
        parameters["scenarioID"] = scenarioID
        parameters["prefix"]     = "TMS"
        parameters["type"]       = ""
        parameters["desc"]       = "PROFILES"
        parameters["startDate"]  = ""
        parameters["endDate"]    = ""
        parameters["version"]    = 0
        parameters["ext"]        = "csv"
        parameters["timelineStartTime"] = self.timeRange["startTime"]
        parameters["timelineEndTime"]   = self.timeRange["endTime"]

        overlays["externals"] = {}
        overlays["externals"]["list"]      = []
        overlays["externals"]["fileList"]  = []
        index = 0;

        profile_value_types = {}
        profile_value_types['data']  = [["rate","data_rate","DATA_RATE"], ["volume","data_volume","DATA_VOLUME"], ["acc","data_accumulated","DATA_ACC"]]
        profile_value_types['power'] = [["rate","power","POWER"],         ["volume","energy","ENERGY"],           ["acc","energy_accumulated","ENERGY_ACC"]]

        for profile_type in self.resources.inst_type_profile:

           #print(self.resources.inst_type_profile)
           for profileInstType in self.resources.inst_type_profile[profile_type]:
              inst_type_res_profile = self.resources.inst_type_profile[profile_type]
              if inst_type_res_profile[profileInstType].start_time != 0:
                 for profile_value_type in profile_value_types[profile_type]:
                    parameters["desc"] = profileInstType
                    parameters["type"] = profile_value_type[2]
                    parameters["profile_value_type"] = profile_value_type
                    proCsv = profileCsv.profileCsv(rootPath, inst_type_res_profile[profileInstType], parameters)
                    index = index + 1
                    
                    if profile_value_type[0] == "rate":
                       unit = inst_type_res_profile[profileInstType].unit.rates
                    elif profile_value_type[0] == "volume":
                       unit = inst_type_res_profile[profileInstType].unit.volume
                    elif profile_value_type[0] == "acc":
                       unit = inst_type_res_profile[profileInstType].unit.acc
                    unit = seg_prof.unit_simph_to_mapps[unit]

                    fileEntry = {}
                    fileEntry["index"]      = index
                    fileEntry["dataColumn"] = 1
                    fileEntry["dataUnit"]   = unit
                    fileEntry["fileName"]   = proCsv.genFile()
                    fileEntry["skipRows"]   = 7
                    overlays["externals"]["fileList"].append(fileEntry)
                    
                    profileEntry = {}
                    profileEntry["index"]        = index
                    profileEntry["displayLabel"] = profileInstType + "_" + profile_value_type[1]
                    profileEntry["displayUnit"]  = unit
                    profileEntry["fileID"]       = index
                    overlays["externals"]["list"].append(profileEntry)

        for profile_type in self.resources.inst_profile:
           #print(profile_type)
           for profileInst in self.resources.inst_profile[profile_type]:
              inst_res_profile = self.resources.inst_profile[profile_type]
              if inst_res_profile[profileInst].start_time != 0:
                 for profile_value_type in profile_value_types[profile_type]:
                    parameters["desc"] = profileInst
                    parameters["type"] = profile_value_type[2]
                    proCsv = profileCsv.profileCsv(rootPath, inst_res_profile[profileInst], parameters)
                    index = index + 1
                    
                    if profile_value_type[0] == "rate":
                       unit = inst_res_profile[profileInst].unit.rates
                    elif profile_value_type[0] == "volume":
                       unit = inst_res_profile[profileInst].unit.volume
                    elif profile_value_type[0] == "acc":
                       unit = inst_res_profile[profileInst].unit.acc
                    unit = seg_prof.unit_simph_to_mapps[unit]

                    fileEntry = {}
                    fileEntry["index"]      = index
                    fileEntry["dataColumn"] = 1
                    fileEntry["dataUnit"]   = unit
                    fileEntry["fileName"]   = proCsv.genFile()
                    fileEntry["skipRows"]   = 7
                    overlays["externals"]["fileList"].append(fileEntry)
                    
                    profileEntry = {}
                    profileEntry["index"]        = index
                    profileEntry["displayLabel"] = "Segment " + profileInst + " " + profile_value_type[1]
                    profileEntry["displayUnit"]  = unit
                    profileEntry["fileID"]       = index
                    overlays["externals"]["list"].append(profileEntry)

        return overlays

    def generateProfileCsvOld(self,rootPath, scenarioID):
        overlays = {}
        
        # Set parameter for file generation
        parameters = {}
        parameters["scenarioID"] = scenarioID
        parameters["prefix"]     = "TMS"
        parameters["type"]       = ""
        parameters["desc"]       = "PROFILES"
        parameters["startDate"]  = ""
        parameters["endDate"]    = ""
        parameters["version"]    = 0
        parameters["ext"]        = "csv"
        parameters["timelineStartTime"] = self.timeRange["startTime"]
        parameters["timelineEndTime"]   = self.timeRange["endTime"]

        overlays["externals"] = {}
        overlays["externals"]["list"]      = []
        overlays["externals"]["fileList"]  = []
        index = 0;
        for profileInstType in self.instTypeProfile:
            if len(self.instTypeProfile[profileInstType]["profile"]) != 0:
                parameters["desc"] = profileInstType
                proCsv = profileCsv.profileCsv(rootPath, self.instTypeProfile[profileInstType]["profile"], parameters)
                index = index + 1

                fileEntry = {}
                fileEntry["index"]      = index
                fileEntry["dataColumn"] = 1
                fileEntry["dataUnit"]   = self.instTypeProfile[profileInstType]["unit"]
                fileEntry["fileName"]   = proCsv.genFile()
                fileEntry["skipRows"]   = 7
                overlays["externals"]["fileList"].append(fileEntry)

                profileEntry = {}
                profileEntry["index"]      = index
                profileEntry["displayLabel"] = profileInstType + " " + self.instTypeProfile[profileInstType]["caption"]
                profileEntry["displayUnit"]  = self.instTypeProfile[profileInstType]["unit"]
                profileEntry["fileID"]       = index
                overlays["externals"]["list"].append(profileEntry)

        for profileInst in self.instProfile:
            if len(self.instProfile[profileInst]["profile"]) != 0:
                parameters["desc"] = profileInst
                proCsv = profileCsv.profileCsv(rootPath, self.instProfile[profileInst]["profile"], parameters)
                index = index + 1

                fileEntry = {}
                fileEntry["index"]      = index
                fileEntry["dataColumn"] = 1
                fileEntry["dataUnit"]   = self.instProfile[profileInst]["unit"]
                fileEntry["fileName"]   = proCsv.genFile()
                fileEntry["skipRows"]   = 7
                overlays["externals"]["fileList"].append(fileEntry)

                profileEntry = {}
                profileEntry["index"]      = index
                profileEntry["displayLabel"] = "Segment " + profileInst + " " + self.instProfile[profileInst]["caption"]
                profileEntry["displayUnit"]  = self.instProfile[profileInst]["unit"]
                profileEntry["fileID"]       = index
                overlays["externals"]["list"].append(profileEntry)

        return overlays

    def initResourceProfiles(self):
        self.getInstrumentsTypes()
        self.getInstruments()
        self.instTypeProfile = {}

        for instTypeDef in self.instTypeDefs["instrument_types"]:
            self.instTypeProfile[instTypeDef["mnemonic"]] = {}
            self.instTypeProfile[instTypeDef["mnemonic"]]["numberOfEntries"]=0
            self.instTypeProfile[instTypeDef["mnemonic"]]["profile"]=[]

        for instDef in self.instruments["instruments"]:
            self.instProfile[instDef["mnemonic"]] = {}
            self.instProfile[instDef["mnemonic"]]["numberOfEntries"]=0
            self.instProfile[instDef["mnemonic"]]["profile"]=[]
        #print(json.dumps(self.instTypeProfile, indent=4))
        #print(json.dumps(self.instProfile, indent=4))

    def buildConfigMap(self):
        self.instrumentTypes = {}
        for instType in self.definitionsConfig["instrument_types"]:
            self.instrumentTypes[instType["mnemonic"]] = instType
        self.instGroupMap = {}
        for inst in self.definitionsConfig["instruments"]:
            self.instGroupMap[inst["mnemonic"]] = inst
            self.instGroupMap[inst["mnemonic"]]["groupList"] = []
            for instType in self.definitionsConfig["instrument_types"]:
                for typeInst in instType["instrument_set"]:
                    if inst["mnemonic"] == typeInst:
                        self.instGroupMap[inst["mnemonic"]]["groupList"].append(instType["mnemonic"])

    def buildResourceProfiles(self):
        segmentDefsList = self.segment_definitions["list"]
        for segCnt in range(len(self.timeline["segment_timeline"])):

            # Save segment instance
            segmentInstance = self.timeline["segment_timeline"][segCnt]
            self.timeline["segment_timeline"][segCnt]["instTypeMap"] = {}

            # Get observation definition
            if segmentInstance["segment_definition"] not in segmentDefsList:
                continue
            segDef = segmentDefsList[segmentInstance["segment_definition"]]

            # Calculate resources
            instTypeMap = {}
            resList = []
            if segmentInstance["overwritten"]:
                resList = segmentInstance["resources"]
            elif ("resources" in segDef):
                resList = segDef["resources"]

            for inst in self.definitionsConfig["instruments"]:
                    if not inst["mnemonic"] in instTypeMap: 
                        instTypeMap[inst["mnemonic"]] = ""

            for resInstance in resList:
                profileEntry = {}
                profileEntry["absTime"] = segmentInstance["startDatetime"]

                if resInstance["category"] == "DATA_VOLUME":
                    segDuration = (segmentInstance["origEndDatetime"]-segmentInstance["origStartDatetime"]).total_seconds()
                else:
                    segDuration = 1

                if resInstance["category"] == "DATA_VOLUME" or resInstance["category"] == "DATA_RATE":
                   profileEntry["unit"] = "kbits"
                   profileEntry["caption"] = "datarate"
                else:
                   profileEntry["unit"] = "w"
                   profileEntry["caption"] = "power"

                profileEntry["value"]  = (resInstance["value"] * self.unitConv[profileEntry["unit"]][resInstance["unit"]]) / segDuration
                profileEntry["origType"] = resInstance["category"]
                self.instTypeProfile[resInstance["instrument_type"]]["profile"].append(profileEntry)
                self.instTypeProfile[resInstance["instrument_type"]]["unit"] = profileEntry["unit"]
                self.instTypeProfile[resInstance["instrument_type"]]["caption"] = profileEntry["caption"]

                profileEntry = {}
                profileEntry["absTime"] = segmentInstance["endDatetime"]
                profileEntry["value"]   = 0.0
                self.instTypeProfile[resInstance["instrument_type"]]["profile"].append(profileEntry)

                # Build instrument/instrument type map
                for inst in self.instrumentTypes[resInstance["instrument_type"]]["instrument_set"]:
                    if inst in instTypeMap:
                        if instTypeMap[inst] == "":
                             instTypeMap[inst] = resInstance["target"]
                    else: instTypeMap[inst] = resInstance["target"]
                for inst in self.definitionsConfig["instruments"]:
                    if not inst["mnemonic"] in instTypeMap:
                        instTypeMap[inst["mnemonic"]] = ""

            self.timeline["segment_timeline"][segCnt]["instTypeMap"] = instTypeMap

            resList = []
            if segmentInstance["instrument_overwritten"]:
                resList = segmentInstance["instrument_resources"] 
            elif ("instrument_resources" in segDef):
                resList = segDef["instrument_resources"]

            for resInstance in resList:
                profileEntry = {}
                profileEntry["absTime"] = segmentInstance["startDatetime"]
                if resInstance["category"] == "DATA_VOLUME":
                    segDuration = (segmentInstance["origEndDatetime"]-segmentInstance["origStartDatetime"]).total_seconds()
                else:
                    segDuration = 1

                if resInstance["category"] == "DATA_VOLUME" or resInstance["category"] == "DATA_RATE":
                   profileEntry["unit"]    = "kbits"
                   profileEntry["caption"] = "datarate"
                else:
                   profileEntry["unit"]    = "w"
                   profileEntry["caption"] = "power"

                profileEntry["value"]  = (resInstance["value"] * self.unitConv[profileEntry["unit"]][resInstance["unit"]]) / segDuration
                profileEntry["origType"] = resInstance["category"]
                self.instProfile[resInstance["instrument"]]["profile"].append(profileEntry)
                self.instProfile[resInstance["instrument"]]["unit"]    = profileEntry["unit"]
                self.instProfile[resInstance["instrument"]]["caption"] = profileEntry["caption"]

                profileEntry = {}
                profileEntry["absTime"] = segmentInstance["endDatetime"]
                profileEntry["value"]   = 0.0
                self.instProfile[resInstance["instrument"]]["profile"].append(profileEntry)
    
    def calculateProfileValues(self, res_inst_cat, duration, src_unit, dest_unit, value):

       if res_inst_cat == "DATA_VOLUME":
           # Convert 
           profile_data_volume = (value * self.unitConv[src_unit][dest_unit])
           profile_data_rates  = profile_data_volume/duration

       elif res_inst_cat == "DATA_RATE":
           # Convert 
           profile_data_rates  = (value * self.unitConv[src_unit][dest_unit])
           profile_data_volume = profile_data_rates * duration

       elif res_inst_cat == "POWER":
           # Convert 
           profile_data_rates  = (value * self.unitConv[src_unit][dest_unit])
           profile_data_volume = profile_data_rates * (duration/3600)

       elif res_inst_cat == "ENERGY":
           # Convert 
           profile_data_volume  = (value * self.unitConv[src_unit][dest_unit])
           profile_data_rates   = profile_data_rates / (duration/3600)

       # Return values
       return profile_data_rates, profile_data_volume

    def buildProfileEntry(self, resInstance, date_time_entry, acc_value):
       profile_entry = {}
       res_inst_type = resInstance["instrument_type"]
       res_inst_cat  = resInstance["category"]

       # Profile (absTime, category)
       profile_entry["absTime"]  = date_time_entry
       profile_entry["category"] = self.profile_category[res_inst_cat]

       # Profile (rates_unit, volume_unit, caption)
       if profile_entry["category"] == "data":
          profileRatesUnit  = "kbits/sec"
          profileVolumeUnit = "kbits"
          profileCaption    = "datarate"
       else:
          profileRatesUnit  = "w"
          profileVolumeUnit = "wh"
          profileCaption    = "power"

       profile_entry["rates_unit"]  = profileRatesUnit  
       profile_entry["volume_unit"] = profileVolumeUnit
       profile_entry["caption"]     = profileCaption  

       segDuration = (origEndDatetime - origStartDatetime).total_seconds()
       self.calculateProfileValues()
       profile_entry["acc_value"]    = acc_value 
       profile_entry["rates_value"]  = profile_data_rates
       profile_entry["volume_value"] = 0.0

    def extractProfile(self, resList, startTime, endTime):
       profile_acc_value = {}
       for resInstance in resList:
           # Process the profile depending on the category
           # ----------------------------------------------
           
           buildProfileEntry(self, resInstance, date_time_entry, profile_acc_value[profileEntry["category"]])

           profileEntry["origType"] = res_inst_cat
           self.instTypeProfile[res_inst_type]["profile"].append(profileEntry)
           self.instTypeProfile[res_inst_type]["rates_unit"]  = profileEntry["rates_unit"] 
           self.instTypeProfile[res_inst_type]["volume_unit"] = profileEntry["volume_unit"]
           self.instTypeProfile[res_inst_type]["caption"]     = profileEntry["caption"]
           self.instTypeProfile[res_inst_type]["cat_type"]    = profile_category[res_inst_cat]

           # Calculate the segment final profile
           profileEntry = {}
           profileEntry["absTime"]  = segmentInstance["endDatetime"]
           profileEntry["category"] = profile_category[res_inst_cat]

           # Update profile values
           profileEntry["rates_value"]  = 0.0
           profileEntry["volume_value"] = profile_data_volume

           # Update profile data
           profileEntry["rates_unit"]   = profileRatesUnit
           profileEntry["volume_unit"]  = profileVolumeUnit
           profileEntry["caption"]      = profileCaption

           # Calculate the segment acc data volume
           if res_inst_type in profile_acc_value:
              profile_acc_value[res_inst_type]["power"] = 0.0
              profile_acc_value[res_inst_type]["data"]  = 0.0
           
           prev_acc_value = profile_acc_value[res_inst_type][profileEntry["category"]]
           prev_acc_value = prev_acc_value + profile_data_volume
           profileEntry["acc_value"] = prev_acc_value
           profile_acc_value[res_inst_type][profileEntry["category"]] = prev_acc_value

           self.instTypeProfile[resInstance["instrument_type"]]["profile"].append(profileEntry)

           # Build instrument/instrument type map
           for inst in self.instrumentTypes[resInstance["instrument_type"]]["instrument_set"]:
               if inst in instTypeMap:
                   if instTypeMap[inst] == "":
                        instTypeMap[inst] = resInstance["target"]
               else: instTypeMap[inst] = resInstance["target"]
           for inst in self.definitionsConfig["instruments"]:
               if not inst["mnemonic"] in instTypeMap:
                   instTypeMap[inst["mnemonic"]] = ""

    def buildResourceProfilesAcc(self):

        segmentDefsList = self.segment_definitions["list"]

        # Reset Accumulation counters
        profile_acc_value ={}
        profile_acc_value_inst = {}

        for segCnt in range(len(self.timeline["segment_timeline"])):

            # Save segment instance
            segmentInstance = self.timeline["segment_timeline"][segCnt]
            self.timeline["segment_timeline"][segCnt]["instTypeMap"] = {}

            # Get segment definition
            segmentDefMnemonic = segmentInstance["segment_definition"]
            if segmentDefMnemonic not in segmentDefsList:
                continue
            segDef = segmentDefsList[segmentDefMnemonic]

            # Extract resources
            # -------------------
            instTypeMap = {}
            resList     = []

            # Check if the resources defined in the instance is overwritting 
            # the resources define in the definition
            if segmentInstance["overwritten"]:
                resList = segmentInstance["resources"]
            elif ("resources" in segDef):
                resList = segDef["resources"]

            # Create Instrument Map List
            for inst in self.definitionsConfig["instruments"]:
                if not inst["mnemonic"] in instTypeMap: 
                    instTypeMap[inst["mnemonic"]] = ""

            # Extract Instrument Type Profiles
            # ---------------------------------
            for resInstance in resList:
                res_inst_type = resInstance["instrument_type"]
                res_inst_cat  = resInstance["category"]
                profileEntry = {}
                profileEntry["absTime"]  = segmentInstance["startDatetime"]
                profileEntry["category"] = profile_category[res_inst_cat]
                
                if profileEntry["category"] == "data":
                   profileRatesUnit  = "kbits/sec"
                   profileVolumeUnit = "kbits"
                   profileCaption    = "datarate"
                else:
                   profileRatesUnit  = "w"
                   profileVolumeUnit = "wh"
                   profileCaption    = "power"

                profileEntry["rates_unit"]  = profileRatesUnit  
                profileEntry["volume_unit"] = profileVolumeUnit
                profileEntry["caption"]     = profileCaption  
                
                # Process the profile depending on the category
                # ----------------------------------------------

                segDuration = (segmentInstance["origEndDatetime"] - segmentInstance["origStartDatetime"]).total_seconds()
                if res_inst_cat == "DATA_VOLUME":
                    # Convert 
                    profile_data_volume = (resInstance["value"] * self.unitConv[profileEntry["volume_unit"]][resInstance["unit"]])
                    profile_data_rates  = profile_data_volume/segDuration

                elif res_inst_cat == "DATA_RATE":
                    # Convert 
                    profile_data_rates  = (resInstance["value"] * self.unitConv[profileEntry["volume_unit"]][resInstance["unit"]])
                    profile_data_volume = profile_data_rates * segDuration

                elif res_inst_cat == "POWER":
                    # Convert 
                    profile_data_rates  = (resInstance["value"] * self.unitConv[profileEntry["volume_unit"]][resInstance["unit"]])
                    profile_data_volume = profile_data_rates * (segDuration/3600)

                elif res_inst_cat == "ENERGY":
                    # Convert 
                    profile_data_volume  = (resInstance["value"] * self.unitConv[profileEntry["volume_unit"]][resInstance["unit"]])
                    profile_data_rates   = profile_data_rates / (segDuration/3600)

                # Update profile values
                profileEntry["acc_value"]    = profile_acc_value[profileEntry["category"]]
                profileEntry["rates_value"]  = profile_data_rates
                profileEntry["volume_value"] = 0.0

                profileEntry["origType"] = res_inst_cat
                self.instTypeProfile[res_inst_type]["profile"].append(profileEntry)
                self.instTypeProfile[res_inst_type]["rates_unit"]  = profileEntry["rates_unit"] 
                self.instTypeProfile[res_inst_type]["volume_unit"] = profileEntry["volume_unit"]
                self.instTypeProfile[res_inst_type]["caption"]     = profileEntry["caption"]
                self.instTypeProfile[res_inst_type]["cat_type"]    = profile_category[res_inst_cat]

                # Calculate the segment final profile
                profileEntry = {}
                profileEntry["absTime"]  = segmentInstance["endDatetime"]
                profileEntry["category"] = profile_category[res_inst_cat]

                # Update profile values
                profileEntry["rates_value"]  = 0.0
                profileEntry["volume_value"] = profile_data_volume

                # Update profile data
                profileEntry["rates_unit"]   = profileRatesUnit
                profileEntry["volume_unit"]  = profileVolumeUnit
                profileEntry["caption"]      = profileCaption

                # Calculate the segment acc data volume
                if res_inst_type in profile_acc_value:
                   profile_acc_value[res_inst_type]["power"] = 0.0
                   profile_acc_value[res_inst_type]["data"]  = 0.0
                
                prev_acc_value = profile_acc_value[res_inst_type][profileEntry["category"]]
                prev_acc_value = prev_acc_value + profile_data_volume
                profileEntry["acc_value"] = prev_acc_value
                profile_acc_value[res_inst_type][profileEntry["category"]] = prev_acc_value

                self.instTypeProfile[resInstance["instrument_type"]]["profile"].append(profileEntry)

                # Build instrument/instrument type map
                for inst in self.instrumentTypes[resInstance["instrument_type"]]["instrument_set"]:
                    if inst in instTypeMap:
                        if instTypeMap[inst] == "":
                             instTypeMap[inst] = resInstance["target"]
                    else: instTypeMap[inst] = resInstance["target"]
                for inst in self.definitionsConfig["instruments"]:
                    if not inst["mnemonic"] in instTypeMap:
                        instTypeMap[inst["mnemonic"]] = ""

            self.timeline["segment_timeline"][segCnt]["instTypeMap"] = instTypeMap

            # Prepare Instrument Profiles
            # ----------------------------
            resList = []
            if segmentInstance["instrument_overwritten"]:
                resList = segmentInstance["instrument_resources"] 
            elif ("instrument_resources" in segDef):
                resList = segDef["instrument_resources"]
            
            # Extract Instrument Profiles
            # ----------------------------
            for resInstance in resList:
                profileEntry = {}
                profileEntry["absTime"]  = segmentInstance["startDatetime"]
                profileEntry["category"] = profile_category[resInstance["category"]]

                if resInstance["category"] == "DATA_VOLUME":
                    segDuration = (segmentInstance["origEndDatetime"] - segmentInstance["origStartDatetime"]).total_seconds()
                else:
                    segDuration = 1

                if resInstance["category"] == "DATA_VOLUME" or resInstance["category"] == "DATA_RATE":
                   profileEntry["unit"]    = "kbits"
                   profileEntry["caption"] = "datarate"
                else:
                   profileEntry["unit"]    = "w"
                   profileEntry["caption"] = "power"
                
                profile_data_volume = (resInstance["value"] * self.unitConv[profileEntry["unit"]][resInstance["unit"]])
                profileEntry["value"] = profile_data_volume / segDuration
                
                if profileEntry["caption"] in profile_acc_value_inst:
                  profile_acc_value_inst[resInstance["instrument"]] = {}
                  profile_acc_value_inst[resInstance["instrument"]]["power"]    = 0.0
                  profile_acc_value_inst[resInstance["instrument"]]["data"] = 0.0
                
                if profileEntry["caption"] == "datarate":
                  profile_acc_value_inst[resInstance["instrument"]] = profile_acc_value_inst[resInstance["instrument"]] + profile_data_volume
                  profileEntry["acc_value"] = profile_acc_value_inst[resInstance["instrument"]]

                profileEntry["origType"] = resInstance["category"]
                if resInstance["instrument"] not in self.instProfile:
                   self.instProfile[resInstance["instrument"]] = {}
                self.instProfile[resInstance["instrument"]]["profile"].append(profileEntry)
                self.instProfile[resInstance["instrument"]]["unit"] = profileEntry["unit"]
                self.instProfile[resInstance["instrument"]]["caption"] = profileEntry["caption"]

                profileEntry = {}
                if resInstance["category"] == "DATA_VOLUME" or resInstance["category"] == "DATA_RATE":
                   profileEntry["unit"] = "kbits"
                   profileEntry["caption"] = "datarate"
                else:
                   profileEntry["unit"] = "w"
                   profileEntry["caption"] = "power"

                profileEntry["absTime"] = segmentInstance["endDatetime"]
                profileEntry["value"]   = 0.0
                if profileEntry["caption"] == "datarate":
                  profile_acc_value[profileEntry["caption"]] = profile_acc_value[profileEntry["caption"]] + profile_data_volume
                  profileEntry["acc_value"]                  = profile_acc_value[profileEntry["caption"]]

                self.instProfile[resInstance["instrument"]]["profile"].append(profileEntry)
    
    def buildTableUnitConversions(self):
        unitList = []
        unitRate = {}
        unitRate["bits"]  = 0.001
        unitRate["kbits"] = 1
        unitRate["mbits"] = 1000
        unitRate["gbits"] = 1000000
        unitRate["bps"]   = 0.001 
        unitRate["kbps"]  = 1
        unitRate["mbps"]  = 1000
        self.unitConv["kbits"] = unitRate

        unitRate = {}
        unitRate["W"] = 1
        self.unitConv["w"] = unitRate

    def report(self, text):
        print(text)

    def getTrajectory(self):
        # CREMA_5_0 CREMA_5_0b23_1
        return self.timeline["trajectory"]
    
    # --------------------------
    #  Scenario Profiles
    # --------------------------

    def calculate_profiles(self):
       self.resources.generate_profiles(self.segment_definitions)

class segmentation(object):
    def __init__(self, *args, **kwargs):
        self.shtClient = shtRestClient(server="https://juicesoc.esac.esa.int")

    def getPlanList(self, crema=""):
        if crema=="":
            planList = self.shtClient.getPlanList()
            if not planList:
                self.report("ERROR - Plan List is empty")
        else:
            planList = self.shtClient.getCremaPlanList(crema)
            if not planList:
                self.report("ERROR - Plan List is empty for " + crema)
        return (planList)


def name2acronym(name):
    
    instrument_dict = {
    'SOC':       'SOC',
    '3GM':       '3GM',
    'GALA':      'GAL',
    'JANUS':     'JAN',
    'JMAG':      'MAG',
    'JMC':       'JMC',
    'MAJIS':     'MAJ',
    'NAVCAM':    'NAV',
    'PEPLO':     'PEH',
    'PEPHI':     'PEL',    
    'PRIDE':     'PRI',
    'RIME':      'RIM',
    'RPWI':      'RPW',
    'SWI':       'SWI',
    'UVS':       'UVS',
    'JUICE':     'JUI'
    }

    return instrument_dict[name]



if __name__ == "__main__":
    
    # Segmentation timeline Test
    # ----------------------------
    segTimeline = segmentationTimeline()
    startTime = "2032-05-10T08:33:51Z"
    endTime   = "2032-09-25T23:58:51Z"
    print(segTimeline.genPlatformPowerProfile(startTime, endTime))


    #print(segTimeline.getPlanList())
    #segTimeline.downloadXmlAttitude()
    #print(segTimeline.getXmlAttitude())
    #segTimeline.buildConfigMap()
    #segTimeline.ingestPlan(51,"","")
    #segTimeline.ingestPlan(51,"2031-07-22T20:45:53","2032-02-13T17:20:31")
    #segTimeline.initResourceProfiles()
    #segTimeline.buildResourceProfiles()
    #segTimeline.getInstrumentsTypes()
    #segTimeline.getInstruments()
    
    #segTimeline.generateSegmentTimeline(R'Z:\Resources\Output',"SJS0001C30A")
    #segTimeline.generateSegmentTimeline(R'Z:\Dev\Projects\Juice\juiceops\ScenarioGeneration',"SJS0001C30A")
    #segTimeline.generateSegmentDefinitions(R'Z:\Dev\Projects\Juice\juiceops\ScenarioGeneration',"SJS0001C30A")
    #segTimeline.generateProfileCsv(R'Z:\Resources',"SJS0001C30A")
    #segTimeline.buildTableUnitConversions()
    
    #test =  segTimeline.generateObservationDefinitions("Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/definitions", instruments)
    #print(json.dumps(test, indent=4))
    
    '''
    parameters = {}
    parameters["scenarioID"]= "SJS0001C30A"
    parameters["includeFiles"] = [
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/3GM/ODF_SJS0001C30A_3GM.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/GALA/ODF_SJS0001C30A_GALA.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/MAJIS/ODF_SJS0001C30A_MAJIS.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/JANUS/ODF_SJS0001C30A_JANUS.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/PEP/ODF_SJS0001C30A_PEP.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/JMAG/ODF_SJS0001C30A_JMAG.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/RIME/ODF_SJS0001C30A_RIME.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/RPWI/ODF_SJS0001C30A_RPWI.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/SWI/ODF_SJS0001C30A_SWI.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/UVS/ODF_SJS0001C30A_UVS.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/JUICE/ODF_SJS0001C30A_JUICE_SPC.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/SEGMENTS/SEGMENTS.def"}
        ]
    
    top = toplevelObsDef.toplevelObsDef("Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration", parameters)
    print (top.genFile())
    
    
    parameters = {}
    parameters["scenarioID"]= "SJS0001C30A"
    parameters["experiment"]= "MAJIS"
    parameters["includeFiles"] = [
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/3GM/ODF_SJS0001C30A_3GM.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/GALA/ODF_SJS0001C30A_GALA.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/MAJIS/ODF_SJS0001C30A_MAJIS.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/JANUS/ODF_SJS0001C30A_JANUS.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/PEP/ODF_SJS0001C30A_PEP.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/JMAG/ODF_SJS0001C30A_JMAG.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/RIME/ODF_SJS0001C30A_RIME.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/RPWI/ODF_SJS0001C30A_RPWI.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/SWI/ODF_SJS0001C30A_SWI.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/UVS/ODF_SJS0001C30A_UVS.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/JUICE/ODF_SJS0001C30A_JUICE_SPC.def"},
        {"fileDescription" : "test",
         "filePath" : "Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration/SEGMENTS/SEGMENTS.def"}
        ]
    
    top = instToplevelObsDef.instToplevelObsDef("Z:/Dev/Projects/Juice/juiceops/ScenarioGeneration", parameters)
    print (top.genFile())
    '''
    
    #client.getPlanList()
    #client.getCremaPlanList("CREMA_5_0")
    
    #client = shtRestClient(server="https://juicesoc.esac.esa.int")
    #print (client.getFile("http://juicesoc.esac.esa.int/rest_api/file/segment_definitions%23ptr%23JM_CB.xml"))
    
    #client.genPlanTimeline(17)
    #test = client.getSegmentDefintion("TE")
    #print ('Output: ')
    #print ('--------')
    #print (test)
    #if test:
    #    print("VALID")
    #else:
    #    print("NOT VALID")
    #print ('------------------------------------------------------------')
    #print ('************************************************************')
    #print ('------------------------------------------------------------')
    #print(json.dumps(test, indent=4))
    
    #client.getObservationDefintion("3GM_HAA_STANDBY")
    
    #segTimeline = segmentationTimeline()
    
    #from class2 import class2
    #
    #parameters = {}
    #parameters["test"] = 1;
    #
    #classTest = class2(parameters)
    #classTest.test1()
    
    #from mapps_io.timeline import timeline
    #
    #params = {}
    #params["type"]    = "ITL"
    #params["desc"]    = "TEST"
    #params["scenarioID"] = "TR001A"
    #params["version"] = 1
    #params["addScenarioID"] = True
    #params["prefix"] = "ITL"
    #params["ext"]    = "itl"
    #
    #tml = timeline(R"Z:\Resources\Juice\Test\Simphony\test", params)
    #tml.genFile()
    
    #plan_tml_json = dict()
    #configPath = R"Z:\Resources\Juice\Test\Simphony\test\json_seg_timeline.txt"
    #
    ## Load scenario generation configuration file
    #with open(configPath) as json_file:
    #   plan_tml_json = json.load(json_file)
    #
    #
    #listStart = []
    #listEnd   = []
    #for segment in plan_tml_json["segments"]:
    #    listStart.append(segment["start"])
    #    listEnd.append(segment["end"])
    #
    #print(listStart)
    #print(min(listStart))
    #print(max(listEnd))
    
    #################################################
    
    
            #print(json.dumps(self.observation_defs_list, indent=4))
    
            #c = self.dbConn.cursor()
            #c.execute("CREATE TABLE plan_tml(id integer, data json)")
    
            #"start",
            #"end",
            #"segment_definition",
            #"overwritten",
            #"instrument_overwritten",
            #"timeline"