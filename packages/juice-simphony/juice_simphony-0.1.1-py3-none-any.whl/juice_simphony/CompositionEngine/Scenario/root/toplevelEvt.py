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

from juice_simphony.CompositionEngine.Scenario.common.fileTemplate import fileTemplate
from juice_simphony.CompositionEngine.Scenario.common.fileHandleEps1 import fileHandleEps1
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName

class toplevelEvtOld(fileTemplate, fileName):

    def __init__(self, path, params=0):
        self.path = path
        self.params = params
        self.params["prefix"] = "EVT"
        self.params["type"] = "TOP_LEVEL"
        self.params["desc"] = ""
        self.params["version"] = "V1"
        self.params["ext"] = "evf"
        self.fileName = ""
        self.template = 0
        fileName.__init__(self, params)


class toplevelEvt(fileHandleEps1):

    def __init__(self, path, includes, params=0):
        self.params = {}
        if params != 0:
            self.params.update(params)
        self.path = path
        self.rootPath = path
        self.params.setdefault("prefix", "EVT")
        self.params["type"] = "TOP_LEVEL"
        self.params["desc"] = ""
        self.params["version"] = "V1"
        self.params["ext"] = "evf"
        self.fileName = ""
        self.template = 0
        self.includes = includes
        self.writeVersion = False
        self.writeTimeWindow = True
        fileName.__init__(self, self.params)

    def writeTimelineHeader(self, writeVersion, writeTimeWindow):
        self.writeHeader(self.params["scenarioID"], "JUICE TOP LEVEL SCENARIO EVENT TIMELINE")
        self.insertEmptyLine()

        if writeVersion == True:
            self.insertVersion()
            self.insertEmptyLine()

        if writeTimeWindow == True:
            self.insertTimeWindow(self.params["timeline"]["startTime"], self.params["timeline"]["endTime"])

    def writeContent(self):
        self.writeTimelineHeader(self.writeVersion, self.writeTimeWindow)
        for include in self.includes:
            self.insertEmptyLine()
            self.insertIncludeFile(include)

