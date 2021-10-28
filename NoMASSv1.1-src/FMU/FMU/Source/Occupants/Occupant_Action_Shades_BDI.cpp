// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <iostream>
#include <vector>

#include <Configuration/Configuration.hpp>
#include <DataStore/DataStore.hpp>
#include <Utility/Utility.hpp>

#include "Occupant_Action_Shades_BDI.hpp"

//**********************************************************************

Occupant_Action_Shades_BDI::Occupant_Action_Shades_BDI()
    {
    ShadeClosedDuringSleep = 0.0;
    ShadeClosedDuringWashing = 0.0;
    ShadeClosedDuringNight = 0.0;
    ShadeClosedDuringAudioVisual = 0.0;
    }

void Occupant_Action_Shades_BDI::setClosedDuringWashing(
    double ShadeClosedDuringWashing)
    {
    this->ShadeClosedDuringWashing = ShadeClosedDuringWashing;
    }

void Occupant_Action_Shades_BDI::setClosedDuringSleep(
    double ShadeClosedDuringSleep)
    {
    this->ShadeClosedDuringSleep = ShadeClosedDuringSleep;
    }

void Occupant_Action_Shades_BDI::setClosedDuringNight(
    double ShadeClosedDuringNight)
    {
    this->ShadeClosedDuringNight = ShadeClosedDuringNight;
    }
void Occupant_Action_Shades_BDI::setClosedDuringAudioVisual(
    double ShadeClosedDuringAudioVisual)
    {
    this->ShadeClosedDuringAudioVisual = ShadeClosedDuringAudioVisual;
    }

bool Occupant_Action_Shades_BDI::doRecipe(const std::vector<double> &activities)
    {
    bool bdi = false;
    int stepCount = Configuration::getStepCount();
    if (ShadeClosedDuringSleep > Utility::randomDouble(0, 1) &&
            activities.at(stepCount) == 0)
        {
        result = 0;
        bdi = true;
        }
    if (ShadeClosedDuringWashing > Utility::randomDouble(0, 1) &&
            activities.at(stepCount) == 6)
        {
        result = 0;
        bdi = true;
        }
    if (ShadeClosedDuringAudioVisual > Utility::randomDouble(0, 1) &&
            activities.at(stepCount) == 2)
        {
        result = 0;
        bdi = true;
        }

    if (ShadeClosedDuringNight > Utility::randomDouble(0, 1))
        {
        if (Lumint < 50)
            {
            result = 0;
            bdi = true;
            }
        }
    return bdi;
    }

//**********************************************************************
