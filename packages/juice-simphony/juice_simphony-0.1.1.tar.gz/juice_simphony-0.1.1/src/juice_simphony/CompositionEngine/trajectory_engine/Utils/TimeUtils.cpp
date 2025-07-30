//
// Filename:    TimeUtils.cpp
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

// System includes
#include <sstream>
#include <ctime>
#include <stdexcept>
#include <cctype>

// Application includes
#include "TimeUtils.hpp"
#include "Conversions.hpp"

// Used namespaces
using namespace std;

// Internal constants
const int TimeUtils::DAYS_IN_MONTH[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
const int TimeUtils::JULIAN_REF_YEAR = 2000;
const int TimeUtils::MAX_JULIAN_YEAR = 50;

//
// Function: TimeUtils::parseAbsoluteTime
//
// Description: This function parses a string containing an absolute time
//              value. The absolute time value is returned to the calling
//              function. This function returns TRUE in case of success
//              and FALSE in case any errors were detected.
//
// yyyy-mm-ddThh:mm:ss[.mmm][Z] or yyyy-dddThh:mm:ss[.mmm][Z]
//
bool TimeUtils::parseAbsoluteTime (const std::string &timeString, AGTime_t &absoluteTime,
                                   parse_msecs_e parseMsecs, use_msecs_e useMsecs, use_zulu_e useZulu)
{
    try
    {
        unsigned int index = 0;
        const size_t length = timeString.length ();

        /////
        // Get the year part
        /////
        checkDigitInPos (timeString, index);
        int year = timeString[index] - '0';
        index++;

        checkDigitInPos (timeString, index);
        year = 10 * year + timeString[index] - '0';
        index++;

        checkDigitInPos (timeString, index);
        year = 10 * year + timeString[index] - '0';
        index++;

        checkDigitInPos (timeString, index);
        year = 10 * year + timeString[index] - '0';
        index++;

        // Check for the year-month separator
        if (index >= length)
            return false;
        if (timeString[index] != '-')
            return false;
        index++;
        /////

        /////
        // Get the month part
        /////
        checkDigitInPos (timeString, index);
        int temp = timeString[index] - '0';
        index++;

        checkDigitInPos (timeString, index);
        temp = 10 * temp + timeString[index] - '0';
        index++;

        // Check for the month-day separator
        if (index >= length) return false;
        bool isDoy = false;
        int month = 0;
        int doy = 0;
        int day = 0;
        if (timeString[index] == '-')
        {
            index++;
            month = temp;
            ////
            // Get the day part
            /////
            checkDigitInPos(timeString, index);
            day = timeString[index] - '0';
            index++;

            checkDigitInPos(timeString, index);
            day = 10 * day + timeString[index] - '0';
            index++;

        }
        else
        {
            isDoy = true;
            checkDigitInPos(timeString, index);
            doy = 10 * temp + timeString[index] - '0';
            index++;
        }
        /////


        // Check for the date code character
        if (index >= length)
        {
            return false;
        }

        if (timeString[index] != 'T')
        {
            return false;
        }
        index++;
        /////


        /////
        // Get the hours part
        /////
        checkDigitInPos (timeString, index);
        int hours = timeString[index] - '0';
        index++;

        checkDigitInPos (timeString, index);
        hours = 10 * hours + timeString[index] - '0';
        index++;
        if (hours > 23)
        {
            return false;
        }

        // Check for the hours-minutes separator
        if (index >= length)
        {
            return false;
        }

        if (timeString[index] != ':')
        {
            return false;
        }
        index++;
        /////

        /////
        // Get the minutes part
        /////
        checkDigitInPos (timeString, index);
        int minutes = timeString[index] - '0';
        index++;

        checkDigitInPos (timeString, index);
        minutes = 10 * minutes + timeString[index] - '0';
        index++;

        if (minutes > 59)
        {
            return false;
        }

        // Check for the minutes-seconds separator
        if (index >= length)
            return false;
        if (timeString[index] != ':')
            return false;
        index++;
        /////

        /////
        // Get the seconds part
        /////
        checkDigitInPos (timeString, index);
        int seconds = timeString[index] - '0';
        index++;

        checkDigitInPos (timeString, index);
        seconds = 10 * seconds + timeString[index] - '0';
        index++;

        if (seconds > 59)
        {
            return false;
        }
        /////

        /////
        // Check for the optional seconds-milliseconds separator
        /////
        int milliSeconds = 0;
        if (index < length)
        {
            if (timeString[index] == '.')
            {
                // Check if milliseconds part allowed
                if (parseMsecs == TimeUtils::parse_msecs_e::DO_NOT_PARSE_MSECS)
                {
                    return false;
                }

                // Get the milliseconds part
                index++;

                checkDigitInPos (timeString, index);
                milliSeconds = timeString[index] - '0';
                index++;

                checkDigitInPos (timeString, index);
                milliSeconds = 10 * milliSeconds + timeString[index] - '0';
                index++;

                checkDigitInPos (timeString, index);
                milliSeconds = 10 * milliSeconds + timeString[index] - '0';
                index++;
            }
        }
        /////

        // Check for the time code character
        if (index < length)
        {
            if (useZulu == TimeUtils::use_zulu_e::DO_NOT_USE_ZULU ||
                timeString[index] != 'Z')
            {
                return false;
            }

            index++;
        }

        // Check for any trailing garbage
        if (index < length)
        {
            return false;
        }
        if (isDoy)
        {
            if (!yearDayToJulianDate(year,doy, absoluteTime))
            {
                return false;
            }
        }
        else
        {
            // Compute the Julian date for the date part
            if (!calendarToJulianDate(year, month, day, absoluteTime))
            {
                return false;
            }
        }

        if (useMsecs == TimeUtils::use_msecs_e::DO_NOT_USE_MSECS)
        {
            milliSeconds = 0;
        }

        // Add the time part to the total Julian date
        absoluteTime += 3600.0 * hours + 60.0 * minutes + seconds + 0.001 * milliSeconds;

        return true;
    }
    catch (const std::runtime_error &/*re*/)
    {
        return false;
    }
}

//
// Function: TimeUtils::parseRelativeTime
//
// Description: This function parses a string containing a relative time
//              value. The relative time value is returned to the calling
//              function. This function returns TRUE in case of success
//              and FALSE in case any errors were detected.
//
// [+/-][d][d][d][T][hh:]mm:ss[.mmm]
//
bool TimeUtils::parseRelativeTime (const std::string &timeString, double &relativeTime, parse_msecs_e parseMsecs, use_msecs_e useMsecs)
{
   try
   {
       size_t index = 0;
       const size_t length = timeString.length();

       /////////
       // Get the optional sign
       /////////
       bool negativeTime = false;
       if (index >= length)
       {
           return false;
       }

       if (timeString[index] == '-')
       {
           negativeTime = true;
           index++;
       }
       else if (timeString[index] == '+')
       {
           negativeTime = false;
           index++;
       }
       //////////////////////

       /////////
       // Check if the days part is available
       /////////
       bool hasDays = false;
       if ((index + 3) < length)
       {
           hasDays = isTSepInPos(timeString, index + 1) ||
                     isTSepInPos(timeString, index + 2)  ||
                     isTSepInPos(timeString, index + 3) ;
       }

       int days = 0;
       if (hasDays)
       {
           // Get the days part
           checkDigitInPos (timeString, index);
           days = timeString[index] - '0';
           index++;

           if (isTSepInPos(timeString, index + 1)  ||
               isTSepInPos(timeString, index + 2) )
           {
               checkDigitInPos (timeString, index);
               days = 10 * days + timeString[index] - '0';
               index++;
           }

           if (isTSepInPos(timeString, index + 1))
           {
               checkDigitInPos (timeString, index);
               days = 10 * days + timeString[index] - '0';
               index++;
           }

           // Check for the date code character
           checkTSepInPos(timeString, index);
           index++;
       }
       /////////

       /////////
       // Check if the hours part is available
       /////////
       bool hasHours = false;
       if ((index + 5) < length)
       {
           hasHours =  isColonInPos(timeString, index + 2) ||
                       isColonInPos(timeString, index + 5);
       }

       int hours = 0;
       if (hasHours)
       {
           // Get the hours part
           checkDigitInPos (timeString, index);
           hours = timeString[index] - '0';

           index++;
           checkDigitInPos (timeString, index);
           hours = 10 * hours + timeString[index] - '0';

           if (hours > 23)
           {
               return false;
           }
           index++;

           // Check for the hours-minutes separator
           checkColonInPos(timeString, index);
           index++;
       }
       /////////

       /////////
       // Check if the minutes part is available
       /////////
       bool hasMinutes = false;

       if ((index + 2) <= length)
       {
           checkColonInPos(timeString, index + 2);
           hasMinutes =  isColonInPos(timeString, index + 2);
       }

       int minutes = 0;
       if (hasMinutes)
       {

           // Get the minutes part
           checkDigitInPos (timeString, index);
           minutes = timeString[index] - '0';
           index++;

           checkDigitInPos (timeString, index);
           minutes = 10 * minutes + timeString[index] - '0';
           index++;

           if (minutes > 59)
           {
               return false;
           }

           // Check for the minutes-seconds separator
           checkColonInPos(timeString, index);
           index++;
       }
       /////////


       /////////
       // Get the seconds part
       /////////
       checkDigitInPos (timeString, index);
       int seconds = timeString[index] - '0';
       index++;

       checkDigitInPos (timeString, index);
       seconds = 10 * seconds + timeString[index] - '0';
       index++;

       if (seconds > 59)
       {
           return false;
       }
       /////////


       /////////
       // Check for the optional seconds-milliseconds separator
       /////////
       int milliSeconds = 0;
       if (index < length)
       {
           if (timeString[index] == '.')
           {
               if (parseMsecs == TimeUtils::parse_msecs_e::DO_NOT_PARSE_MSECS)
               {
                   return false;
               }

               // Get the milliseconds part
               index++;
               checkDigitInPos (timeString, index);
               milliSeconds = timeString[index] - '0';
               index++;

               checkDigitInPos (timeString, index);
               milliSeconds = 10 * milliSeconds + timeString[index] - '0';
               index++;

               checkDigitInPos (timeString, index);
               milliSeconds = 10 * milliSeconds + timeString[index] - '0';
               index++;
           }
       }
       /////////


       // Check for any trailing garbage
       if (index < length)
       {
           return false;
       }

       if (useMsecs == TimeUtils::use_msecs_e::DO_NOT_USE_MSECS)
       {
           milliSeconds = 0;
       }

       // Compute the relative time value
       relativeTime = AG_DAY2SECF * days + 3600.0 * hours + 60.0 * minutes + seconds + 0.001 * milliSeconds;
       if (negativeTime)
       {
           relativeTime *= -1.0;
       }

       return true;
   }
   catch (const std::runtime_error &/*re*/)
   {
       return false;
   }
}


//===========================================================================
// NAME: isDigitInPos
//===========================================================================
bool TimeUtils::isDigitInPos (const std::string &str, size_t pos)
{
    const size_t length = str.length();

    if (pos >= length)
    {
        return false;
    }

    return std::isdigit (str[pos])?true:false;
}

//===========================================================================
// NAME: isColonInPos
//===========================================================================
bool TimeUtils::isColonInPos (const std::string &str, size_t pos)
{
    const size_t length = str.length();

    if (pos >= length)
    {
        return false;
    }

    return str[pos] == ':';
}

//===========================================================================
// NAME: isTSepInPos
//===========================================================================
bool TimeUtils::isTSepInPos (const std::string &str, size_t pos)
{
    const size_t length = str.length();

    if (pos >= length)
    {
        return false;
    }

    return str[pos] == 'T';
}

//===========================================================================
// NAME: checkDigitInPos
//===========================================================================
void TimeUtils::checkDigitInPos (const std::string &str, size_t pos) noexcept(false)
{
    if (pos >= str.length())
    {
        throw std::runtime_error("Index out of bound");
    }

    if (!isDigitInPos (str, pos))
    {
        throw std::runtime_error("Is not a digit");
    }
}

//===========================================================================
// NAME: checkColonInPos
//===========================================================================
void TimeUtils::checkColonInPos (const std::string &str, size_t pos) noexcept(false)
{
    if (pos >= str.length())
    {
        throw std::runtime_error("Index out of bound");
    }

    if (!isColonInPos (str, pos))
    {
        throw std::runtime_error("Is not a colon");
    }
}

//===========================================================================
// NAME: checkTSepInPos
//===========================================================================
void TimeUtils::checkTSepInPos (const std::string &str, size_t pos) noexcept(false)
{
    if (pos >= str.length())
    {
        throw std::runtime_error("Index out of bound");
    }

    if (!isTSepInPos (str, pos))
    {
        throw std::runtime_error("Is not a T separator");
    }
}


//=================================================================
// Function: TimeUtils::formatAbsoluteTime
//
// Description: This function formats an absolute time value for output
//              reporting. The formatted time is returned to the calling
//              function. This function returns TRUE in case of success
//              and FALSE in case any errors were detected.
//=================================================================
bool TimeUtils::formatAbsoluteTime (AGTime_t absoluteTime, string &timeString, use_msecs_e useMsecs, use_zulu_e useZulu)
{
   // Get the absolute time components
   int day, month, year;
   int hours, minutes, seconds;
   int milliSeconds;
   getAbsTimeComponents (absoluteTime,
                         day, month, year,
                         hours, minutes, seconds,
                         milliSeconds);
   
   // Check if the year is within reasonable limits
   if (year <  (JULIAN_REF_YEAR - MAX_JULIAN_YEAR) ||
       year >= (JULIAN_REF_YEAR + MAX_JULIAN_YEAR))
      return false;
   
   // Create an output stream
   ostringstream timeStream;
   
   // Format the abolute time components
   timeStream.fill ('0');
   timeStream.width (4);
   timeStream << year;
   timeStream.width (1);
   timeStream << '-';
   timeStream.width (2);
   timeStream << month;
   timeStream.width (1);
   timeStream << '-';
   timeStream.width (2);
   timeStream << day;
   timeStream.width (1);
   timeStream << 'T';
   timeStream.width (2);
   timeStream << hours;
   timeStream.width (1);
   timeStream << ':';
   timeStream.width (2);
   timeStream << minutes;
   timeStream.width (1);
   timeStream << ':';
   timeStream.width (2);
   timeStream << seconds;
   
   // Write the optional milli-seconds part
   if (useMsecs == TimeUtils::use_msecs_e::USE_MSECS)
   {
      timeStream.width (1);
      timeStream << '.';
      timeStream.width (3);
      timeStream << milliSeconds;
   }
   
   // Write the optional time code character
   if (useZulu)
   {
      timeStream.width (1);
      timeStream << 'Z';
   }
   
   // Return the resulting string
   timeString = timeStream.str();
   
   // Return success status
   return true;
   
} // end TimeUtils::formatAbsoluteTime


//=================================================================
// Function: TimeUtils::formatAbsoluteTimeYMD
//
// Description: This function formats an absolute time value for output
//              reporting. The formatted time is returned to the calling
//              function. This function returns TRUE in case of success
//              and FALSE in case any errors were detected.
//=================================================================
bool TimeUtils::formatAbsoluteTimeYMD(AGTime_t absoluteTime, string& timeString)
{
    // Get the absolute time components
    int day, month, year;
    int hours, minutes, seconds;
    int milliSeconds;
    getAbsTimeComponents(absoluteTime,
                         day, month, year,
                         hours, minutes, seconds,
                         milliSeconds);

    // Check if the year is within reasonable limits
    if (year < (JULIAN_REF_YEAR - MAX_JULIAN_YEAR) ||
        year >= (JULIAN_REF_YEAR + MAX_JULIAN_YEAR))
        return false;

    // Create an output stream
    ostringstream timeStream;

    // Format the abolute time components
    timeStream.fill('0');
    timeStream.width(2);
    timeStream << year-2000;
    timeStream.width(2);
    timeStream << month;
    timeStream.width(2);
    timeStream << day;

    // Return the resulting string
    timeString = timeStream.str();

    // Return success status
    return true;

} // end TimeUtils::formatAbsoluteTime




//===================================================
// NAME: absoluteTimeToStr
//===================================================
std::string TimeUtils::absoluteTimeToStr(AGTime_t absoluteTime)
{
    std::string strAbsoluteTime;
    formatAbsoluteTime(absoluteTime, strAbsoluteTime);
    return strAbsoluteTime;
}



//=================================================================
// Function: TimeUtils::formatRelativeTime
//
// Description: This function formats a relative time value for output
//              reporting. The formatted time is returned to the calling
//              function. This function returns TRUE in case of success
//              and FALSE in case any errors were detected.
//=================================================================
bool TimeUtils::formatRelativeTime (double relativeTime, std::string &timeString,
                                    use_msecs_e useMsecs, use_sign_e usePositiveSign, use_doy_e useDoy)
{
   // Get the relative time components
   bool negativeTime;
   int days;
   int hours, minutes, seconds;
   int milliSeconds;
   getRelTimeComponents (relativeTime,
                         negativeTime, days,
                         hours, minutes, seconds,
                         milliSeconds);
   
   // Check if the number of days is within limits
   if (days > 999)   // only 3 digits for days
      return false;

   std::ostringstream timeStream;
   
   // Format the optional sign indicator
   if (negativeTime) {
      timeStream.width (1);
      timeStream << '-';
   }
   else if (usePositiveSign &&
            !(days == 0 && hours == 0 && minutes == 0 && seconds == 0 &&
              (milliSeconds == 0 || useMsecs == TimeUtils::DO_NOT_USE_MSECS)))
   {
      timeStream.width (1);
      timeStream << '+';
   }
   
   // Format the relative time components
   timeStream.fill ('0');
   if (days > 0 || useDoy == TimeUtils::use_doy_e::USE_DOY)
   {
      timeStream.width (3);
      timeStream << days;
      timeStream.width (1);
      timeStream << 'T';
   }
   if (days > 0 || hours > 0 || useDoy == TimeUtils::use_doy_e::USE_DOY)
   {
      timeStream.width (2);
      timeStream << hours;
      timeStream.width (1);
      timeStream << ':';
   }
   if (days > 0 || hours > 0 || minutes > 0 || useDoy == TimeUtils::use_doy_e::USE_DOY)
   {
      timeStream.width (2);
      timeStream << minutes;
      timeStream.width (1);
      timeStream << ':';
   }
   timeStream.width (2);
   timeStream << seconds;
   
   // Write the optional milli-seconds part
   if (useMsecs == TimeUtils::use_msecs_e::USE_MSECS)
   {
      timeStream.width (1);
      timeStream << '.';
      timeStream.width (3);
      timeStream << milliSeconds;
   }
   
   // Return the resulting string
   timeString = timeStream.str();
   

   return true;
}



//=================================================================
// Functions: TimeUtils::getCurrentTime
//            TimeUtils::formatCurrentTime
//
// Description: These functions can be used to get the current time and
//              return it as an AGM time type or as a formatted absolute
//              time string. These functions returns TRUE in case of
//              success and FALSE in case any errors were detected.
//=================================================================
bool TimeUtils::getCurrentTime (AGTime_t &absoluteTime)
{
   // Get the current time (using the 1970 time scale of the system)
   AGTime_t currentTime1970 = (AGTime_t) time (0);
   
   // Get the reference time for the 1970 time scale in the AGM time scale
   AGTime_t referenceTime1970;
   if (!TimeUtils::parseAbsoluteTime ("1970-01-01T00:00:00",
                                      referenceTime1970))
      return false;   // error to be reported by calling function
   
   // Return the value in the AGM time scale (w.r.t. 1-1-2000_12:00:00)
   absoluteTime = currentTime1970 + referenceTime1970;

   return true;
}

//=================================================================
//  NAME: formatCurrentTime
//=================================================================
bool TimeUtils::formatCurrentTime (std::string &timeString)
{
   AGTime_t currentTime;
   if (!getCurrentTime (currentTime))
      return false;   // error to be reported by calling function
   
   // Format the current time value
   return formatAbsoluteTime (currentTime, timeString);   // error to be reported by calling function
}



//=================================================================
// Function: TimeUtils::getAbsTimeComponents
//
// Description: This function returns the date components of a pure
//              Julian day number (given in seconds). The day number
//              counts from 1 to 31, the month number counts from 1 to
//              12 and the year is the full four digit year number.
//              The number of milli-seconds is only computed when the
//              TimeUtils are set to milli-second resolution, otherwise
//              the number of milli-seconds is set to zero and the
//              number of seconds is rounded off to the nearest second.
//=================================================================
void TimeUtils::getAbsTimeComponents (AGTime_t absoluteTime,
                                      int &day, int &month, int &year,
                                      int &hours, int &minutes, int &seconds,
                                      int &milliSeconds,
                                      use_msecs_e useMsecs)
{
   // Convert time into integer value in seconds
   int integerTime;
   if (useMsecs == TimeUtils::use_msecs_e::USE_MSECS)
   {
      integerTime = (int)absoluteTime;
      if (absoluteTime < 0.0) {
         milliSeconds = (int)(-1000.0 * (absoluteTime - integerTime) + 0.5);
         if (milliSeconds == 1000) {
            integerTime--;
            milliSeconds = 0;
         }
      }
      else {
         milliSeconds = (int)(1000.0 * (absoluteTime - integerTime) + 0.5);
         if (milliSeconds == 1000)
         {
            integerTime++;
            milliSeconds = 0;
         }
      }
   }
   else {   // no milli-second resolution
      if (absoluteTime < 0.0)
         integerTime = (int)(absoluteTime - 0.5);
      else
         integerTime = (int)(absoluteTime + 0.5);
      milliSeconds = 0;
   }
   
   // UTC counts from 12:00 noon, so correct to 0:00
   integerTime += AG_DAY2SEC2;
   
   // Check in what year we are in, this will shift the time to
   // the correct year, so the corrected time in seconds will
   // fall within the current year.
   int currentYear = JULIAN_REF_YEAR;
   while (integerTime < 0 ||
          integerTime >= secondsInYear (currentYear)) {

      // Check if we have to go to previous or next year
      if (integerTime < 0)
         integerTime += secondsInYear (--currentYear);
      else
         integerTime -= secondsInYear (currentYear++);
      
   } // end while
   
   // Get hours, minutes and seconds
   seconds      = integerTime % 60;
   integerTime /= 60;
   minutes      = integerTime % 60;
   integerTime /= 60;
   hours        = integerTime % 24;
   
   // Get the total number of days
   int theseDays = integerTime / 24;
   
   // Get month and day within the month
   int thisMonth = 0;
   while (theseDays >= daysInMonth (currentYear, thisMonth))
      theseDays -= daysInMonth (currentYear, thisMonth++);
   
   // Set the output values
   day   = theseDays + 1;
   month = thisMonth + 1;
   year  = currentYear;
   
}



//=================================================================
// Function: TimeUtils::getRelTimeComponents
//
// Description: This function returns the time components of a Julian time
//              specification in seconds. Note that if the time value is
//              negative then the flag negativeTime is set to TRUE.
//              The number of milli-seconds is only computed when the
//              TimeUtils are set to milli-second resolution, otherwise
//              the number of milli-seconds is set to zero and the
//              number of seconds is rounded off to the nearest second.
//=================================================================
void
TimeUtils::getRelTimeComponents (double relativeTime,
                                 bool &negativeTime,
                                 int &days,
                                 int &hours,
                                 int &minutes,
                                 int &seconds,
                                 int &milliSeconds,
                                 use_msecs_e useMsecs)
{
   // Convert time into an integer value in seconds
   int integerTime;
   if (useMsecs == TimeUtils::use_msecs_e::USE_MSECS) {
      integerTime = (int)relativeTime;
      if (relativeTime < 0.0) {
         milliSeconds = (int)(-1000.0 * (relativeTime - integerTime) + 0.5);
         if (milliSeconds == 1000) {
            integerTime--;
            milliSeconds = 0;
         }
      }
      else {
         milliSeconds = (int)(1000.0 * (relativeTime - integerTime) + 0.5);
         if (milliSeconds == 1000) {
            integerTime++;
            milliSeconds = 0;
         }
      }
   }
   else {   // no milli-second resolution
      if (relativeTime < 0.0)
         integerTime = (int)(relativeTime - 0.5);
      else
         integerTime = (int)(relativeTime + 0.5);
      milliSeconds = 0;
   }
   
   // Check if time is negative
   if (relativeTime < 0.0 && (integerTime != 0 || milliSeconds != 0)) {
      negativeTime = true;
      integerTime *= -1;
   }
   else
      negativeTime = false;
   
   // Get hours, minutes, seconds and days
   seconds      = integerTime % 60;
   integerTime /= 60;
   minutes      = integerTime % 60;
   integerTime /= 60;
   hours        = integerTime % 24;
   days         = integerTime / 24;
   
}



//=================================================================
// Function: TimeUtils::calendarToJulianDate
//
// Description: This function converts readable date components into
//              a Julian Date given with respect to Jan 1st, 2000 at
//              12:00:00 (in seconds). This function returns TRUE in
//              case of success and FALSE in case of an error.
//=================================================================
bool TimeUtils::calendarToJulianDate (int year, int month, int day, AGTime_t &julianDate)
{
   // Check the current year
   if (year <  (JULIAN_REF_YEAR - MAX_JULIAN_YEAR) ||
       year >= (JULIAN_REF_YEAR + MAX_JULIAN_YEAR))
      return false;   // year out of range
   
   // Check the month
   month--;
   if (month < 0 || month >= 12)
      return false;   // month out of range
   
   // Check the day within the month
   day--;
   if (day < 0 || day >= daysInMonth (year, month))
      return false;   // day number out of range
   
   // Get the number of days within the year
   int totalDays = 0;
   while (month > 0)
      totalDays += daysInMonth (year, --month);
   totalDays += day;
   
   // Calculate the time in seconds within the year
   julianDate = totalDays * AG_DAY2SECF;
   
   // Shift the time to the correct year
   while (year != JULIAN_REF_YEAR) {
   
      // Check if we have to go to previous or next year
      if (year < JULIAN_REF_YEAR)
         julianDate -= (AGTime_t)secondsInYear (year++);
      else
         julianDate += (AGTime_t)secondsInYear (--year);
      
   } // end while
   
   // UTC counts from 12:00 noon, so correct from 0:00
   julianDate -= AG_DAY2SEC2F;

   return true;
}

//=================================================================
// Function: TimeUtils::calendarToJulianDate
//
// Description: This function converts readable date components into
//              a Julian Date given with respect to Jan 1st, 2000 at
//              12:00:00 (in seconds). This function returns TRUE in
//              case of success and FALSE in case of an error.
//=================================================================
bool TimeUtils::yearDayToJulianDate(int year, int doy, AGTime_t& julianDate)
{
    // Check the current year
    if (year < (JULIAN_REF_YEAR - MAX_JULIAN_YEAR) ||
        year >= (JULIAN_REF_YEAR + MAX_JULIAN_YEAR))
        return false;   // year out of range

     // Check the day within the month
    doy--;
    if (doy < 0 || doy >= 366)
        return false;   // day number out of range

    // Calculate the time in seconds within the year
    julianDate = doy * AG_DAY2SECF;

    // Shift the time to the correct year
    while (year != JULIAN_REF_YEAR)
    {

        // Check if we have to go to previous or next year
        if (year < JULIAN_REF_YEAR)
            julianDate -= (AGTime_t)secondsInYear(year++);
        else
            julianDate += (AGTime_t)secondsInYear(--year);

    } // end while

    // UTC counts from 12:00 noon, so correct from 0:00
    julianDate -= AG_DAY2SEC2F;

    return true;
}



//=================================================================
// Function: TimeUtils::secondsInYear
//
// Description: This function calculates the number of seconds in the
//              given year taking into account leap-years.
//=================================================================
int
TimeUtils::secondsInYear (int theYear)
{
   int daysInYear = isLeapYear (theYear)? 366:365;

   return daysInYear * AG_DAY2SEC; // Calculate seconds in year
}



//=================================================================
// Function: TimeUtils::daysInMonth
//
// Description: This function calculates the number of days in the
//              given month taking into account leap-years.
//=================================================================
int TimeUtils::daysInMonth (int theYear, int theMonth)
{
   int daysInMonth = DAYS_IN_MONTH [theMonth];
   
   // Check for February, might be leap-year
   if (theMonth == 1 && isLeapYear (theYear))
   {
       daysInMonth++;
   }

   return daysInMonth;
}



//=================================================================
// Function: TimeUtils::isLeapYear
//
// Description: This function will check if the given year is a leap-year.
//=================================================================
bool TimeUtils::isLeapYear (int theYear)
{
   return ((theYear % 4) == 0 &&
          ((theYear % 100) != 0 || (theYear % 400) == 0));
}
