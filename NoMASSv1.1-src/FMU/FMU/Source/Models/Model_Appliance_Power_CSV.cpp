// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <string>

#include <Utility/Utility.hpp>

#include "Model_Appliance_Power_CSV.hpp"

//**********************************************************************

Model_Appliance_Power_CSV::Model_Appliance_Power_CSV() {}

void Model_Appliance_Power_CSV::parseConfiguration(
    const std::string & filename)
    {
    profile = Utility::csvToTable<double>(filename, false);
    }

double Model_Appliance_Power_CSV::power(const int dayOfYear,
                                        const int minuteOfday)
    {
    return profile[minuteOfday][dayOfYear];
    }

//**********************************************************************
