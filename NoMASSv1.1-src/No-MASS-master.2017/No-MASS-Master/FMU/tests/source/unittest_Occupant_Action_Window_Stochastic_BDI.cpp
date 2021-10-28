// Copyright 2015 Jacob Chapman

#include <limits.h>
#include <vector>

#include "tests/Gen.hpp"
#include "DataStore.hpp"
#include "Occupant_Action_Window_Stochastic_BDI.hpp"
#include "Utility.hpp"
#include "gtest/gtest.h"

class Test_Occupant_Action_Window_Stochastic_BDI : public ::testing::Test {
 protected:
    Occupant_Action_Window_Stochastic_BDI aaw;

    std::vector<double> activities;
    virtual void SetUp();
};

void Test_Occupant_Action_Window_Stochastic_BDI::SetUp() {
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

TEST_F(Test_Occupant_Action_Window_Stochastic_BDI, Arrival) {
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

  aaw.setOpenDuringCooking(false);
  aaw.setOpenDuringWashing(false);

    
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

TEST_F(Test_Occupant_Action_Window_Stochastic_BDI, OpenWindowDuringCooking) {
  ConfigStructZone zs;
  zs.name = "Block1:Kitchen";
  zs.id = 1;
  Building_Zone z_Kitchen;
  z_Kitchen.setName(zs.name);
  z_Kitchen.setActive(true);
  z_Kitchen.setup(zs);
  aaw.setOpenDuringCooking(true);

  activities.push_back(4);
  aaw.step(z_Kitchen, true, false, activities);
  aaw.doRecipe(activities);
  EXPECT_EQ(aaw.getResult(), 1);

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  aaw.doRecipe(activities);
  EXPECT_EQ(aaw.getResult(), 0);
}

TEST_F(Test_Occupant_Action_Window_Stochastic_BDI, OpenWindowAfterShower) {
  ConfigStructZone zs;
  zs.name = "Block1:Kitchen";
  zs.id = 1;
  Building_Zone z_Kitchen;
  z_Kitchen.setName(zs.name);
  z_Kitchen.setActive(true);
  z_Kitchen.setup(zs);
  aaw.setOpenDuringWashing(true);
  aaw.getResult();

  activities.push_back(6);
  aaw.step(z_Kitchen, true, false, activities);
  aaw.doRecipe(activities);
  EXPECT_EQ(aaw.getResult(), 0);

  Configuration::step();
  activities.push_back(6);
  aaw.step(z_Kitchen, true, false, activities);
  aaw.doRecipe(activities);
  EXPECT_EQ(aaw.getResult(), 0);

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  aaw.doRecipe(activities);
  EXPECT_EQ(aaw.getResult(), 1);

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  aaw.doRecipe(activities);
  EXPECT_EQ(aaw.getResult(), 0);
}



TEST_F(Test_Occupant_Action_Window_Stochastic_BDI, OpenWindowAfterShower2) {
  DataStore::addVariable("Block2:BathroomZoneMeanAirTemperature");
  DataStore::addVariable("Block2:BathroomZoneAirRelativeHumidity");
  DataStore::addVariable("Block2:BathroomZoneMeanRadiantTemperature");

  DataStore::addValueS("Block2:BathroomZoneMeanAirTemperature", 18);
  DataStore::addValueS("Block2:BathroomZoneAirRelativeHumidity", 18);
  DataStore::addValueS("Block2:BathroomZoneMeanRadiantTemperature", 18);


  ConfigStructZone zs;
  zs.name = "Block1:Kitchen";
  zs.id = 1;
  zs.activities = {1, 2, 3};
  Building_Zone z_Kitchen;
  z_Kitchen.setName(zs.name);
  z_Kitchen.setActive(true);
  z_Kitchen.setIDString(zs.name);
  z_Kitchen.setup(zs);
  zs.name = "Block2:Bathroom";
  zs.id = 2;
  zs.activities = {6};
  Building_Zone z_Bath;
  z_Bath.setName(zs.name);
  z_Bath.setActive(true);
  z_Bath.setIDString(zs.name);
  z_Bath.setup(zs);

  Occupant_Action_Window_Stochastic_BDI aab;
  if (z_Kitchen.hasActivity(6)) {
    aaw.setOpenDuringWashing(true);
  }
  if (z_Bath.hasActivity(6)) {
    aab.setOpenDuringWashing(true);
  }

  aaw.getResult();
  aab.getResult();

  activities.push_back(6);
  aaw.step(z_Kitchen, true, false, activities);
  aaw.doRecipe(activities);
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.getResult(), 0);
  aab.step(z_Bath, true, false, activities);
  EXPECT_FALSE(aab.doRecipe(activities));
  EXPECT_EQ(aab.getResult(), 0);

  Configuration::step();
  activities.push_back(6);
  aaw.step(z_Kitchen, true, false, activities);
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.getResult(), 0);
  aab.step(z_Bath, true, false, activities);
  EXPECT_FALSE(aab.doRecipe(activities));
  EXPECT_EQ(aab.getResult(), 0);

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.getResult(), 0);
  aab.step(z_Bath, true, false, activities);
  EXPECT_TRUE(aab.doRecipe(activities));
  EXPECT_EQ(aab.getResult(), 1);

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.getResult(), 0);
  aab.step(z_Bath, true, false, activities);
  EXPECT_TRUE(aab.doRecipe(activities));
  EXPECT_EQ(aab.getResult(), 0);


  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.getResult(), 0);
  aab.step(z_Bath, true, false, activities);
  EXPECT_FALSE(aab.doRecipe(activities));
  EXPECT_EQ(aab.getResult(), 0);

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.getResult(), 0);
  aab.step(z_Bath, true, false, activities);
  EXPECT_FALSE(aab.doRecipe(activities));
  EXPECT_EQ(aab.getResult(), 0);
}

TEST_F(Test_Occupant_Action_Window_Stochastic_BDI, multiZone) {
  DataStore::addValueS("EnvironmentSiteOutdoorAirDrybulbTemperature", 23);
  DataStore::addValueS("Block1:KitchenZoneMeanAirTemperature", 26);
  DataStore::addValueS("Block1:KitchenZoneAirRelativeHumidity", 50);
  DataStore::addValueS("Block1:KitchenZoneMeanRadiantTemperature", 23);

  ConfigStructZone zs;
  zs.name = "Block1:Kitchen";
  zs.id = 1;
  zs.activities = {1, 2, 3};
  Building_Zone z_Kitchen;
  z_Kitchen.setName(zs.name);
  z_Kitchen.setActive(true);
  z_Kitchen.setup(zs);

  aaw.getResult();

  for (int i = 0; i < 100; i++) {
    activities.push_back(0);
    aaw.step(z_Kitchen, false, false, activities);
    z_Kitchen.setWindowState(aaw.getResult());
    EXPECT_FALSE(aaw.doRecipe(activities));
    EXPECT_EQ(aaw.getResult(), 0);
  }

  while (aaw.getResult() == 0 || aaw.durationOpen() < 1000) {
    Configuration::step();
    activities.push_back(1);
    aaw.step(z_Kitchen, true, false, activities);
    z_Kitchen.setWindowState(aaw.getResult());
    EXPECT_FALSE(aaw.doRecipe(activities));
  }
  EXPECT_EQ(aaw.getResult(), 1);
  EXPECT_EQ(aaw.durationOpen(), 1007);

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, true, activities);
  z_Kitchen.setWindowState(aaw.getResult());
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.durationOpen(), 1002);
  EXPECT_EQ(aaw.getResult(), 1);

  Configuration::step();
  activities.push_back(2);
  aaw.step(z_Kitchen, true, true, activities);
  z_Kitchen.setWindowState(aaw.getResult());
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.durationOpen(), 997);
  EXPECT_EQ(aaw.getResult(), 1);
  int prevDuration =  aaw.durationOpen();
  while (aaw.durationOpen() > 0) {
    Configuration::step();
    activities.push_back(2);
    aaw.step(z_Kitchen, true, true, activities);
    z_Kitchen.setWindowState(aaw.getResult());
    EXPECT_FALSE(aaw.doRecipe(activities));
    prevDuration = prevDuration - 5;
    if (prevDuration < 0 ) prevDuration = 0;
    EXPECT_EQ(aaw.durationOpen(), prevDuration);
    if (prevDuration > 0) {
      EXPECT_EQ(aaw.getResult(), 1);
    } else {
      EXPECT_EQ(aaw.getResult(), 0);
    }
  }

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.getResult(), 0);

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.getResult(), 0);

  Configuration::step();
  activities.push_back(1);
  aaw.step(z_Kitchen, true, false, activities);
  EXPECT_FALSE(aaw.doRecipe(activities));
  EXPECT_EQ(aaw.getResult(), 0);
}
