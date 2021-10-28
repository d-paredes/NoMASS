// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef MODEL_APPLIANCE_POWER_CSV_HPP_
#define MODEL_APPLIANCE_POWER_CSV_HPP_

#include <string>
#include <vector>

//**********************************************************************

/**
 * @brief Appliance modeled from a CSV file
 * @details Models appliance useage at each timestep from a CSV file
 */

//**********************************************************************

class Model_Appliance_Power_CSV
    {
    public:
        Model_Appliance_Power_CSV();
        void parseConfiguration(const std::string & filename);
        double power(const int dayOfYear, const int minuteOfday);
    private:
        std::vector<std::vector<double>> profile;
    };

//**********************************************************************

#endif  // MODEL_APPLIANCE_POWER_CSV_HPP_
