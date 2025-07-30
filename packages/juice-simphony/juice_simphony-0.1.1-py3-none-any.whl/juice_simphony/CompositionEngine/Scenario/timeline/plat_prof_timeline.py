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

from juice_simphony.CompositionEngine.Scenario.common.fileHandleTml import fileHandleTml


class plat_prof_timeline(fileHandleTml):
     
    def __init__(self, path, exp_name, params = 0):
        self.params = {}
        if params!=0: 
            self.params.update(params)
        self.path = path
        self.rootPath = path
        self.exp_name = exp_name
        self.params["prefix"]  = "ITL"
        self.params["type"]    = self.exp_name
        self.params["desc"]    = "POWER"
        self.params["version"] = "SXXPYY"
        self.params["ext"]     = "itl"
        self.fileName = ""
        self.template = 0
        self.writeVersion    = False
        self.writeTimeWindow = False
        fileHandleTml.__init__(self,path)


    def writeTimelineHeader(self, writeVersion, writeTimeWindow):
        self.writeHeader(self.params["scenarioID"], "JUICE PLATFORM POWER SCENARIO TIMELINE")
        self.insertEmptyLine()

        if writeVersion == True:
            self.insertVersion()
            self.insertEmptyLine()

        if writeTimeWindow == True:
            self.insertTimeWindow(self.params["timeline"]["startTime"], self.params["timeline"]["endTime"])

    def writeContent(self):
        self.writeTimelineHeader(self.writeVersion, self.writeTimeWindow)
        self.insertComment("")
        self.insertComment("Spacecrat platform initialization")
        self.insertComment("------------------------------------")
        self.insertInitPM ("BATTERY_DOD", 11, 0.0, 4, "Battery DoD")
        self.insertInitMS (self.exp_name, 6, "DST_X_R",  9, "NOM", 4, "Antena Receiver always ON")
        self.insertInitMS (self.exp_name, 6, "PLATFORM", 9, "ON",  4, "Platform ON to enable platform power consumption")
        self.insertEmptyLine()
        self.insertComment("")
        self.insertComment("Set platform profile")
        self.insertComment("----------------------")
        self.insertEmptyLine()
        self.insertEmptyLine()
        for power_entry in self.params["power_profile"]:
            self.insertComment("Profile entry")
            self.insertRequestEntry(power_entry["abs_time"], self.exp_name, " * ", "SET_POWER", "VALUE", power_entry["value"], power_entry["desc"])
            self.insertEmptyLine()