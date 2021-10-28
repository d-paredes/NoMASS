// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <vector>

#include <Utility/Utility.hpp>

#include "Occupant_Action_Appliance_BDI.hpp"

//**********************************************************************

Occupant_Action_Appliance_BDI::Occupant_Action_Appliance_BDI()
    {
    ApplianceDuringDay = 0.0;
    }

void Occupant_Action_Appliance_BDI::setApplianceDuringDay(
    double ApplianceDuringDay)
    {
    this->ApplianceDuringDay = ApplianceDuringDay;
    }

bool Occupant_Action_Appliance_BDI::doRecipe(
    const std::vector<double> &activities)
    {
    bool bdi = false;
    if (ApplianceDuringDay > 0)
        {
        bdi = true;
        result = 0;
        int stepCount = Configuration::getStepCount();
        if (stepCount == 0)
            {
            first = -1;
            last = -1;
            }
        if (last < stepCount)
            {
            calculateFirstLastCouts(activities);
            }
        if (ApplianceDuringDay > Utility::randomDouble(0, 1))
            {
            if (stepCount >= first && stepCount <= last)
                {
                result = 1;
                }
            }
        }
    return bdi;
    }

void Occupant_Action_Appliance_BDI::calculateFirstLastCouts(
    const std::vector<double> &activities)
    {
    int stepCount = Configuration::getStepCount();
    if (stepCount > first)
        {
        int hour = (stepCount * Configuration::lengthOfTimestep()) / 3600;
        int day = hour / 24;
        int dayCounter = day;
        int counter = stepCount;

        while (stepCount > first)
            {
            if (activities[counter] < 9)
                {
                first = counter;
                break;
                }
            counter++;
            }
        while (day == dayCounter)
            {
            if (activities[counter] < 9)
                {
                last = counter;
                }
            hour = (counter * Configuration::lengthOfTimestep()) / 3600;
            dayCounter = hour / 24;
            counter++;
            }
        }
    }
