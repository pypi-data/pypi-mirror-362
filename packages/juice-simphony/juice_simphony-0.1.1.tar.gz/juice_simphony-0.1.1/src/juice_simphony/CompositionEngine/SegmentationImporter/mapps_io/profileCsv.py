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
#from mapps_io import common
#from mapps_io.common.fileHandle import fileHandle
from datetime import datetime
#import segmentation_profiles as seg_profile

from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io import common
from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io.common.fileHandle import fileHandle
#from juice_simphony.CompositionEngine.SegmentationImporter.segmentation_profiles import segmentation_profiles as seg_profile


class profileCsv(fileHandle):
     
    def __init__(self, path, profile, params = 0):
        self.params = {}
        if params!=0:
            self.params.update(params)
        self.path = path
        self.profile = profile
        self.writeVersion    = True
        self.writeTimeWindow = True
        
        fileHandle.__init__(self,path)

    def insertProfileEntry(self,profileEntry):
       entry_time = datetime.strftime(profileEntry.time,"%Y-%m-%dT%H:%M:%SZ")
       if   self.params["profile_value_type"][0] == "rate":
          entry_value = profileEntry.instant.value
       elif self.params["profile_value_type"][0] == "volume": 
          entry_value = profileEntry.volume.value
       elif self.params["profile_value_type"][0] == "acc":
          entry_value = profileEntry.accumulated.value
       self.fileHdl.write("{} {}\n".format(entry_time, entry_value))

    def writePrfileHeader(self):
        self.writeHeader(self.params["scenarioID"], "SEGMENTATION RESOURCE FILE")
        self.insertEmptyLine()
        #self.fileHdl.write("{} {} {} {}\n".format(segment["end"].replace(".000", ""),   "SCI_SEGMENT", "OBS_END",   segment["segment_definition"]))
   
    def writeContent(self):
        self.writePrfileHeader()
        for profileEntry in self.profile.res_profile:
           self.insertProfileEntry(profileEntry)