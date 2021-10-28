// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef FMU_SOURCE_OCCUPANT_ACTION_LIGHTS_HPP_
//#define FMU_SOURCE_OCCUPANT_ACTION_LIGHTS_HPP_
#ifndef OCCUPANT_ACTION_LIGHTS_HPP_
#define OCCUPANT_ACTION_LIGHTS_HPP_

#include <vector>

#include <Occupants/Occupant_Action.hpp>

//**********************************************************************

/**
 * @brief Occupant action on lights
 * @details Occupant action on lights
 */

//**********************************************************************

class Occupant_Action_Lights : public Occupant_Action
    {
    public:
        Occupant_Action_Lights();
        void step(const Building_Zone& zone, const bool inZone,
                  const bool previouslyInZone,
                  const std::vector<double> &activities);
    };

//**********************************************************************

//#endif  // FMU_SOURCE_OCCUPANT_ACTION_LIGHTS_HPP_
#endif  // OCCUPANT_ACTION_LIGHTS_HPP_
