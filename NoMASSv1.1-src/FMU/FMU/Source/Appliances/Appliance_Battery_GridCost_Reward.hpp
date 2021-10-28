// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef APPLIANCE_BATTERY_GRIDCOST_REWARD_HPP_
#define APPLIANCE_BATTERY_GRIDCOST_REWARD_HPP_

#include <Appliances/Appliance_Battery.hpp>

//**********************************************************************

/**
 * @brief Battery Appliance class with reward calculated form the grid
 * @details The Battery appliance agent
 */
class Appliance_Battery_GridCost_Reward : public Appliance_Battery
    {
    public:
        Appliance_Battery_GridCost_Reward();

        double rewardFunction(double mostShortage, double binShortage) const;

    };

//**********************************************************************

#endif  // APPLIANCE_BATTERY_GRIDCOST_REWARD_HPP_
