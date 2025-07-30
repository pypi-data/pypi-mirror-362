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

#include "OrbitDataFile.hpp"

// Standard includes
#include <filesystem>
#include <iostream>
#include <iomanip>

// External includes
#include "../cspice/include/SpiceUsr.h"
#include "../Utils/TimeUtils.hpp"

namespace fs = std::filesystem;

OrbitDataFile::OrbitDataFile()
{
}

OrbitDataFile::~OrbitDataFile()
{
}

bool OrbitDataFile::setObject(Object_s object)
{
    _object = object;
    return true;
}

int OrbitDataFile::writeHeader(std::string objectName, std::string centralObjectName, 
                               std::string fileType, std::vector<kernelFile>& kernelsList,
                               std::string startTime, std::string endTime, double timeStep)
{
    double dCurrentTime;
    TimeUtils::getCurrentTime(dCurrentTime);
    std::string strCurrentTime = TimeUtils::absoluteTimeToStr(dCurrentTime);

    _fileHandler << "# -----------------------------------------------------------------------------------" << std::endl;
    _fileHandler << "# " << objectName << " state vectors from centre of " << centralObjectName << ", created by F.Nespoli" << std::endl;
    _fileHandler << "#" << std::endl;
    _fileHandler << "# [Generation Time: " << strCurrentTime << "]" << std::endl;
    _fileHandler << "# [StartTime: " << startTime << " - EndTime: " << endTime << " - TimeStep: " << std::setprecision (0) << timeStep << "s ]" << std::endl;
    _fileHandler << "#" << std::endl;
    _fileHandler << writeHeaderKernels (kernelsList);
    _fileHandler << "#" << std::endl;
    _fileHandler << "# Note that Julian dates count from 1 January 2000 at 12:00:00" << std::endl;
    _fileHandler << "#" << std::endl;
    _fileHandler << "#        Time   PositionX   PositionY   PositionZ    VelX    VelY    VelZ" << std::endl;
    _fileHandler << "#    UTC (JD)        (Km)        (Km)        (Km)  (Km/s)  (Km/s)  (Km/s)" << std::endl;
    _fileHandler << "# -----------------------------------------------------------------------------------" << std::endl;
    _fileHandler << "#" << std::endl;
    _fileHandler << "FILE_TYPE       = " << fileType   << std::endl;
    _fileHandler << "TIME_SCALE      = JD"             << std::endl;
    _fileHandler << "CENTRAL_BODY    = " << centralObjectName << std::endl;
    _fileHandler << "REFERENCE_FRAME = EME"            << std::endl;
    _fileHandler << "#" << std::endl;

    return 0;
}

int OrbitDataFile::getKernelsList (std::vector<kernelFile>& kernelsList)
{
    SpiceInt numOfKernels;
    ktotal_c ("all", &numOfKernels);

    for (int kernelCnt = 0; kernelCnt < numOfKernels; ++kernelCnt)
    {
        SpiceInt  count;
        SpiceInt  handle;

        const int FILLEN = 256;
        const int TYPLEN = 33;
        const int SRCLEN = 256;

        SpiceChar file[FILLEN];
        SpiceChar filtype[TYPLEN];
        SpiceChar source[SRCLEN];

        SpiceBoolean found;
        kdata_c (kernelCnt, "all", FILLEN, TYPLEN, SRCLEN, file, filtype, source, &handle, &found);

        kernelFile kernel;
        kernel.file    = file;
        kernel.filtype = filtype;
        kernel.source  = source;

        kernelsList.push_back (kernel);
    }

    return 0;
}

std::string OrbitDataFile::writeHeaderKernels (std::vector<kernelFile>& kernelsList)
{
    std::string comment = "#";
    std::stringstream kernelsHeadersStr;
    kernelsHeadersStr << comment << " " << "[Source: SPICE-Kernels]" << std::endl;
    for (std::vector<kernelFile>::iterator klIt = kernelsList.begin (); klIt != kernelsList.end (); ++klIt)
    {
        fs::path kernelPath(klIt->file);
        kernelsHeadersStr << comment;
        std::stringstream kernelsType;
        kernelsType << " [" << kernelPath.parent_path ().filename ().string () << "] ";
        kernelsHeadersStr << std::left << std::setw(8) << kernelsType.str();
        kernelsHeadersStr << kernelPath.filename () << std::endl;
    }
    return kernelsHeadersStr.str();
}

int OrbitDataFile::writeBodyLine(bodyState_s bodyState)
{
    double utcTime;
    deltet_c(bodyState.time, "ET", &utcTime);
    _fileHandler << std::fixed;
    _fileHandler << std::setprecision(9) << (bodyState.time - utcTime) / 86400 << " ";
    _fileHandler << std::setw(15) << std::setprecision(6) << bodyState.position[0] << " ";
    _fileHandler << std::setw(15) << std::setprecision(6) << bodyState.position[1] << " ";
    _fileHandler << std::setw(15) << std::setprecision(6) << bodyState.position[2] << " ";
    _fileHandler << std::setw(11) << std::setprecision(6) << bodyState.velocity[0] << " ";
    _fileHandler << std::setw(11) << std::setprecision(6) << bodyState.velocity[1] << " ";
    _fileHandler << std::setw(11) << std::setprecision(6) << bodyState.velocity[2];
    _fileHandler << std::endl;

    return 0;
}


int OrbitDataFile::writeFile(std::string fileName, std::string startTime, std::string endTime, double deltaTime, double timeMargin)
{
    _fileHandler.open(fileName);

    std::vector<kernelFile> kernelsList;
    getKernelsList (kernelsList);

    // Add margin
    double deltaStartTime;
    double deltaEndTime;
    TimeUtils::parseAbsoluteTime(startTime, deltaStartTime);
    TimeUtils::parseAbsoluteTime(endTime,   deltaEndTime);

    deltaStartTime -= timeMargin;
    deltaEndTime   += timeMargin;
    std::string  deltaStartTimeStr = TimeUtils::absoluteTimeToStr(deltaStartTime);
    std::string  deltaEndTimeStr   = TimeUtils::absoluteTimeToStr(deltaEndTime);

    writeHeader(_object.name, _object.centralBody, _object.fileType, kernelsList, deltaStartTimeStr, deltaEndTimeStr, deltaTime);

    double startTimeET;
    double endTimeET;
    utc2et_c(deltaStartTimeStr.c_str(), &startTimeET);
    utc2et_c(deltaEndTimeStr.c_str(), &endTimeET);

    double stepET   = deltaTime;
    double utcDelta = deltaTime;
    double et = startTimeET;
    endTimeET = endTimeET;

    while (et <= endTimeET + 0.1)
    {
        // Get the position of EXOMARS
        double lt;
        double objState[6];
        spkezr_c(_object.nameSpice.c_str(), et, "J2000", "NONE", _object.centralBodySpice.c_str(), objState, &lt);

        bodyState_s bodyState;
        bodyState.time = et;
        bodyState.position[0] = objState[0];
        bodyState.position[1] = objState[1];
        bodyState.position[2] = objState[2];
        bodyState.velocity[0] = objState[3];
        bodyState.velocity[1] = objState[4];
        bodyState.velocity[2] = objState[5];
        writeBodyLine(bodyState);

        et = et + stepET;
    }

    _fileHandler.close();

    return 0;
}