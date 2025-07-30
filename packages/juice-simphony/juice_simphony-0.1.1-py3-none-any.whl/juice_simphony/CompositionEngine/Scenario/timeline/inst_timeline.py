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

from juice_simphony.CompositionEngine.Scenario.common.fileHandleEps1 import fileHandleEps1
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName




class timelineFile(fileHandleEps1):
     
    def __init__(self, path, exp_name, params = 0):
        self.params = {}
        if params!=0: 
            self.params.update(params)
        self.path = path
        self.rootPath = path
        self.exp_name = exp_name
        self.params["prefix"]  = "ITL"
        self.params["type"]    = self.exp_name
        self.params["desc"]    = ""
        self.params["version"] = "SXXPYY"
        self.params["ext"]     = "json"
        self.fileName = ""
        self.template = 0
        self.writeVersion    = False
        self.writeTimeWindow = False
        fileName.__init__(self, self.params)


    def writeTimelineHeader(self, writeVersion, writeTimeWindow):
        self.writeHeader(self.params["scenarioID"], "JUICE " + self.exp_name + " SCENARIO TIMELINE")
        self.insertEmptyLine()

        if writeVersion == True:
            self.insertVersion()
            self.insertEmptyLine()

        if writeTimeWindow == True:
            self.insertTimeWindow(self.params["timeline"]["startTime"], self.params["timeline"]["endTime"])

    def writeContent(self):
        self.writeTimelineHeader(self.writeVersion, self.writeTimeWindow)

