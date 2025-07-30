//
// Filename:    Conversions.hpp
// Module:      Attitude Generator
//
// Description: This unit defines any general conversion factors and macros
//              of the module.
//
// Authors:     Borja Garcia Gutierrez
//              Peter van der Plas
// Date:        29 May 2013
//
// (c) ESA/Estec
//

#ifndef _CONVERSIONS_HPP_
#define _CONVERSIONS_HPP_

// General angle units conversion constants
#define AG_RAD2DEG   57.29577951308232087680
#define AG_DEG2RAD    0.01745329251994329577

// General time units conversion constants
#define AG_DAY2SEC     86400
#define AG_DAY2SECF    86400.0
#define AG_DAY2SEC2    43200
#define AG_DAY2SEC2F   43200.0

// General angle units conversion macros
#define AGRadToDeg(x)   (57.29577951308232087680*(x))
#define AGDegToRad(x)   ( 0.01745329251994329577*(x))

// General distance units conversion macros
#define AGMToKm(x)      ((x)/1000.0)
#define AGKmToM(x)      ((x)*1000.0)

#endif // _CONVERSIONS_HPP_
