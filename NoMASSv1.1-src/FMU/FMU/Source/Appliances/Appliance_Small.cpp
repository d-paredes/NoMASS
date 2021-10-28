// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <algorithm>
#include <string>

#include <Configuration/Configuration.hpp>
#include <DataStore/DataStore.hpp>
#include <Utility/Utility.hpp>

#include "Appliance_Small.hpp"

//**********************************************************************

Appliance_Small::Appliance_Small() {}

void Appliance_Small::setup(ConfigStructAppliance a)
    {
    setID(a.id);
    setHoulyPriority(a.priority);
    model.setFolderLocation(Configuration::FolderSmallAppliance);
    model.readWeibullParameters(a.WeibullParameters);
    model.readStateProbabilities(a.StateProbabilities);
    model.readFractions(a.Fractions);
    model.readSumRatedPowers(a.SumRatedPowers);
    model.setRatedPowerAt(Utility::randomInt(0, 24));
    }

void Appliance_Small::step()
    {
    int stepcount = Configuration::getStepCount();
    setPower(model.consumption(stepcount));
    }

//**********************************************************************
