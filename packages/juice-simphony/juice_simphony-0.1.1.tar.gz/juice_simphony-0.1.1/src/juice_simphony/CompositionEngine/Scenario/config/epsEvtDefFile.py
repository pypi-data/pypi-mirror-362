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
from jinja2 import Template
from juice_simphony.CompositionEngine.Scenario.common.fileTemplate import fileTemplate
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName

#class epsEvtDefFile(fileTemplate, fileName):

#    def __init__(self, path, params=0):
#        self.path = path
#        self.params = params
#        self.params["prefix"]  = "EVD"
#        self.params["type"]    = "EPS"
#        self.params["desc"]    = ""
#        self.params["version"] = ""
#        self.params["ext"]     = "def"
#        self.fileName = ""
#        self.template = 0
#        fileName.__init__(self, params)


class epsEvtDefFile(fileTemplate, fileName):
    def __init__(self, path, params=0):
        self.path = path
        self.params = params

        # Only set defaults if they aren't already provided
        self.params.setdefault("prefix", "EVD")
        self.params.setdefault("type", "EPS")
        self.params.setdefault("desc", "")
        self.params.setdefault("version", "")
        self.params.setdefault("ext", "def")

        self.fileName = ""
        self.template = 0
        fileName.__init__(self, self.params)
