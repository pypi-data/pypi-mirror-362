//
// Filename:    CommonTypes.hpp
// Module:      Attitude Generator
//
// Description: This unit defines any common data types of the module.
//
// Authors:     Borja Garcia Gutierrez
//              Peter van der Plas
// Date:        28 May 2013
//
// (c) ESA/Estec
//

#ifndef _COMMON_TYPES_HPP_
#define _COMMON_TYPES_HPP_


// This type shall be used for any position, velocity and direction vectors
typedef double AGVec2_t[2];   // meters, meters/second or unit vector
typedef double AGVec3_t[3];   // meters, meters/second or unit vector

// This type defines an attitude matrix (body axes defined as column vectors)
typedef double AGMat33_t[3][3];   // <unitless>

// This type defines a quaternion (q0,q1,q2: vector, q3: magnitude)
typedef double AGQuat_t[4];   // <unitless>

// This type defines a Julian date (reference: 1-Jan-2000 12:00:00)
typedef double AGTime_t;   // seconds

// Wheel Momentum Manadgement Reset struct, used to store data about if a reaction wheel accumulated momentum need to be reseted during the block
struct WMMReset_s {
    bool resetEnabled;
    double resetValue;
};

#endif // _COMMON_TYPES_HPP_
