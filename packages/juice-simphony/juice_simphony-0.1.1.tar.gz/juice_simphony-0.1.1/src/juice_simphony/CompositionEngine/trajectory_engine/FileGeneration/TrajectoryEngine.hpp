/******************************************************************************
*                                                                             *
* Copyright (C) 2020-2021 by European Space Agency                            *
*                                                                             *
* This file is subject to the terms and conditions defined in file            *
* 'LICENSE.txt', which is part of this source code package.                   *
* No part of the package, including this file, may be copied, modified,       *
* propagated, or distributed except according to the terms contained in the   *
* LICENSE file.                                                               *
*                                                                             *
******************************************************************************/

/**
*  \file   TrajectoryEngine.hpp
*  \author Juice Science Operations Development (ESAC-ESA)
*  \brief  This file contain the OSGE interface definitions
*/

#pragma once

#define SEGREP_DLL_API
#ifdef _WIN32
#  ifndef STATIC_LIB
#    ifdef DLL_API_EXPORTS
#      define SEGREP_DLL_API __declspec(dllexport)
#    else
#      define SEGREP_DLL_API __declspec(dllimport)
#    endif
#  endif
#endif

#ifdef __cplusplus
extern "C" {
#endif
    struct celestialBodies_s
    {
        short int writeCallisto;
        char* callistoFilePath;
        short int writeEuropa;
        char* europaFilePath;
        short int writeGanymede;
        char* ganymedeFilePath;
        short int writeJuice;
        char* juiceFilePath;
        short int writeJuiceOrbDef;
        char* juiceOrbDefFilePath;
    };

    /**
     * @brief The genMappsOrbitFiles is the entry point to exectute the poitning based on the session file.
     * @param rootScenarioPath Provide the top level path of the scenario to be used to resolve the relative paths.
     * @param sessionFilePath Provide the location and name of the seesion file containing all the scenarios files.
     * @return 0 If the execution has been successfull (This doesn't mean that there is no constraints violations)
    */
    SEGREP_DLL_API int genMappsOrbitFiles(const char* sceStartTime, const char* sceEndTime, const char* spiceKernels, struct celestialBodies_s celestialBodies);

#ifdef __cplusplus
}
#endif