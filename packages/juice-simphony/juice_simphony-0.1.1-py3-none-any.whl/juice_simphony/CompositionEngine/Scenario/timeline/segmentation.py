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
from juice_simphony.CompositionEngine.Scenario.common import utils as utils
from juice_simphony.CompositionEngine.SegmentationImporter.SegmentationImporter import segmentationTimeline
from juice_simphony.CompositionEngine.Scenario.timeline import inst_timeline as inst_timeline
from juice_simphony.CompositionEngine.Scenario.timeline.inst_top_timeline import instToplevel
from juice_simphony.CompositionEngine.Scenario.timeline.plat_prof_timeline import plat_prof_timeline

class segmentation:

    def __init__(self, segmentationTimelineInst, root_path, parameters=0):
        self.root_path = root_path
        self.params = parameters
        self.segTimeline = segmentationTimelineInst
        self.mainFolderPath = ""
        self.structure = {}
        self.elements  = {}
        #self.expTimelines = []

    def build(self):
        self.createMainFolder('SEGMENTATION')
        self.structure["path"] = self.mainFolderPath;
        if self.segTimeline.size() > 0:
            self.structure["segmentationTimeline"] = self.addSegmentationTimeline()
        self.elements = self.addOverlays()

        output = {}
        output["structure"] = self.structure
        output["elements"] = {}
        output["elements"]["overlays"] = self.elements

        #exp_list = ["3GM","GAL","JAN","MAG","JMC","MAJ","NAV","PEH","PEL","PRI","RAD","RIM","RPW","SWI","UVS"]
        #output["structure"].update(self.addTmlPlaceHolder(exp_list))

        #self.params["includeFiles"] = self.expTimelines
        #inst_top = instToplevel(self.root_path, self.mainFolderPath, self.params)
        #output["structure"]["top_level_inst"] = inst_top.genFile()

        #output["structure"]["plat_timeline"] = self.createPlatProfTimeline(self.mainFolderPath,"JUICE")
        return output

    def createMainFolder(self, folderName):
        env_path = utils.createFolder(self.root_path, "ENVIRONMENT")  # ensure ENVIRONMENT exists
        self.mainFolderPath = utils.createFolder(env_path, folderName)  # create SEGMENTATION inside it

    def addSegmentationTimeline(self):
        return self.segTimeline.generateSegmentTimeline(self.mainFolderPath, self.params["scenarioID"])

    def addOverlays(self):
        return self.segTimeline.generateProfileCsv(self.mainFolderPath, self.params["scenarioID"])

    #def addTmlPlaceHolder(self, exp_list):
    #    structure = {}
    #    for exp in exp_list:
    #        structure[exp] = {}
    #        structure[exp]["path"] = utils.createFolder(self.mainFolderPath, exp)
    #        self.expTimelines.append(self.createPlaceHolderTimeline(structure[exp]["path"],exp))
    #    return structure

    #def createPlaceHolderTimeline(self, pathFile, exp):
    #    tml = inst_timeline.timelineFile(path=pathFile, exp_name=exp, params=self.params)
    #    return tml.genFile()

    #def createPlatProfTimeline(self, pathFile, exp):
    #    self.params["power_profile"] = self.segTimeline.genPlatformPowerProfile(self.params["startTime"], self.params["endTime"])
    #    platform_timeline = plat_prof_timeline(path=pathFile, exp_name=exp, params=self.params)
    #    return platform_timeline.genFile()


if __name__ == "__main__":
    params = {}
    params["scenarioID"] = "SJS0003C30A"

    # Segmentation timeline Test
    # ----------------------------
    segTimeline = segmentationTimeline()
    params["startTime"] = "2032-05-10T08:33:51Z"
    params["endTime"]   = "2032-09-25T23:58:51Z"
    root_path = "Z:\VALIDATION\simphony\pcm\phs_pcm_test_001\scenario_generator\output"
    tml = timeline(segTimeline, root_path, params)
    tml.createPlatProfTimeline(root_path,"JUICE")