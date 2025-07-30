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

#include "OrbitDefFile.hpp"
#include "../Utils/TimeUtils.hpp"

// Standard includes
#include <filesystem>  
#include <iostream>
#include <iomanip>

// External includes
#include "../cspice/include/SpiceUsr.h"

namespace fs = std::filesystem;

OrbitDefFile::OrbitDefFile()
{
}

OrbitDefFile::~OrbitDefFile()
{
}

bool OrbitDefFile::setObject(Object_s object)
{
    _object = object;
    return true;
}

int OrbitDefFile::writeHeader(std::string objectName, std::string centralObjectName, 
                               std::string fileType, std::vector<kernelFile>& kernelsList,
                               std::string startTime, std::string endTime, double timeStep)
{
    double dCurrentTime;
    TimeUtils::getCurrentTime(dCurrentTime);
    std::string strCurrentTime = TimeUtils::absoluteTimeToStr(dCurrentTime);

    std::string timeStepStr;
    TimeUtils::formatRelativeTime (timeStep, timeStepStr);
    _fileHandler << "# -----------------------------------------------------------------------------------" << std::endl;
    _fileHandler << "# " << "Periods " << objectName << " state vectors at centre of " << centralObjectName << ", created by F.Nespoli" << std::endl;
    _fileHandler << "#" << std::endl;
    _fileHandler << "# [Generation Time: " << strCurrentTime << "]" << std::endl;
    _fileHandler << "# [StartTime: " << startTime << " - EndTime: " << endTime << " - Periods Duration: " << std::setprecision (0) << timeStepStr << " ]" << std::endl;
    _fileHandler << "#" << std::endl;
    _fileHandler << writeHeaderKernels (kernelsList);
    _fileHandler << "#" << std::endl;
    _fileHandler << "# Note that Julian dates count from 1 January 2000 at 12:00:00" << std::endl;
    _fileHandler << "#" << std::endl;
    _fileHandler << "#     Time Apo |     Time Peri |  Period number |   Distance to | Distance to " << std::endl;
    _fileHandler << "# (Start Time) | (Center Time) |                | Jupiter start | Jupiter end " << std::endl;
    _fileHandler << "#     UTC (JD) |      UTC (JD) |                |          [Km] |        [Km] " << std::endl;
    _fileHandler << "# -----------------------------------------------------------------------------------" << std::endl;
    _fileHandler << "#" << std::endl;
    _fileHandler << "FILE_TYPE       = " << fileType   << std::endl;
    _fileHandler << "TIME_SCALE      = JD"             << std::endl;
    _fileHandler << "CENTRAL_BODY    = " << centralObjectName << std::endl;
    _fileHandler << "REFERENCE_FRAME = EME"            << std::endl;
    _fileHandler << "#" << std::endl;

    return 0;
}

int OrbitDefFile::getKernelsList (std::vector<kernelFile>& kernelsList)
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

std::string OrbitDefFile::writeHeaderKernels (std::vector<kernelFile>& kernelsList)
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

int OrbitDefFile::writeTimeSlotEntry (timeSlotEntry_s timeSlotEntry)
{
    double utcApoTime;
    double utcPeriTime;
    if (timeSlotEntry.apoTime != 0.0) deltet_c(timeSlotEntry.apoTime, "ET", &utcApoTime);
    else utcApoTime  = 0.0;
    if (timeSlotEntry.periTime != 0.0) deltet_c(timeSlotEntry.periTime, "ET", &utcPeriTime);
    else utcPeriTime = 0.0;

    _fileHandler << std::fixed;
    _fileHandler << std::setw(16) << std::setprecision(9) << (timeSlotEntry.apoTime-utcApoTime)/86400   << " ";
    _fileHandler << std::setw(16) << std::setprecision(9) << (timeSlotEntry.periTime-utcPeriTime)/86400 << " ";
    _fileHandler << std::setfill('0') << std::setw(4)     << timeSlotEntry.slotNum << " " << std::setfill (' ');
    _fileHandler << std::setw(18) << std::setprecision(6) << timeSlotEntry.apoDistance  << " ";
    _fileHandler << std::setw(18) << std::setprecision(6) << timeSlotEntry.periDistance;
    _fileHandler << std::endl;

    return 0;
}


int OrbitDefFile::writeFile(std::string fileName, std::string startTime, std::string endTime, int numOfSlots)
{
    _fileHandler.open(fileName);

    double startTimeET;
    double endTimeET;
    utc2et_c (startTime.c_str (), &startTimeET);
    utc2et_c (endTime.c_str (),   &endTimeET);

    double deltaTime = endTimeET - startTimeET;
    double slotDuration = deltaTime / numOfSlots;
    
    // Write Header
    std::vector<kernelFile> kernelsList;
    getKernelsList (kernelsList);
    writeHeader (_object.name, _object.centralBody, _object.fileType, kernelsList, startTime, endTime, slotDuration);
    
    double lt;
    double objStateApo[6];
    double objStatePeri[6];
    int slotNum = 1;
    double slotStartET = startTimeET;
    while (slotNum <= numOfSlots)
    {
        timeSlotEntry_s timeSlotEntry;
        timeSlotEntry.slotNum  = slotNum;
        timeSlotEntry.apoTime  = slotStartET;
        timeSlotEntry.periTime = slotStartET + slotDuration/2;

        // Get the body distance
        spkezr_c(_object.nameSpice.c_str(), timeSlotEntry.apoTime,  "J2000", "NONE", _object.centralBodySpice.c_str(), objStateApo, &lt);
        spkezr_c(_object.nameSpice.c_str(), timeSlotEntry.periTime, "J2000", "NONE", _object.centralBodySpice.c_str (), objStatePeri, &lt);
        timeSlotEntry.apoDistance  = vnorm_c(objStateApo);
        timeSlotEntry.periDistance = vnorm_c(objStatePeri);

        writeTimeSlotEntry(timeSlotEntry);

        slotStartET += slotDuration;
        slotNum++;
    }

    // Write last dummy slot to close the previous slot
    timeSlotEntry_s timeSlotEntry;
    timeSlotEntry.slotNum  = 9999;
    timeSlotEntry.apoTime  = slotStartET;
    timeSlotEntry.periTime     = 0.0;

    // Get the body distance
    spkezr_c(_object.nameSpice.c_str(), timeSlotEntry.apoTime, "J2000", "NONE", _object.centralBodySpice.c_str(), objStateApo, &lt);
    timeSlotEntry.apoDistance = vnorm_c(objStateApo);
    timeSlotEntry.periDistance = 0.0;
    writeTimeSlotEntry (timeSlotEntry);

    _fileHandler.close();

    return 0;
}