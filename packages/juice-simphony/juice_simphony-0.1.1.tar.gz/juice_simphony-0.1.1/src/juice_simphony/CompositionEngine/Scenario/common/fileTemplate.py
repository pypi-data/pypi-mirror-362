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
import configparser
from jinja2 import Template
import os

from juice_simphony.CompositionEngine.Scenario.common import utils

def relPath (path, refPath):
    return os.path.relpath(path, refPath).replace("\\","/")

class fileTemplate():

    def __init__(self, path):
        self.path = path
        self.params = dict()
        self.fileName = ""
        self.template = 0
        self.refFileLoaded = False

    def genFile(self, refFilePath):
        self.loadRefFile(refFilePath)
        self.fileName = self.genBaseFileName() + "." + self.params["ext"]
        destFilePath = os.path.join(self.path, self.fileName)
        self.writeFile(destFilePath)
        return destFilePath

    def loadRefFile(self, filePath):
        with open(filePath) as tplFile:
            self.template = Template(tplFile.read())
        self.template.globals["relPath"] = relPath

    def writeFile(self, filePath):
        self.template.stream(self.params).dump(filePath)


class fileTemp():

    def __init__(self, path):
        self.path = path
        self.params = dict()
        self.fileName = ""
        self.template = 0
        self.refFileLoaded = False

    def genFile(self, refFilePath):
        self.loadRefFile(refFilePath)
        self.fileName = self.genBaseFileNameNoV() + "." + self.params["ext"]
        destFilePath = os.path.join(self.path, self.fileName)
        self.writeFile(destFilePath)
        return destFilePath

    def loadRefFile(self, filePath):
        with open(filePath) as tplFile:
            self.template = Template(tplFile.read())
        self.template.globals["relPath"] = relPath

    def writeFile(self, filePath):
        self.template.stream(self.params).dump(filePath)