/*****************************************************************************
* This file is subject to the terms and conditions defined in the            * 
* file 'LICENSE.txt', which is part of this source code package.             *
*                                                                            *
* No part of the package, including this file, may be copied, modified,      *
* propagated, or distributed except according to the terms contained in      *
* the file 'LICENSE.txt'.                                                    *
*                                                                            *
* (C) Copyright European Space Agency, 2025                                  *
*****************************************************************************/

// *************************************************************
// *                                                           *
// *             Juice Mapps Inputs Generator                  *
// *                                                           *
// *************************************************************

// Standard includes
#include <iostream>
#include <string>
#include <fstream>
#include <iomanip>
#include <vector>

// External includes
#include "../cspice/include/SpiceUsr.h"

// Application includes
#include "../Utils/TimeUtils.hpp"
#include "OrbitDataFile.hpp"
#include "OrbitDefFile.hpp"
#include "EventsFile.hpp"
#include "TrajectoryEngine.hpp"

int genMappsOrbitFiles(const char* sceStartTime, const char* sceEndTime, const char* spiceKernels, struct celestialBodies_s celestialBodies)
{
    // LOAD SPICE KERNELS
    // -------------------
    furnsh_c(spiceKernels);

    // ORBIT DATA FILE
    // ----------------
    OrbitDataFile orbitDataFile;
    OrbitDefFile orbitDefFile;
    std::vector <OrbitDataFile::Object_s> orbitDataFileList;
    std::vector<OrbitDataFile::kernelFile> kernelsList;

    OrbitDataFile::Object_s object;

    if (celestialBodies.writeJuice == 1)
    {
        object.name = "JUICE";
        object.nameSpice = "JUICE";
        object.centralBody = "JUPITER";
        object.centralBodySpice = "JUPITER";
        object.startTime = sceStartTime;
        object.endTime = sceEndTime;
        object.fileName = celestialBodies.juiceFilePath;
        object.timeStep = 120;
        object.fileType = "ORBIT_DATA";
        object.timeMargin = 20 * 120;
        orbitDataFileList.push_back(object);
    }

    if (celestialBodies.writeGanymede == 1)
    {
        object.name = "GANYMEDE";
        object.nameSpice = "GANYMEDE";
        object.centralBody = "JUPITER";
        object.centralBodySpice = "JUPITER";
        object.fileName = celestialBodies.ganymedeFilePath;
        object.startTime = sceStartTime;
        object.endTime = sceEndTime;
        object.timeStep = 240;
        object.fileType = "OBJECT_DATA";
        object.timeMargin = 20 * 240;
        orbitDataFileList.push_back(object);
    }

    if (celestialBodies.writeEuropa == 1)
    {
        object.name = "EUROPA";
        object.nameSpice = "EUROPA";
        object.centralBody = "JUPITER";
        object.centralBodySpice = "JUPITER";
        object.fileName = celestialBodies.europaFilePath;
        object.startTime = sceStartTime;
        object.endTime = sceEndTime;
        object.timeStep = 240;
        object.fileType = "OBJECT_DATA";
        object.timeMargin = 20 * 240;
        orbitDataFileList.push_back(object);
    }

    if (celestialBodies.writeCallisto == 1)
    {
        object.name = "CALLISTO";
        object.nameSpice = "CALLISTO";
        object.centralBody = "JUPITER";
        object.centralBodySpice = "JUPITER";
        object.fileName = celestialBodies.callistoFilePath;
        object.startTime = sceStartTime;
        object.endTime = sceEndTime;
        object.timeStep = 240;
        object.fileType = "OBJECT_DATA";
        object.timeMargin = 20 * 240;
        orbitDataFileList.push_back(object);
    }

    for (std::vector<OrbitDataFile::Object_s>::iterator odfIt = orbitDataFileList.begin(); odfIt != orbitDataFileList.end(); ++odfIt)
    {
        orbitDataFile.setObject(*odfIt);
        orbitDataFile.writeFile(odfIt->fileName, odfIt->startTime, odfIt->endTime, odfIt->timeStep, odfIt->timeMargin);
    }

    // ORBIT DEFINITION FILE
    // ---------------------
    std::vector <OrbitDefFile::Object_s> orbitDefFileList;

    if (celestialBodies.writeJuiceOrbDef == 1)
    {
        OrbitDefFile::Object_s objectDef;
        objectDef.name = "JUICE";
        objectDef.nameSpice = "JUICE";
        objectDef.centralBody = "JUPITER";
        objectDef.centralBodySpice = "JUPITER";
        objectDef.fileName = celestialBodies.juiceOrbDefFilePath;
        objectDef.startTime = sceStartTime;
        objectDef.endTime = sceEndTime;
        objectDef.timeStep = 1;
        objectDef.fileType = "ORBIT_DEF";
        orbitDefFileList.push_back(objectDef);
    }

    for (std::vector<OrbitDefFile::Object_s>::iterator odfIt = orbitDefFileList.begin(); odfIt != orbitDefFileList.end(); ++odfIt)
    {
        orbitDefFile.setObject(*odfIt);
        orbitDefFile.writeFile(odfIt->fileName, odfIt->startTime, odfIt->endTime, odfIt->timeStep);
    }

    return 0;
}