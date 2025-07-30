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
#from datetime import datetime

#from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io import common
from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io.common.fileHandleEps import fileHandleEps
from datetime import datetime

class timeline(fileHandleEps):
     
    def __init__(self, path, segments_timeline, params = 0):
        self.params = {}
        if params!=0: 
            self.params.update(params)
        self.path = path
        self.segments_timeline = segments_timeline
        self.writeVersion    = True
        self.writeTimeWindow = True
        fileHandleEps.__init__(self)

    def insertObservation(self,obs):
        comment = "Observation " + obs["name"]
        self.fileHdl.write("# " + comment)
        self.fileHdl.write("{} {} {} {}\n".format(datetime.strptime(obs["startDatetime"],"%Y-%m-%dT%H:%M:%SZ"), obs["instrument"], "OBS_START", obs["name"]))
        self.fileHdl.write("{} {} {} {}\n".format(datetime.strptime(obs["endDatetime"],"%Y-%m-%dT%H:%M:%SZ"),   obs["instrument"], "OBS_END",   obs["name"]))

    def insertSegment(self,segment):
        comment = "Segment " + segment["segment_definition"]
        #print(comment)
        self.fileHdl.write("# " + comment + "\n")

        # Write segment start entry
        # -------------------------
        entryLine = "{} {} {} {}".format(datetime.strftime(segment["startDatetime"],"%Y-%m-%dT%H:%M:%SZ"), "SCI_SEGMENT", "OBS_START", segment["segment_definition"])
        self.fileHdl.write(entryLine)
        entryLineLen = len(entryLine)

        # Write parameters definition if exists
        cnt = 0
        total = len(segment["instTypeMap"])
        for instTargetMap in segment["instTypeMap"]:
            instTarget = segment["instTypeMap"][instTargetMap]
            cnt = cnt + 1
            if segment["instTypeMap"][instTargetMap] == "":
                instTarget = "NONE"
            if cnt == 1:
                self.fileHdl.write(" ( {:<8} = {} \\\n".format(instTargetMap, instTarget))
            else:
                if cnt != total:
                    self.fileHdl.write("{:{}}{:<8} = {} \\\n".format("", entryLineLen+3, instTargetMap, instTarget))
                else:
                    self.fileHdl.write("{:{}}{:<8} = {} )\n".format("", entryLineLen+3, instTargetMap, instTarget))
        if cnt == 0 :  
            self.fileHdl.write("\n")
        
        # Write segment end entry
        # -----------------------
        self.fileHdl.write("{} {} {} {}\n".format(datetime.strftime(segment["endDatetime"],"%Y-%m-%dT%H:%M:%SZ"),   "SCI_SEGMENT", "OBS_END",   segment["segment_definition"]))        
        
        #"segment_definition"

        #"overwritten"
        #"instrument_overwritten"
        #"timeline"

        # STARE AT LIMB 40N, RIDE ALONG TO MAJIS
        # 2032-01-11T12:31:40Z JANUS OBS_START LIMB_STARE_40N_001 (PRIME=TRUE \
        #  DATA_RATE_PROFILE = 00:00:00  59.1 [kbits/sec])
        # 2032-01-11T12:56:00Z JANUS OBS_END LIMB_STARE_40N_001

    def writeTimelineHeader(self, writeVersion, writeTimeWindow):
        self.writeHeader(self.params["scenarioID"], "SEGMENTATION TIMELINE")
        self.insertEmptyLine()

        if writeVersion == True:
            self.insertVersion()
            self.insertEmptyLine()

        if writeTimeWindow == True:
            self.insertTimeWindow(self.params["timelineStartTime"], self.params["timelineEndTime"])

    def writeContent(self):
        self.writeTimelineHeader(self.writeVersion, self.writeTimeWindow)
        self.segments_timeline.sort(key=self.get_timeline_entry_start)
        for segment in self.segments_timeline:
            self.insertEmptyLine()
            self.insertSegment(segment)

    def get_timeline_entry_start(self, entry):
        return entry["start"]