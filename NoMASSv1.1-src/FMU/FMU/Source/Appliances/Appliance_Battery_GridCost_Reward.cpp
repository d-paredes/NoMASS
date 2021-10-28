// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <Simulation/Simulation.hpp>

#include "Appliance_Battery_GridCost_Reward.hpp"

//**********************************************************************

Appliance_Battery_GridCost_Reward::Appliance_Battery_GridCost_Reward() {}

double Appliance_Battery_GridCost_Reward::rewardFunction(double mostShortage,
        double binShortage) const
    {
    double gridCost = Simulation::getGridCost();
    double x = binShortage / mostShortage;
    double ret = x / gridCost;
    if (action)
        {
        if (x > 0.7)
            {
            ret = x * gridCost;
            }
        else
            {
            ret = -x / gridCost;
            }
        }
    else
        {
        if (x > 0.7)
            {
            ret = -x * gridCost;
            }
        }
    return ret;
    }

//**********************************************************************
