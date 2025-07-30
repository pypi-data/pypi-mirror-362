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
from juice_simphony.CompositionEngine.Scenario.common import utils
from juice_simphony.CompositionEngine.Scenario.definitions.toplevelObsDef import toplevelObsDef
from juice_simphony.CompositionEngine.SegmentationImporter.SegmentationImporter import segmentationTimeline

class definitions:

    def __init__(self, segmentationTimelineInst, root_path, parameters=0):
        self.root_path = root_path
        self.segTimeline = segmentationTimelineInst
        self.parameters = parameters
        self.mainFolderPath = ""
        self.structure = dict()

    def build(self):
        self.createMainFolder('OBSERVATIONS')
        print("Add OBSERVATIONS section")
        self.structure["path"]         = self.mainFolderPath;
        #self.structure["observations"] = self.addObsSection('OBSERVATIONS')
        self.structure["observations"] = self.addObsSection()

        if (self.segTimeline.getNumOfSegmDefs()>0):
            self.structure["segments"] = self.addSegmentSection('SEGMENTS')

        self.structure["topLevelObsDefFile"] = self.addRootContent()
        # REMOVED by PE!
        #self.structure["topLevelObsDefFile"] = None

        return self.structure

    def createMainFolder(self, folderName):
        self.mainFolderPath = utils.createFolder(self.root_path, folderName)

    def addObsSection(self):
        #folderPath = utils.createFolder(self.mainFolderPath, folderName)
        folderPath = self.mainFolderPath
        instruments = \
        {
           "3GM":{},
           "GAL":{},
           "MAJ":{},
           "JAN":{},
           "PEH":{},
           "PEL":{},
           "MAG":{},
           "RIM":{},
           "RPW":{},
           "SWI":{},
           "UVS":{},
           "JUI":{}
        }

        return self.segTimeline.generateObservationDefinitions(
            self.mainFolderPath,
            folderPath,
            self.parameters["scenarioID"],
            instruments
        )

    def addSegmentSection(self,folderName):
        folderPath = utils.createFolder(self.mainFolderPath, folderName)
        return self.segTimeline.generateSegmentDefinitions(folderPath, self.parameters["scenarioID"])

    def addRootContent(self):

        # Observation definition top level
        # --------------------------------
        structure = {}
        topParameters = {}
        topParameters["scenarioID"] = self.parameters["scenarioID"]
        topParameters["includeFiles"] = []

        includeFile = {}
        includeFile["filePath"] = self.structure["observations"]["obsDefTopLevel"]
        structure["topLevelObsDefFile"] = self.structure["observations"]["obsDefTopLevel"]
        topParameters["includeFiles"].append(includeFile)

        if "segments" in self.structure:
            if "segmentTrajectoryDefinitionFile" in self.structure["segments"]:
                includeFile = {}
                includeFile["filePath"] = self.structure["segments"]["segmentTrajectoryDefinitionFile"]
                includeFile["commented"] = True
                topParameters["includeFiles"].append(includeFile)
        
            if "segmentTimelineDefinitionFile" in self.structure["segments"]:
                includeFile = {}
                includeFile["filePath"] = self.structure["segments"]["segmentTimelineDefinitionFile"]
                includeFile["commented"] = False
                topParameters["includeFiles"].append(includeFile)

        return self.segTimeline.generateDefinitions(self.mainFolderPath, self.parameters["scenarioID"], topParameters)

#    def addRootPlaceHolder(self):
#        structure = {}
#        tlObsDefParams = dict()
#        tlObsDefParams["scenarioID"] = self.parameters["scenarioID"]
#        tlObsDef = toplevelObsDef(self.mainFolderPath, tlObsDefParams)
#        filePath = os.path.normpath(os.path.join(self.parameters["refScenarioPath"], "ODF_TPL0001A_TOP_LEVEL.def"))
#        structure["topLevelObsDefFile"] = tlObsDef.genFile(filePath)
#        return structure