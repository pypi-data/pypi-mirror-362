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
from .fileHandle import fileHandle

class fileHandleEps1(fileHandle):
    def __init__(self):
        fileHandle.__init__(self,self.path)

    def insertVersion (self, version = 1):
        self.fileHdl.write("# Timeline version" + "\n")
        self.fileHdl.write("Version: 1" + "\n")

    def insertTimeWindow (self, startTime, endTime):
        self.fileHdl.write("# Time Window" + "\n")
        self.fileHdl.write("Start_time: " + startTime + "\n")
        self.fileHdl.write("End_time:   " + endTime   + "\n")

    def insertInclude(self,params):
        fileNameRel = os.path.relpath(params["filePath"], self.rootPath).replace("\\","/")
        if "fileDescription" in params:
            self.insertEmptyLine()
            self.fileHdl.write("# " + params["fileDescription"] + "\n")
        self.fileHdl.write("Include: " + fileNameRel + "\n")
        
    def insertIncludeFile(self,params):
        fileNameRel = os.path.relpath(params["filePath"], self.rootPath).replace("\\","/")
        if "fileDescription" in params:
            self.insertEmptyLine()
            self.fileHdl.write("# " + params["fileDescription"] + "\n")
        self.fileHdl.write("Include_file: " + "\"" + fileNameRel + "\"" + "\n")
        