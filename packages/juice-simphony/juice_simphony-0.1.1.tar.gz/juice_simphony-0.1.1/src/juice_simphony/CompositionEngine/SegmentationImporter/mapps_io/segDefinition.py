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
#from mapps_io.common.fileHandleEps import fileHandleEps

from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io import common
from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io.common.fileHandleEps import fileHandleEps

class segDefinition(fileHandleEps):
     
    def __init__(self, path, segment_definitions, params = 0):
        self.params = {}
        if params!=0: 
            self.params.update(params)
        self.path = path
        self.segment_definitions = segment_definitions
        fileHandleEps.__init__(self)

    def insertSegmentDef(self, instrument, segment):
        comment = "Segment Definition for " + segment["name"]
        self.fileHdl.write("# " + comment + "\n")
        self.fileHdl.write("ObservationName: {}\n".format(segment["name"]))
        self.fileHdl.write("Experiment:      {}\n".format(instrument))

        # Write parameters definition if exists
        cnt = 1
        total = len(segment["instTargetMapList"])
        for instTargetMap in segment["instTargetMapList"]:
            if instTargetMap["target"] == "":
                target = "NONE"
            if cnt == 1:
                self.fileHdl.write(    "Parameters: {:<8} = {} \\\n".format(instTargetMap["instName"],target))
            else:
                if cnt != total:
                    self.fileHdl.write("            {:<8} = {} \\\n".format(instTargetMap["instName"],target))
                else:
                    self.fileHdl.write("            {:<8} = {}\n".format(instTargetMap["instName"],target))
            cnt = cnt + 1
        
        # Write segment definition parent if exist
        if "observation_definitions" in segment:
            self.insertEmptyLine()
            self.fileHdl.write("# CHILD_OBSERVATIONS: \n")
            self.fileHdl.write("# ------------------- \n")
            for obsDef in segment["observation_definitions"]:
                self.fileHdl.write("# " + obsDef + "\n")
            self.fileHdl.write("# ------------------- \n")

        # Write segment definition parent if exist
        #if "observation_definitions" in segment:
        #    self.insertEmptyLine()
        #    self.fileHdl.write("# CHILD_OBSERVATIONS:")
        #    for obsDef in segment["observation_definitions"]:
        #        self.fileHdl.write(" [" + obsDef + "]")

    def writeSegDefHeader(self):
        # Insert definition file type
        self.writeHeader("SEGMENTS", "SEGMENT DEFINITIONS")
        self.insertEmptyLine()
        self.fileHdl.write("FileType: OBSERVATION\n")

    def writeContent(self):
        self.writeSegDefHeader()
        for defItem in self.segment_definitions:
            definition = {}
            definition["name"]       = self.segment_definitions[defItem]["name"]
            definition["instrument"] = "SCI_SEGMENT"
            self.insertEmptyLine()
            self.insertEmptyLine()
            self.insertSegmentDef("SCI_SEGMENT", self.segment_definitions[defItem])


