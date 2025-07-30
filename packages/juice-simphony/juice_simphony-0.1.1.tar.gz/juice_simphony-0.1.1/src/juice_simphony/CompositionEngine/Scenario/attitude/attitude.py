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
import juice_simphony.CompositionEngine.Scenario.common.utils as utils
from juice_simphony.CompositionEngine.Scenario.definitions.toplevelObsDef import toplevelObsDef
from juice_simphony.CompositionEngine.SegmentationImporter.SegmentationImporter import segmentationTimeline
from juice_simphony.CompositionEngine.Scenario.attitude import xml_attitude as xml_att


import os

class attitude:

    def __init__(self, segmentationTimelineInst, root_path, parameters=0):
        self.root_path = root_path
        self.segTimeline = segmentationTimelineInst
        self.parameters = parameters
        self.mainFolderPath = ""
        self.structure = {}

    def build(self):
        self.createMainFolder('POINTING')
        self.structure["path"]            = self.mainFolderPath;
        self.structure["xmlAttitudeFile"] = self.addRootContent()
        return self.structure

    def createMainFolder(self, folderName):
        self.mainFolderPath = utils.createFolder(self.root_path, folderName)

    def addRootContent(self):
        xml_seg_attitude = self.segTimeline.getXmlAttitude()
        if xml_seg_attitude["valid"]:
          xml_att_file = xml_att.xml_attitude(self.mainFolderPath, xml_seg_attitude["xml_tree"], self.parameters)
          return xml_att_file.genFile()
        return ""