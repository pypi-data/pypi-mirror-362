# CMakeList.txt : CMake project for TrajectoryEngine, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)

project ("Test")

set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(CMAKE_VERBOSE_MAKEFILE ON CACHE BOOL "ON")

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=gnu++17 -fPIC")
endif ()

# add_subdirectory(cspice)
add_subdirectory(Utils)
add_subdirectory(FileGeneration)

# Add source to this project's executable.
file(GLOB SRC *.cpp)
file(GLOB HEAD *.hpp)

add_executable (stub ${SRC} ${HEAD})

SET (CSPICE_INCLUDE_LIBRARY "${CMAKE_CURRENT_SOURCE_DIR}/../cspice/lin/include")
target_include_directories(stub PRIVATE ${CSPICE_INCLUDE_LIBRARY})

target_include_directories(stub PRIVATE TrajectoryEngine)

target_link_libraries (stub PRIVATE TrajectoryEngine)