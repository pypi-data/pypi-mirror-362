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
from common.fileHandleEps1 import fileHandleEps1
from common.fileName import fileName
from commons.name2acronym import name2acronym


class timelineFile(fileHandleEps1):
     
    def __init__(self, path, exp_name, parameters = 0):
        self.parameters = {}
        if parameters!=0: 
            self.parameters.update(parameters)
        self.path = path
        self.rootPath = path
        self.parameters["prefix"]  = "ITL"
        self.parameters["type"]    = name2acronym(exp_name)
        self.parameters["desc"]    = ""
        self.parameters["version"] = "SXXPYY"
        self.parameters["ext"]     = "itl"
        self.fileName = ""
        self.template = 0
        self.includes = includes
        self.writeVersion    = False
        self.writeTimeWindow = False
        fileName.__init__(self, self.parameters)   


    def writeTimelineHeader(self, writeVersion, writeTimeWindow):
        self.writeHeader(self.parameters["scenarioID"], "JUICE " + exp_name + " SCENARIO TIMELINE")
        self.insertEmptyLine()

        if writeVersion == True:
            self.insertVersion()
            self.insertEmptyLine()

        if writeTimeWindow == True:
            self.insertTimeWindow(self.parameters["timeline"]["startTime"], self.parameters["timeline"]["endTime"])

    def writeContent(self):
        self.writeTimelineHeader(self.writeVersion, self.writeTimeWindow)
