// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <string>

#include <Configuration/Configuration.hpp>
#include <DataStore/DataStore.hpp>
#include <Environment/Environment.hpp>

#include "Occupant_Action_Window_Learning.hpp"

//**********************************************************************

Occupant_Action_Window_Learning::Occupant_Action_Window_Learning() {}

void Occupant_Action_Window_Learning::print()
    {
    learn.printQ();
    }
void Occupant_Action_Window_Learning::reset()
    {
    learn.reset();
    }

void Occupant_Action_Window_Learning::setup(const int id)
    {
    variableNameWindowDesire = DataStore::addVariable("Occupant_Window_Desire_"
                               + std::to_string(id));

    std::string zoneIdStr = std::to_string(zoneId);
    learn.setFilename("window-" + zoneIdStr + "-");
    learn.setStates(400);
    learn.setActions(2);
    learn.setId(id);
    learn.setUpdate(Configuration::info.learn);
    learn.setEpsilon(Configuration::info.learnep);
    learn.setup();
    window_name =
        DataStore::addVariable("Weekday-" + zoneIdStr + "-_pmv" + std::to_string(id));
    result = 0;
    }

void Occupant_Action_Window_Learning::step(const Building_Zone& zone,
        const bool inZone, const bool previouslyInZone)
    {
    if (inZone || previouslyInZone)
        {
        double pmv = reward;
        int temp = zone.getMeanAirTemperature();
        int outdoorTemperature = Environment::getOutdoorAirDrybulbTemperature();
        if (temp > 29) temp = 29;
        if (temp < 10) temp = 10;
        temp = temp -10;
        if (outdoorTemperature > 29) outdoorTemperature = 29;
        if (outdoorTemperature < 10) outdoorTemperature = 10;
        outdoorTemperature = outdoorTemperature - 10;

        int state = (temp * 20) + outdoorTemperature;

        learn.setState(state);
        int winState = zone.getWindowState();
        reward = 0;
        if (winState == 1 && pmv > 0.5)
            {
            reward = 0.1;
            }
        if (winState == 0 && pmv > 0.5)
            {
            reward = -0.1;
            }
        if (winState == 1 && pmv < -0.5)
            {
            reward = -0.1;
            }
        if (winState == 0 && pmv < -0.5)
            {
            reward = 0.1;
            }

        DataStore::addValue(window_name, pmv);

        learn.setAction(zone.getWindowState());
        learn.setReward(reward);
        learn.learn();
        result = learn.getAction();
        }
    }

//**********************************************************************
