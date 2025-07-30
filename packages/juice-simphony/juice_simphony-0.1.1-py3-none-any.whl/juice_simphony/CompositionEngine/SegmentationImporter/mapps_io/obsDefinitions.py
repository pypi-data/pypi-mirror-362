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
from mapps_io import common
from mapps_io.common.fileHandleEps import fileHandleEps

class obsDefinitions(fileHandleEps):

    def __init__(self, path, observation_definitions, params = 0):
        self.params = {}
        if params!=0: 
            self.params.update(params)
        self.path = path
        self.observation_definitions = observation_definitions

    def insertObservationDef(self, observation, insertComment=False):
        if insertComment:
            comment = "Observation Definition for " + observation["name"]
            self.fileHdl.write("# " + comment + "\n")
        self.fileHdl.write("ObservationName: {}\n".format(observation["mnemonic"]))
        self.fileHdl.write("Experiment:      {}\n".format(observation["payload"]))
        
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
            for profEntry in observation["data_profile"]:
                ref = ""
                if   (profEntry["event"] == "START"): ref = ""
                elif (profEntry["event"] == "END"):   ref = "END"
                self.fileHdl.write("        {:^3s} {} {:.2f} {}".format(ref, profEntry["time"], profEntry["data_rate"], "[bits/sec]"))
                if profEntry == observation["data_profile"][-1]: self.fileHdl.write("\n")  
                else: self.fileHdl.write(" \\ \n")

        if "power_profile" in observation:
            self.insertEmptyLine()
            self.fileHdl.write("PowerEnvelope: \\\n")
            for profEntry in observation["power_profile"]:
                ref = ""
                if   (profEntry["event"] == "START"): ref = ""
                elif (profEntry["event"] == "END"):   ref = "END"
                self.fileHdl.write("        {:^3s} {} {:.2f} {}".format(ref, profEntry["time"], float(profEntry["power"]), "[w]"))
                if profEntry == observation["power_profile"][-1]: self.fileHdl.write("\n")  
                else: self.fileHdl.write(" \\ \n")

    def writeObsDefHeader(self, title, shortDesc, description=""):
        # Insert definition file type
        self.writeHeader(title, shortDesc, description)
        self.insertEmptyLine()
        self.fileHdl.write("FileType: OBSERVATION\n")

    def writeContent(self):
        self.writeObsDefHeader("SEGMENTS", "SEGMENT DEFINITIONS")
        self.insertEmptyLine()
        for defItem in self.observation_definitions:
            self.insertObservationDef(self.observation_definitions[defItem])
            self.insertEmptyLine()