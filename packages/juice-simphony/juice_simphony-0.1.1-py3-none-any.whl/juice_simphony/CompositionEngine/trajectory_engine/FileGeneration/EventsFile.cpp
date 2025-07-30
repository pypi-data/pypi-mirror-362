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

#include "EventsFile.hpp"
#include "../Utils/rapidcsv.hpp"
#include "../Utils/TimeUtils.hpp"
#include <fstream>
#include <iomanip>
#include <algorithm>

EventsFile::EventsFile()
{}

EventsFile::~EventsFile()
{}

int EventsFile::importFromCsv(std::string fileName)
{
    rapidcsv::Document csvEvtFile(fileName);
    std::vector<std::string> EventName = csvEvtFile.GetColumn<std::string>("EventName");
    std::vector<std::string> StartTime = csvEvtFile.GetColumn<std::string>("StartTime");
    std::vector<std::string> EndTime   = csvEvtFile.GetColumn<std::string>("EndTime");

    std::cout << "Read " << EventName.size() << " values." << std::endl;
    int csvSize = EventName.size();
    std::vector<EventInstance> EventTimeline;


    // Write Header
    std::ofstream gsVisFile;
    gsVisFile.open(R"(C:\outputs\GVIS.txt)");

    gsVisFile << "# Ground station data converted from ESOC FD event file" << std::endl;
    gsVisFile << "#" << std::endl;
    gsVisFile << "# Note that Julian dates count from 12:00:00 noon, 1 January 2000" << std::endl;
    gsVisFile << "#" << std::endl;
    gsVisFile << "# GS Start time End time" << std::endl;
    gsVisFile << "# UTC (JD) UTC (JD)" << std::endl;
    gsVisFile << "#" << std::endl;
    gsVisFile << "FILE_TYPE = GS_VIS_PERIODS" << std::endl;
    gsVisFile << "TIME_SCALE = JD" << std::endl;
    gsVisFile << "#" << std::endl;
    int malEvtCnt = 0;
    int cebEvtCnt = 0;
    int gdsEvtCnt = 0;
    for (int index = 0; index < csvSize; index++)
    {
        double dStartTime;
        TimeUtils::parseAbsoluteTime(StartTime[index], dStartTime);
        double dEndtime;
        TimeUtils::parseAbsoluteTime(EndTime[index], dEndtime);

        std::string stationID;
        EventInstance evtInstanceStart;
        EventInstance evtInstanceEnd;

        if (EventName[index].compare("VISIBILITY_MALARGUE_START_END") == 0)
        {
            malEvtCnt++;
            evtInstanceStart.count = malEvtCnt;
            evtInstanceEnd.count = malEvtCnt;
            stationID = "MAL";
        }

        else if (EventName[index].compare("VISIBILITY_CEBREROS_START_END") == 0)
        {
            cebEvtCnt++;
            evtInstanceStart.count = cebEvtCnt;
            evtInstanceEnd.count = cebEvtCnt;
            stationID = "CEB";
        }

        else if (EventName[index].compare("VISIBILITY_GOLDSTONE_START_END") == 0)
        {
            gdsEvtCnt++;
            evtInstanceStart.count = gdsEvtCnt;
            evtInstanceEnd.count = gdsEvtCnt;
            stationID = "GDS";
        }

        // Only station visibility events are allowed
        if (!stationID.empty())
        {
            gsVisFile << stationID << "  ";
            gsVisFile << std::fixed;
            gsVisFile << std::setw(16) << std::setprecision(8) << dStartTime / 86400 << " ";
            gsVisFile << std::setw(16) << std::setprecision(8) << dEndtime / 86400 << std::endl;


            std::string radixEvtName = EventName[index];
            int subStrPos = 0; 
            subStrPos = radixEvtName.find("_START_END", subStrPos);

            if (subStrPos != std::string::npos)
            {
                // Make the replacement.
                radixEvtName.replace(subStrPos, 10, "");
            }

            evtInstanceStart.name = radixEvtName + "_START";
            evtInstanceStart.time = dStartTime;
            EventTimeline.push_back(evtInstanceStart);

            evtInstanceEnd.name = radixEvtName + "_END";
            evtInstanceEnd.time = dEndtime;
            EventTimeline.push_back(evtInstanceEnd);

        }
    }
    gsVisFile.close();

    std::sort(EventTimeline.begin(), EventTimeline.end(), compareInterval);

    std::ofstream evtVisFile;
    evtVisFile.open(R"(C:\outputs\EVENTS.txt)");

    for (int evtCnt = 0; evtCnt < EventTimeline.size(); evtCnt++)
    {
        std::string strTime = TimeUtils::absoluteTimeToStr(EventTimeline[evtCnt].time);
        evtVisFile << strTime << "  " << EventTimeline[evtCnt].name << " " << "(COUNT = ";
        evtVisFile << std::setfill('0') << std::setw(4) << EventTimeline[evtCnt].count << std::setfill(' ') << ")" << std::endl;
    }
    evtVisFile.close();
    return 0;
}

// Compares two intervals according to staring times. 
bool compareInterval(EventsFile::EventInstance i1, EventsFile::EventInstance i2)
{
    return (i1.time < i2.time);
}
