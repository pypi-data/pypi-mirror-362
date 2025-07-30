# CMakeList.txt : CMake project for TrajectoryEngine, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)

#if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  SET(GCC_FILESYSTEM_COMPILE_FLAGS "--std=c++17 -lstdc++fs")
  SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}")
#endif()

# Add source to this project's executable.
file(GLOB SRC *.cpp)
file(GLOB HEAD *.hpp)

add_library (Utils ${SRC} ${HEAD})