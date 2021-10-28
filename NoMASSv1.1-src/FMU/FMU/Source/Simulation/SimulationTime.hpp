// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef SIMULATIONTIME_HPP_
#define SIMULATIONTIME_HPP_

#include <vector>

//**********************************************************************

/**
 * @brief Keeps track of time
 * @details Keeps track of time
 */

//**********************************************************************

class SimulationTime
    {
    public:
        static void preprocess();
        static void trackTime();
        static void reset();

        static int stepCount;
        static int databaseIdStepCount;
        static int minute;
        static int databaseIdMinute;
        static int hour;
        static int databaseIdHour;
        static int day;
        static int databaseIdDay;
        static int month;
        static int databaseIdMonth;
        static int hourOfDay;
        static int databaseIdHourOfDay;
        static int minuteOfDay;
        static int databaseIdMinuteOfDay;

    private:
        static std::vector<int> monthCount;
        SimulationTime();
    };

//**********************************************************************

#endif  // SIMULATIONTIME_HPP_
