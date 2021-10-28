// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef ENVIRONMENT_HPP_
#define ENVIRONMENT_HPP_

#include <deque>

//**********************************************************************

/**
 * @brief Stores environmental parameters
 * @details Stores environmental parameters such as external weather conditions
 */
class Environment
    {
    public:
        static double dailyMeanTemperature;
        static void calculateDailyMeanTemperature();
        static double getDailyMeanTemperature();
        static double getEVG();
        static double getOutdoorAirDrybulbTemperature();

    private:
        static std::deque<double> outDoorTemperatures;
        Environment();
    };

//**********************************************************************

#endif  // ENVIRONMENT_HPP_
