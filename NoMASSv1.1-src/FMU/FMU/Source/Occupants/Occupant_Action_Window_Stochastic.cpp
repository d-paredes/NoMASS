// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <vector>
#include <iostream>

#include <Configuration/Configuration.hpp>
#include <DataStore/DataStore.hpp>
#include <Environment/Environment.hpp>
#include <Utility/Utility.hpp>

#include "Occupant_Action_Window_Stochastic.hpp"

//**********************************************************************

Occupant_Action_Window_Stochastic::Occupant_Action_Window_Stochastic()
    {
    }

void Occupant_Action_Window_Stochastic::setup(int windowID, int id)
    {
	//LOG << "     void Occupant_Action_Window_Stochastic::setup(" << windowID << ", " << id << ")" << "\n";
    ConfigStructWindow ws = Configuration::windows.at(windowID);
	//LOG << "        step 1" << "\n";
    m_window.setDurationVars(ws.aop, ws.bopout, ws.shapeop);
	//LOG << "        step 2" << "\n";
	m_window.setArrivalVars(ws.a01arr, ws.b01inarr, ws.b01outarr,
                            ws.b01absprevarr, ws.b01rnarr);
	//LOG << "        step 3" << "\n";
	m_window.setInterVars(ws.a01int, ws.b01inint, ws.b01outint,
                          ws.b01presint, ws.b01rnint);
	//LOG << "        step 4" << "\n";
	m_window.setDepartureVars(ws.a01dep, ws.b01outdep, ws.b01absdep,
                              ws.b01gddep, ws.a10dep, ws.b10indep, ws.b10outdep, ws.b10absdep,
                              ws.b10gddep);

	//LOG << "        step 5" << "\n";
	variableNameWindowDesire = DataStore::addVariable("Occupant_Window_Desire_"
                               + std::to_string(id) + "_"
                               + std::to_string(windowID));
	//LOG << "        step 6" << "\n";
    }

void Occupant_Action_Window_Stochastic::step(const Building_Zone& zone,
        const bool inZone,
        const bool previouslyInZone, const std::vector<double> &activities)
    {
    double outdoorTemperature = Environment::getOutdoorAirDrybulbTemperature();

    // double rain = DataStore::getValue("EnvironmentSiteRainStatus");
    double rain = 0;
    double indoorTemperature = zone.getMeanAirTemperature();
    double timeStepLengthInMinutes = Configuration::lengthOfTimestep() / 60;

    m_window.setWindowState(zone.getWindowState());
    if (m_window.getWindowState() == 0)
        {
        m_window.setDurationOpen(0);
        }
    if (inZone && !previouslyInZone)
        {
        double previousDuration = getPreviousDurationOfAbsenceState(activities);
        m_window.arrival(indoorTemperature,
                         outdoorTemperature, previousDuration, rain, timeStepLengthInMinutes);
        }
    else if (inZone && previouslyInZone)
        {
        double currentDuration = getCurrentDurationOfPresenceState(activities);
        m_window.intermediate(indoorTemperature,
                              outdoorTemperature, currentDuration, rain, timeStepLengthInMinutes);
        }
    else if (!inZone && previouslyInZone)
        {
        double groundFloor = zone.getGroundFloor();
        double futureDuration = getFutureDurationOfAbsenceState(activities);
        m_window.departure(
            indoorTemperature, dailyMeanTemperature, futureDuration, groundFloor);
        }
    result = m_window.getWindowState();
    }

//**********************************************************************
