#pragma once

// Standard includes
#include <fstream>
#include <sstream>
#include <iomanip>
#include <vector>

class OrbitDefFile
{
public:
	typedef struct
	{
		int slotNum;
		double apoTime;
		double periTime;
		double apoDistance;
		double periDistance;
	} timeSlotEntry_s;

	typedef struct
	{
		std::string name;
		std::string centralBody;
		std::string nameSpice;
		std::string centralBodySpice;
		std::string fileName;
		std::string startTime;
		std::string endTime;
		double timeStep;
		std::string fileType;
	} Object_s;

	typedef struct
	{
		std::string filtype;
		std::string file;
		std::string source;
	} kernelFile;

public:
	OrbitDefFile();
	~OrbitDefFile();
	bool setObject(OrbitDefFile::Object_s object);
	int writeHeader (std::string objectName, std::string centralObjectName,
					 std::string fileType, std::vector<kernelFile>& kernelsList,
					 std::string startTime, std::string endTime, double timeStep);
	std::string writeHeaderKernels (std::vector<kernelFile>& kernelsList);
	int getKernelsList (std::vector<kernelFile>& kernelsList);
	int writeTimeSlotEntry (timeSlotEntry_s timeSlotEntry);
	int writeFile(std::string fileName, std::string startTime, std::string endTime, int numOfSlots);

private:
	std::ofstream _fileHandler;
	std::string _objectName;
	Object_s _object;
};

