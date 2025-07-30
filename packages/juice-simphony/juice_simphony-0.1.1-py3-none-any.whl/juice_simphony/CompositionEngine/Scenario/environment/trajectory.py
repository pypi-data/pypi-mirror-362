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
from datetime import datetime
from ctypes import *
import os
from pathlib import Path
import sys
import juice_simphony.spice_interface.spice_interface as spice_if
from importlib import resources

base_package = (__package__ or "").split(".")[0]
traj_path = resources.files(base_package) / "libs"

class celestialBodies_s(Structure):
    _fields_ = [("writeCallisto",       c_short),
                ("callistoFilePath",    c_char_p),
                ("writeEuropa",         c_short),
                ("europaFilePath",      c_char_p),
                ("writeGanymede"   ,    c_short),
                ("ganymedeFilePath",    c_char_p),
                ("writeJuice"   ,       c_short),
                ("juiceFilePath",       c_char_p),
                ("writeJuiceOrbDef",    c_short),
                ("juiceOrbDefFilePath", c_char_p)]

class trajectory():

    def __init__(self, path, parameters=0):
        self.parameters = parameters
        self.path = path

        spice_info = self.parameters["spice_if"]
        kernels = spice_info.kernels_list

        os.makedirs(self.parameters["spice_info"]["spice_tmp_abs_path"], exist_ok=True)
        self.parameters["spice_tmp_meta_Kernel"] = os.path.normpath(os.path.join(self.parameters["spice_info"]["spice_tmp_abs_path"], kernels.metakernel))
        meta_kernel_file = spice_if.meta_kernel(kernels, self.parameters["spice_info"]["spice_kernels_abs_path"])
        meta_kernel_file.to_file(self.parameters["spice_tmp_meta_Kernel"])

        self.trajectoryFileName       = ""
        self.periodDefinitionFileName = ""
        self.groundStationFileName    = ""
        self.callistoTrjFileName      = ""
        self.ganymedeTrjFileName      = ""
        self.europaTrjFileName        = ""
        self.structure = dict()

    def build(self):
        self.genFiles()
        return self.structure

    # Base File Name Generator
    # ------------------------
    def genBaseFileName(self, parameters):
        # General scenario file name structure
        # {prefix}_{scenarioID}_{type}_{desc}_{startDate}_{endDate}_{version}
        type = ""
        desc = ""
        version = ""
        startDate = ""
        endDate = ""
        if parameters["type"] != "":      type = "_" + parameters["type"].upper()
        if parameters["desc"] != "":      desc = "_" + parameters["desc"]
        if parameters["startDate"] != "": startDate = "_" + parameters["startDate"]
        if parameters["endDate"] != "":   endDate = "_" + parameters["endDate"]
        if parameters["version"] != 0:    version = "_V{}".format(parameters["version"])
        return "{}_{}{}{}{}{}{}.{}".format(parameters["prefix"],
                                    self.parameters["scenarioID"],
                                    type,
                                    desc,
                                    startDate,
                                    endDate,
                                    version,
                                    parameters["ext"])

    def generateFileName(self):
        # TRJ_SJS0003C30A_320110_320112_V01.asc
        parameters = dict()
        parameters["prefix"]    = "TRJ"
        parameters["type"]      = ""
        parameters["desc"]      = ""
        parameters["startDate"] = self.parameters["startDate"]
        parameters["endDate"]   = self.parameters["endDate"]
        parameters["version"]   = 1
        parameters["ext"]       = "asc"
        self.trajectoryFileName = self.genBaseFileName(parameters)
        
        # PDF_SJS0003C30A_320110_320112_V01.orb
        parameters["prefix"]    = "PDF"
        parameters["type"]      = ""
        parameters["desc"]      = ""
        parameters["startDate"] = self.parameters["startDate"]
        parameters["endDate"]   = self.parameters["endDate"]
        parameters["version"]   = 1
        parameters["ext"]       = "asc"
        self.periodDefinitionFileName = self.genBaseFileName(parameters)

        # GSV_SJS0003C30A_330216_330626_V01.asc
        parameters["prefix"]       = "GSV"
        parameters["type"]         = ""
        parameters["desc"]         = ""
        parameters["startDate"]    = self.parameters["startDate"]
        parameters["endDate"]      = self.parameters["endDate"]
        parameters["version"]      = 1
        parameters["ext"]          = "asc"
        self.groundStationFileName = self.genBaseFileName(parameters)

        # TRJ_SJS0003C30A_CAL_330216_330626_V01.asc
        parameters["prefix"]    = "TRJ"
        parameters["type"]      = "CAL"
        parameters["desc"]      = ""
        parameters["startDate"] = self.parameters["startDate"]
        parameters["endDate"]   = self.parameters["endDate"]
        parameters["version"]   = 1
        parameters["ext"]       = "asc"
        self.callistoTrjFileName = self.genBaseFileName(parameters)

        # TRJ_SJS0003C30A_GAN_330216_330626_V01.asc
        parameters["prefix"]    = "TRJ"
        parameters["type"]      = "GAN"
        parameters["desc"]      = ""
        parameters["startDate"] = self.parameters["startDate"]
        parameters["endDate"]   = self.parameters["endDate"]
        parameters["version"]   = 1
        parameters["ext"]       = "asc"
        self.ganymedeTrjFileName = self.genBaseFileName(parameters)

        # TRJ_SJS0003C30A_EUR_330216_330626_V01.asc
        parameters["prefix"]    = "TRJ"
        parameters["type"]      = "EUR"
        parameters["desc"]      = ""
        parameters["startDate"] = self.parameters["startDate"]
        parameters["endDate"]   = self.parameters["endDate"]
        parameters["version"]   = 1
        parameters["ext"]       = "asc"
        self.europaTrjFileName = self.genBaseFileName(parameters)

    def buildFilesPath(self):
        self.structure["path"] = self.path
        self.structure["trajectoryFile"]       = os.path.join(self.structure["path"], self.trajectoryFileName)
        self.structure["periodDefinitionFile"] = os.path.join(self.structure["path"], self.periodDefinitionFileName)
        self.structure["groundStationFile"]    = os.path.join(self.structure["path"], self.groundStationFileName)
        self.structure["callistoTrjFile"]      = os.path.join(self.structure["path"], self.callistoTrjFileName)
        self.structure["ganymedeTrjFile"]      = os.path.join(self.structure["path"], self.ganymedeTrjFileName)
        self.structure["europaTrjFile"]        = os.path.join(self.structure["path"], self.europaTrjFileName)

    def genFiles(self):
        self.generateFileName()
        self.buildFilesPath()


        try:
            #trajEngine = CDLL(self.parameters["scenario_generator"]["trj_engine_lib_abs_path"])
            #trajEngine = CDLL(os.path.join(config_file_path, "../libs", "libTrajectoryEngine.dylib"))
            traj_lib = traj_path / "libTrajectoryEngine.dylib"
            trajEngine = CDLL(traj_lib)
            print("Successfully loaded ", trajEngine)
        except Exception as e:
            print(e)
        startTime = c_char_p(bytes(self.parameters["startTime"], 'utf-8'))
        endTime   = c_char_p(bytes(self.parameters["endTime"], 'utf-8'))
        spiceKernels = c_char_p(bytes(self.parameters["spice_tmp_meta_Kernel"], 'utf-8'))
        
        cB = celestialBodies_s()
        cB.writeCallisto       = c_short(1)
        cB.callistoFilePath    = c_char_p(bytes(self.structure["callistoTrjFile"], 'utf-8'))
        cB.writeEuropa         = c_short(1)
        cB.europaFilePath      = c_char_p(bytes(self.structure["europaTrjFile"], 'utf-8'))
        cB.writeGanymede       = c_short(1)
        cB.ganymedeFilePath    = c_char_p(bytes(self.structure["ganymedeTrjFile"], 'utf-8'))
        cB.writeJuice          = c_short(1)
        cB.juiceFilePath       = c_char_p(bytes(self.structure["trajectoryFile"], 'utf-8'))
        cB.writeJuiceOrbDef    = c_short(1)
        cB.juiceOrbDefFilePath = c_char_p(bytes(self.structure["periodDefinitionFile"], 'utf-8'))
        genMappsOrbitFiles = trajEngine.genMappsOrbitFiles
        genMappsOrbitFiles(startTime, endTime, spiceKernels, cB);

        # Create the temporaty Ground Station Visibility
        f = open(self.structure["groundStationFile"], "a")
        f.write("# Note that Julian dates count from 12:00:00 noon, 1 January 2000\n")
        f.write("#\n")
        f.write("# GS Start time    End time\n")
        f.write("#      UTC (JD)    UTC (JD)\n")
        f.write("#\n")
        f.write("FILE_TYPE = GS_VIS_PERIODS\n")
        f.write("TIME_SCALE = JD\n")
        f.write("#\n")
        f.write("# File Empty not used for the time being\n")
        f.close()

        handle = trajEngine._handle
        if sys.platform.startswith('win'):
            windll.kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
            windll.kernel32.FreeLibrary(handle)
        else:
             dll_close = trajEngine.dlclose
        del (trajEngine)
        return self.structure