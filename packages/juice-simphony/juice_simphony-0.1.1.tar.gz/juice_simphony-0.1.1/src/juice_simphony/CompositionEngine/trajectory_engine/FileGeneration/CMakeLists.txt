# CMakeList.txt : CMake project for TrajectoryEngine, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)

#if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  SET(GCC_FILESYSTEM_COMPILE_FLAGS "--std=c++17 -fPIC")
  SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}")
#endif()

# Add source to this project's executable.
file(GLOB SRC *.cpp)
file(GLOB HEAD *.hpp)

message (${SRC})

add_compile_definitions(DLL_API_EXPORTS)
add_compile_definitions(_SILENCE_EXPERIMENTAL_FILESYSTEM_DEPRECATION_WARNING)

add_library (TrajectoryEngine SHARED ${SRC} ${HEAD})


SET (CSPICE_INCLUDE_LIBRARY "${CMAKE_CURRENT_SOURCE_DIR}/../cspice/include")
target_include_directories(TrajectoryEngine PUBLIC ${CSPICE_INCLUDE_LIBRARY})

add_library(libspice STATIC IMPORTED)
SET (CSPICE_MAC_LIBRARY "${CMAKE_CURRENT_SOURCE_DIR}/../cspice/lib/mac/cspice.a")
SET (CSPICE_LINUX_LIBRARY "${CMAKE_CURRENT_SOURCE_DIR}/../cspice/lib/linux/cspice.a")

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    # for MacOS X
    set_target_properties(libspice PROPERTIES IMPORTED_LOCATION ${CSPICE_MAC_LIBRARY})
endif()

if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    message("Linux spice")
    set_target_properties(libspice PROPERTIES IMPORTED_LOCATION ${CSPICE_LINUX_LIBRARY})
endif()

target_link_libraries(TrajectoryEngine PUBLIC libspice)
target_link_libraries (TrajectoryEngine PRIVATE Utils)

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  target_link_libraries(TrajectoryEngine PRIVATE stdc++fs)
  target_link_libraries(TrajectoryEngine PRIVATE pthread)
  target_link_libraries(TrajectoryEngine PRIVATE dl)
  target_link_libraries(TrajectoryEngine PRIVATE -static-libgcc -static-libstdc++)
endif ()
