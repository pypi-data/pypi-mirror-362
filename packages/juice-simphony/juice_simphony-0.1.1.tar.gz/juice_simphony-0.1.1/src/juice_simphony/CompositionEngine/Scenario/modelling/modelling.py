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
from juice_simphony.CompositionEngine.Scenario.common import utils
from juice_simphony.CompositionEngine.Scenario.modelling.toplevelEdf import toplevelEdf
from juice_simphony.CompositionEngine.Scenario.modelling.experiment.experiment import experiment
import distutils.dir_util
import os
from distutils.dir_util import copy_tree
import errno, os
import shutil

from dotenv import load_dotenv
load_dotenv()


class modelling:

    def __init__(self, root_path, parameters=0):
        self.root_path = root_path
        self.parameters = parameters
        self.mainFolderPath = ""
        self.structure = {}

    def build(self):
        self.createMainFolder('MODELLING')
        print("Add MODELLING section")
        self.structure["path"] = self.mainFolderPath
        juice_conf = self.parameters['conf_repo']['juice_conf']
        refModellingPath = os.path.normpath(os.path.join(juice_conf,"internal/phs/eps", "modelling"))
        try:
            if os.path.exists(self.mainFolderPath):
                 shutil.rmtree(self.mainFolderPath)
            shutil.copytree(refModellingPath, self.mainFolderPath)
        except OSError as exc: 
              raise
        self.structure["toplevelEdf"] = os.path.normpath(os.path.join(self.mainFolderPath, "EDF_JUICE.edf"))
        return self.structure

    def createMainFolder(self, folderName):
        self.mainFolderPath = utils.createFolder(self.root_path, folderName)

    def addRootContent(self):
        structure = dict()

        # Observation definition top level
        # --------------------------------
        tlEdfParams = dict()
        tlEdfParams["scenarioID"] = self.parameters["scenarioID"]
        tlEdf = toplevelEdf(self.mainFolderPath, tlEdfParams)
        filePath = os.path.normpath(os.path.join(self.parameters["refScenarioPath"], R"MODELLING/EDF_JUICE.edf"))
        structure["toplevelEdf"] = tlEdf.genFile(filePath)
        return structure

    def addExperimentModelSection(self,instName):
        tlEdfParams = dict()
        tlEdfParams["scenarioID"]  = self.parameters["scenarioID"]
        expModelSection = experiment(self.mainFolderPath, instName, tlEdfParams)
        return expModelSection.build()