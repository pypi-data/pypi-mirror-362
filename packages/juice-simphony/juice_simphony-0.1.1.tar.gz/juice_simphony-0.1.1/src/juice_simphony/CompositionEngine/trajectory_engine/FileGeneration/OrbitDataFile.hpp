#pragma once

// Standard includes
#include <fstream>
#include <sstream>
#include <iomanip>
#include <vector>

class OrbitDataFile
{
public:
	typedef struct
	{
		double time;
		double position[3];
		double velocity[3];
	} bodyState_s;

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
		double timeMargin;
	} Object_s;

	typedef struct
	{
		std::string filtype;
		std::string file;
		std::string source;
	} kernelFile;

public:
	OrbitDataFile();
	~OrbitDataFile();
	bool setObject(Object_s object);
	int writeHeader (std::string objectName, std::string centralObjectName,
					 std::string fileType, std::vector<kernelFile>& kernelsList,
					 std::string startTime, std::string endTime, double timeStep);
	std::string writeHeaderKernels (std::vector<kernelFile>& kernelsList);
	int getKernelsList (std::vector<kernelFile>& kernelsList);
	int writeBodyLine(bodyState_s bodyState);
	int writeFile(std::string fileName, std::string startTime, std::string endTime, double deltaTime, double timeMargin);

private:
	std::ofstream _fileHandler;
	std::string _objectName;
	Object_s _object;
};

