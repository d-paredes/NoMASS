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

#include "Occupant_Action_Window.hpp"

//**********************************************************************

Occupant_Action_Window::Occupant_Action_Window()
    {
    }

void Occupant_Action_Window::setDailyMeanTemperature(
    double dailyMeanTemperature)
    {
    this->dailyMeanTemperature = dailyMeanTemperature;
    }

void Occupant_Action_Window::setup(int windowID, int id)
    {
    variableNameWindowDesire = DataStore::addVariable("Occupant_Window_Desire_"
                               + std::to_string(id) + "_"
                               + std::to_string(windowID));
    }

void Occupant_Action_Window::saveResult()
    {
    DataStore::addValue(variableNameWindowDesire, result);
    }

int Occupant_Action_Window::durationOpen() const
    {
    return m_window.getDurationOpen();
    }

//**********************************************************************
