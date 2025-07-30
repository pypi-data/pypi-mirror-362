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
from juice_simphony.CompositionEngine.Scenario.common.fileHandle import fileHandle
from juice_simphony.CompositionEngine.Scenario.common.fileHandleEps import fileHandleEps
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName


class toplevelExpEdf(fileHandleEps):

    def __init__(self, path, instName, parameters=0):
        self.path = path
        self.parentPath = parameters["edfRootPath"]
        self.parameters = parameters
        self.instName   = instName
        self.parameters["prefix"]        = "EDF"
        self.parameters["type"]          = "JUI"
        self.parameters["addScenarioID"] = False
        self.parameters["desc"]          = instName
        self.parameters["version"]       = 0
        self.parameters["ext"]           = "edf"
        self.fileName = ""
        fileName.__init__(self, parameters)

    def writeContent(self):

        # -------
        # HEADER
        # -------

        title       = "JUICE-{}".format(self.instName)
        shortDesc   = "SCIENCE OPERATIONS SIMULATOR MODEL"
        desc        = "# This file includes all the files providing the parameters needed to configure the simulator\n"\
                      "# used by the science operations team to simulate the behaviour and the performance\n"\
                      "# of the {} instrument.".format(self.instName)
        self.writeHeader(title, shortDesc, desc)

        # -------
        # CONTENT
        # -------

        includeFiles = [
            {"fileDescription":"Mode definitions file",
             "fileName":R"Z:\Dev\Projects\Juice\juiceops\ScenarioGeneration\PLANNING\SJE0001_TEST\SJE0001C30A_TEST_300105_300105\MODELLING\3GM\EDF_JUI_3GM_MODES.edf"},
            {"fileDescription":"Field of View definitions file",
             "fileName":R"Z:\Dev\Projects\Juice\juiceops\ScenarioGeneration\PLANNING\SJE0001_TEST\SJE0001C30A_TEST_300105_300105\MODELLING\3GM\EDF_JUI_3GM_FOV.edf"}
            ]

        for includeFile in includeFiles:
            self.insertEmptyLine()
            self.insertInclude(includeFile)