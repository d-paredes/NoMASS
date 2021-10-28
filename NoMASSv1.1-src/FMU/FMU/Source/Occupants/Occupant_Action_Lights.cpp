// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <vector>

#include <Models/Model_Lights.hpp>
#include <Utility/Utility.hpp>

#include "Occupant_Action_Lights.hpp"

//**********************************************************************

Occupant_Action_Lights::Occupant_Action_Lights() {}

void Occupant_Action_Lights::step(const Building_Zone& zone, const bool inZone,
                                  const bool previouslyInZone, const std::vector<double> &activities)
    {

    float Lumint = zone.getDaylightingReferencePoint1Illuminance();
    bool lightState = zone.getLightState();
    Model_Lights m_lightUsage;

    if (inZone && !previouslyInZone)
        {
        lightState = m_lightUsage.arrival(lightState, Lumint);
        }
    else if (inZone && previouslyInZone)
        {
        lightState = m_lightUsage.intermediate(lightState, Lumint);
        }
    else if (!inZone && previouslyInZone)
        {
        int pffs = getFutureDurationOfAbsenceState(activities);
        lightState = m_lightUsage.departure(lightState, pffs);
        }
    result = lightState;
    }

//**********************************************************************
