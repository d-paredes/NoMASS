// Copyright 2015 Jacob Chapman

#include <limits.h>
#include <vector>

#include "tests/Gen.hpp"
#include "DataStore.hpp"
#include "Occupant_Action_Window_Stochastic.hpp"
#include "Utility.hpp"
#include "gtest/gtest.h"

class Test_Occupant_Action_Window_Stochastic : public ::testing::Test {
 protected:
    Occupant_Action_Window_Stochastic aaw;

    std::vector<double> activities;
    virtual void SetUp();
};

void Test_Occupant_Action_Window_Stochastic::SetUp() {
  Configuration::reset();
  Configuration::parseConfiguration(testFiles + "/SimulationConfig2.xml");

  Configuration::setStepCount(0);
  Configuration::info.windows = false;
  Configuration::info.shading = false;
  Configuration::info.lights = false;
  Configuration::info.timeStepsPerHour = 12;
  DataStore::addVariable("Block1:KitchenZoneMeanAirTemperature");
  DataStore::addVariable("Block1:KitchenZoneAirRelativeHumidity");
  DataStore::addVariable("Block1:KitchenZoneMeanRadiantTemperature");
  DataStore::addVariable("EnvironmentSiteOutdoorAirDrybulbTemperature");

  DataStore::addValueS("EnvironmentSiteOutdoorAirDrybulbTemperature", 0);
  DataStore::addValueS("Block1:KitchenZoneMeanAirTemperature", 18);
  DataStore::addValueS("Block1:KitchenZoneAirRelativeHumidity", 18);
  DataStore::addValueS("Block1:KitchenZoneMeanRadiantTemperature", 18);
  activities.clear();
}

TEST_F(Test_Occupant_Action_Window_Stochastic, Arrival) {
  Utility::setSeed(1);

  ConfigStructZone zs;
  zs.name = "Block1:Kitchen";
  zs.id = 1;
  Building_Zone z_Kitchen;
  z_Kitchen.setName(zs.name);
  z_Kitchen.setActive(true);
  z_Kitchen.setup(zs);
  z_Kitchen.setWindowState(0);
  DataStore::addValueS("EnvironmentSiteOutdoorAirDrybulbTemperature", 10);
  DataStore::addValueS("Block1:KitchenZoneMeanAirTemperature", 35);

  for (int i =0; i < 7200; i++) {
    activities.push_back(4);
  }
  for (int i =0; i < 2; i++) {
    aaw.step(z_Kitchen, true, false, activities);
    EXPECT_FALSE(aaw.getResult());
  }

  // aaw.step(z_Kitchen, true, false, activities);
  // EXPECT_TRUE( aaw.getResult());
}
