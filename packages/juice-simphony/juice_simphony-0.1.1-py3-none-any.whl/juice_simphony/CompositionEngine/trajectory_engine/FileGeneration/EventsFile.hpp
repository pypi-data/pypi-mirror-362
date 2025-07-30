#pragma once
#include <string>

class EventsFile
{
public:
    typedef struct {
        std::string name;
        int count;
        double time;
    } EventInstance;
    EventsFile();
    ~EventsFile();
    int importFromCsv(std::string fileName);
};

bool compareInterval(EventsFile::EventInstance i1, EventsFile::EventInstance i2);