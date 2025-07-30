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
import textwrap

from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io import common
from juice_simphony.CompositionEngine.SegmentationImporter.mapps_io.common.fileHandleEps import fileHandleEps


class obsDefinition(fileHandleEps):

    def __init__(self, path, observation_definition, params = 0):
        self.params = {}
        if params!=0:
            self.params.update(params)
        self.path = path
        self.observation_definition = observation_definition
        fileHandleEps.__init__(self)

    # Insert observation Definition
    def insertObservationDef(self, observation, insertComment=False):
        if insertComment:
            comment = "Observation Definition for " + observation["mnemonic"]
            self.fileHdl.write("# " + comment + "\n")
        self.fileHdl.write("ObservationName: {}\n".format(observation["mnemonic"].replace(" ", "").upper()))
        self.fileHdl.write("Experiment:      {}\n".format(observation["payload"]))

        # Write segment definition parent if exist
        if "segment_definitions" in observation:
            self.insertEmptyLine()
            self.fileHdl.write("# PARENT_SEGMENTS: \n")
            self.fileHdl.write("# ---------------- \n")
            for segDef in observation["segment_definitions"]:
                self.fileHdl.write("# " + segDef + "\n")
            self.fileHdl.write("# ---------------- \n")

        # --------
        # PROFILES
        # --------
        if ("data_profile" in observation) or ("data_profile" in observation):
            self.insertEmptyLine()
            self.fileHdl.write("# Observation Profile Envelope \n")
            self.fileHdl.write("# ---------------------------- \n")

        if "data_profile" in observation:
            self.insertEmptyLine()
            self.fileHdl.write("DataRateEnvelope: \\\n")
            #dataProfile = sorted(observation["data_profile"]["time"])
            for profEntry in observation["data_profile"]:
                ref = ""
                if   (profEntry["event"] == "Start"): ref = ""
                elif (profEntry["event"] == "End"):   ref = "END"
                if profEntry["data_rate"] is None: 
                    self.fileHdl.write("        {:^3s} {} {:.2f} {}".format(ref, profEntry["time"], 0.0, "[bits/sec]"))
                else:
                    self.fileHdl.write("        {:^3s} {} {:.2f} {}".format(ref, profEntry["time"], profEntry["data_rate"], "[bits/sec]"))

                if profEntry == observation["data_profile"][-1]: self.fileHdl.write("\n")  
                else: self.fileHdl.write(" \\ \n")

        if "power_profile" in observation:
            self.insertEmptyLine()
            self.fileHdl.write("PowerEnvelope: \\\n")
            for profEntry in observation["power_profile"]:
                ref = ""
                if   (profEntry["event"] == "Start"): ref = ""
                elif (profEntry["event"] == "End"):   ref = "END"
                if profEntry["power"] is None: 
                    self.fileHdl.write("        {:^3s} {} {:.2f} {}".format(ref, profEntry["time"], 0.0, "[w]"))
                else:
                    self.fileHdl.write("        {:^3s} {} {:.2f} {}".format(ref, profEntry["time"], float(profEntry["power"]), "[w]"))

                if profEntry == observation["power_profile"][-1]: self.fileHdl.write("\n")  
                else: self.fileHdl.write(" \\ \n")

    def writeObsDefHeader(self, title, shortDesc, description=""):
        # Insert definition file type
        self.writeHeader(title, shortDesc, description)
        self.insertEmptyLine()
        self.fileHdl.write("FileType: OBSERVATION\n")

    def writeContent(self):
        self.writeObsDefHeader(self.params["scenarioID"] + " OBSERVATION DEFINITION", self.observation_definition["payload"] + " OBSERVATION " + self.observation_definition["name"])
        self.insertEmptyLine()
        self.insertObservationDef(self.observation_definition)
        self.insertEmptyLine()