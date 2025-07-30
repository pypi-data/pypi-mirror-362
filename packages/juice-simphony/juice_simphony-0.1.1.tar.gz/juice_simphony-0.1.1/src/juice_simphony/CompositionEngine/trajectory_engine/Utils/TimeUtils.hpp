//
// Filename:    TimeUtils.hpp
// Module:      Attitude Generator
//
// Description: This unit defines the TimeUtils class, which contains a set
//              of utility functions to parse time values from character
//              strings and to format time values for output reporting.
//
// Authors:     Peter van der Plas
// Date:        28 May 2013
//
// (c) ESA/Estec
//

#ifndef _TIME_UTILS_HPP_
#define _TIME_UTILS_HPP_

// System includes
#include <string>

// Application includes
#include "CommonTypes.hpp"


//
// Class: TimeUtils
//
// Description: This class contains a set of utility functions to convert
//              time values to and from character strings. Time values may
//              either represent an absolute time value or a relative time
//              value. An absolute time value is stored in type AGTime_t,
//              which is defined as the number of seconds from a reference
//              date, being 1-1-2000_12:00:00 (noon). A relative time type
//              is simply defined as a number of seconds and is stored in
//              a double. These functions will support the time types as
//              defined in the PT ICD; an absolute time shall be provided
//              as <yyyy-mm-ddThh:mm:ss[.mmm][Z]>, a relative time shall
//              be provided as <[+-][[-[d][d][dT]hh:]mm:]ss[.mmm]>. Note
//              that the use of milli-seconds and the Z-code on relative
//              time values is not defined in the PT ICD, but is allowed
//              here for consistency of the implementation. The general
//              use of milli-seconds in this unit is configurable.
//
class TimeUtils
{
public:
    typedef enum {
      DO_NOT_PARSE_MSECS,
      PARSE_MSECS
    } parse_msecs_e;

    typedef enum {
      DO_NOT_USE_MSECS,
      USE_MSECS
    } use_msecs_e;

    typedef enum {
        DO_NOT_USE_ZULU,
        USE_ZULU
    } use_zulu_e;

    typedef enum {
        DO_NOT_USE_SIGN,
        USE_SIGN
    } use_sign_e;

    typedef enum {
        DO_NOT_USE_DOY,
        USE_DOY
    } use_doy_e;


    //
    // Function: parseAbsoluteTime
    //
    // Description: This function parses a string containing an absolute time
    //              value. The absolute time value is returned to the calling
    //              function. This function returns TRUE in case of success
    //              and FALSE in case any errors were detected.
    //
    static bool parseAbsoluteTime (const std::string &timeString,
                                   AGTime_t &absoluteTime,
                                   parse_msecs_e parseMsecs = TimeUtils::parse_msecs_e::PARSE_MSECS,
                                   use_msecs_e useMsecs =  TimeUtils::use_msecs_e::DO_NOT_USE_MSECS,
                                   use_zulu_e useZulu = TimeUtils::use_zulu_e::DO_NOT_USE_ZULU);

    //
    // Function: parseRelativeTime
    //
    // Description: This function parses a string containing a relative time
    //              value. The relative time value is returned to the calling
    //              function. This function returns TRUE in case of success
    //              and FALSE in case any errors were detected.
    //
    static bool parseRelativeTime (const std::string &timeString,
                                   double &relativeTime,
                                   parse_msecs_e parseMsecs = TimeUtils::parse_msecs_e::PARSE_MSECS,
                                   use_msecs_e useMsecs =  TimeUtils::use_msecs_e::DO_NOT_USE_MSECS);

    //
    // Function: formatAbsoluteTime
    //
    // Description: This function formats an absolute time value for output
    //              reporting. The formatted time is returned to the calling
    //              function. This function returns TRUE in case of success
    //              and FALSE in case any errors were detected.
    //
    static bool formatAbsoluteTime (AGTime_t absoluteTime,
                                    std::string &timeString,
                                    use_msecs_e useMsecs = TimeUtils::use_msecs_e::DO_NOT_USE_MSECS,
                                    use_zulu_e useZulu = TimeUtils::use_zulu_e::DO_NOT_USE_ZULU);

    static bool yearDayToJulianDate(int year, int doy, AGTime_t& julianDate);


    //
    // Function: formatAbsoluteTimeYMD
    //
    // Description: This function formats an absolute time value for output
    //              reporting. The formatted time is returned to the calling
    //              function. This function returns TRUE in case of success
    //              and FALSE in case any errors were detected.
    //
    static bool formatAbsoluteTimeYMD(AGTime_t absoluteTime, std::string& timeString);

    //
    // Function: formatAbsoluteTime
    //
    // Description: This function formats an absolute time value for output
    //              reporting. The formatted time is returned to the calling
    //              function. This function returns TRUE in case of success
    //              and FALSE in case any errors were detected.
    //
    static std::string absoluteTimeToStr (AGTime_t absoluteTime);

    //
    // Function: formatRelativeTime
    //
    // Description: This function formats a relative time value for output
    //              reporting. The formatted time is returned to the calling
    //              function. This function returns TRUE in case of success
    //              and FALSE in case any errors were detected.
    //
    static bool formatRelativeTime (double relativeTime,
                                    std::string &timeString,
                                    use_msecs_e useMsecs = TimeUtils::use_msecs_e::DO_NOT_USE_MSECS,
                                    use_sign_e usePositiveSign = TimeUtils::use_sign_e::DO_NOT_USE_SIGN,
                                    use_doy_e useDoy = TimeUtils::use_doy_e::USE_DOY);

    //
    // Functions: getCurrentTime
    //            formatCurrentTime
    //
    // Description: These functions can be used to get the current time and
    //              return it as an AGM time type or as a formatted absolute
    //              time string. These functions returns TRUE in case of
    //              success and FALSE in case any errors were detected.
    //
    static bool getCurrentTime (AGTime_t &absoluteTime);
    static bool formatCurrentTime (std::string &timeString);

private:
    // Internal constants
    static const int DAYS_IN_MONTH[12];
    static const int JULIAN_REF_YEAR;
    static const int MAX_JULIAN_YEAR;


    // Internal helper functions
    static void getAbsTimeComponents (AGTime_t absoluteTime,
                                    int &day, int &month, int &year,
                                    int &hours, int &minutes, int &seconds,
                                    int &milliSeconds,
                                    use_msecs_e useMsecs = TimeUtils::use_msecs_e::DO_NOT_USE_MSECS);
    static void getRelTimeComponents (double relativeTime,
                                    bool &negativeTime, int &days,
                                    int &hours, int &minutes, int &seconds,
                                    int &milliSeconds,
                                    use_msecs_e useMsecs = TimeUtils::use_msecs_e::DO_NOT_USE_MSECS);
    static bool calendarToJulianDate (int year, int month, int day,
                                    AGTime_t &julianDate);
    static int secondsInYear (int theYear);
    static int daysInMonth (int theYear, int theMonth);
    static bool isLeapYear (int theYear);

    static bool isDigitInPos (const std::string &str, size_t pos);
    static bool isColonInPos (const std::string &str, size_t pos);
    static bool isTSepInPos (const std::string &str, size_t pos);

    static void checkDigitInPos (const std::string &str, size_t pos) noexcept (false);
    static void checkColonInPos (const std::string &str, size_t pos) noexcept (false);
    static void checkTSepInPos (const std::string &str, size_t pos) noexcept (false);

}; // end TimeUtils

#endif // _TIME_UTILS_HPP_