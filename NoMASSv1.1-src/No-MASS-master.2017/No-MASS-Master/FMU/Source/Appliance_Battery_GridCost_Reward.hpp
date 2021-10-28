// Copyright 2016 Jacob Chapman

#ifndef APPLIANCE_BATTERY_GRIDCOST_REWARD_H_
#define APPLIANCE_BATTERY_GRIDCOST_REWARD_H_

#include "Appliance_Battery.hpp"

/**
 * @brief Battery Appliance class with reward calculated form the grid
 * @details The Battery appliance agent
 */

class Appliance_Battery_GridCost_Reward : public Appliance_Battery {
 public:
  Appliance_Battery_GridCost_Reward();

  double rewardFunction(double mostShortage, double binShortage) const;

};

#endif  // APPLIANCE_BATTERY_GRIDCOST_REWARD_H_
