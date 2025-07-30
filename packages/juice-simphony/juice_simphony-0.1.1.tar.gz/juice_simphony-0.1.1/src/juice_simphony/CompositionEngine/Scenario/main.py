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
from scenario import scenario
import argparse
import json
from pathlib import Path
from graphicalPath import graphicalPath
import os

def searchFile(search_path, filename):
    result = []
    for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
    return result

if __name__ == '__main__':
    search_path = R'Z:\VALIDATION\simphony\pcm\phs_pcm_test_001\segmentation_exporter\tmp'
    filename = "config_segmentation.json"

    print (searchFile(search_path,filename))
    #return result
    #print (os.listdir(directory))
    #print ([name for name in os.listdir(directory) if os.path.isdir(name)]) 
    
    """
    seg_importer_cfg = {}

    # session_cfg
    # -----------
    seg_importer_cfg.update(sessionConfiguration={})
    session_cfg = seg_importer_cfg["sessionConfiguration"]
    session_cfg["sessionID"] = "eps_package"
    session_cfg["version"]   = "1.0.0"

    # simulation_cfg
    session_cfg.update(simulationConfiguration={})
    simulation_cfg = session_cfg["simulationConfiguration"]
    simulation_cfg["timeStep"]       = 1
    simulation_cfg["outputTimeStep"] = 1

    #att_sim_cfg
    session_cfg.update(atttitudeSimulationConfiguration={})
    att_sim_cfg = session_cfg["atttitudeSimulationConfiguration"]
    att_sim_cfg["kernelsList"]         = {}
    att_sim_cfg["baselineRelPath"]     = "" #self.structure["configuration"]["agmCfg"]["path"] # rel path
    att_sim_cfg["ageConfigFileName"]   = "."
    att_sim_cfg["userDefinitionFile"]  = ""
    att_sim_cfg["predefinedBlockFile"] = ""

    #inst_sim_cfg
    session_cfg.update(instumentSimulationConfiguration={})
    inst_sim_cfg = session_cfg["instumentSimulationConfiguration"]
    inst_sim_cfg["baselineRelPath"]     = ""#self.structure["configuration"]["agmCfg"]["path"] # rel path
    inst_sim_cfg["unitFileName"]   = "."
    inst_sim_cfg["configFileName"]  = ""
    inst_sim_cfg["edfFileName"] = ""
    inst_sim_cfg["eventDefFileName"] = ""
    inst_sim_cfg["observationDefFileName"] = ""

    #input_files_cfg
    session_cfg.update(inputFiles={})
    input_files_cfg = session_cfg["inputFiles"]
    input_files_cfg["baselineRelPath"]         = ""
    input_files_cfg["jsonSegmentFilePath"]     = ""
    input_files_cfg["xmlPtrPath"]              = ""
    input_files_cfg["segmentTimelineFilePath"] = ""
    input_files_cfg["eventTimelineFilePath"]   = ""
    
    #output_files_cfg
    session_cfg.update(outputFiles={})
    output_files_cfg = session_cfg["outputFiles"]
    output_files_cfg["baselineRelPath"]      = ""
    output_files_cfg["baselineRelPath"]      = ""
    output_files_cfg["simOutputFilesPath"]   = ""
    output_files_cfg["ckAttitudeFilePath"]   = ""
    output_files_cfg["simDataFilePath"]      = ""
    output_files_cfg["attitudeXmlPtr"]       = ""
    output_files_cfg["runtimeErrorFilePath"] = ""
    output_files_cfg["runtimeLogFilePath"]   = ""

    with open(R'Z:\VALIDATION\simphony\pcm\phs_pcm_test_001\segmentation_importer\timelines\output.json', 'w') as outfile:
        json.dump(seg_importer_cfg, outfile, indent=4)


   
    parser = argparse.ArgumentParser(prog="simphony")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-f', '--force', dest='force', action='store_true')
    parser.add_argument('-c', '--config',
                        required=True, action="store", type=str, dest="cfgFile",
                        help="Read configuration file from FILEPATH", metavar="FILEPATH")
    parser.add_argument("-d", "--dest",
                        required=True, action="store", type=str, dest="destPath",
                        help="Install the scenario in PATH", metavar="PATH")
    parser.set_defaults(force=False)

    # Load Scenario Generation configuration file with fix parameters
    # ---------------------------------------------------------------
    sceParams = dict()
    configPath = R"Z:\Resources\Juice\Test\Simphony\config-test.json"
    #configPath = R"Z:\Resources\Juice\Test\Simphony\config-rel.json"
    
    # Load scenario generation configuration file
    with open(configPath) as json_file:
       sceParams = json.load(json_file)
    

    sceParams["labelPrefix"]     = "SJ"
    sceParams["type"]            = "ENGINEERING"
    sceParams["code"]            = 1
    sceParams["version"]         = 1
    sceParams["cremaVersion"]    = "5.0"
    sceParams["shortDesc"]       = "21C13 CALLISTO FB"
    sceParams["startTime"]       = "2032-07-01T16:22:24"
    sceParams["endTime"]         = "2032-07-03T16:22:24"
    sceParams["iniAbsolutePath"] = "SOFTWARE/MAPPS"
    sceParams["segmentID"]       = 51

    scen = scenario(sceParams["scenarioAbsPathArea"], sceParams, True)
    scenarioPath = scen.buildScenario()
    """
