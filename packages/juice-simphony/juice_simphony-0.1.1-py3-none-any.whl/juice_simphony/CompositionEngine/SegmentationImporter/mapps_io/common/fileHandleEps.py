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
#from mapps_io.common.fileHandle import fileHandle

from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io.common.fileHandle import fileHandle


class fileHandleEps(fileHandle):
    def __init__(self):
        fileHandle.__init__(self,self.path)

    def insertVersion (self, version = 1):
        self.fileHdl.write("# Timeline version" + "\n")
        self.fileHdl.write("Version: 1" + "\n")

    def insertTimeWindow (self, startTime, endTime):
        self.fileHdl.write("# Time Window" + "\n")
        self.fileHdl.write("Start_time: " + startTime + "\n")
        self.fileHdl.write("End_time:   " + endTime   + "\n")

      ## Timeline file for JUICE
      #  Version: 1
      #  
      ## Time Window
      ## (mandatory at top level)
      #Start_time: 2032-01-09T16:44:04Z
      #End_time:   2032-01-13T18:44:04Z

    def insertInclude(self,params):
        fileNameRel = os.path.relpath(params["filePath"], self.rootPath).replace("\\","/")
        if "fileDescription" in params:
            self.fileHdl.write("# " + params["fileDescription"] + "\n")
        if "commented" in params:
            if (params["commented"]):
                self.fileHdl.write("# ")
        self.fileHdl.write("Include: " + fileNameRel)
        
    def insertIncludeFile(self,params):
        fileNameRel = os.path.relpath(params["filePath"], self.rootPath).replace("\\","/")
        if "fileDescription" in params:
            self.fileHdl.write("# " + params["fileDescription"] + "\n")
        if "commented" in params:
            if (params["commented"]):
                self.fileHdl.write("# ")
        self.fileHdl.write("Include_file: " + "\"" + fileNameRel + "\"" + "\n")
        