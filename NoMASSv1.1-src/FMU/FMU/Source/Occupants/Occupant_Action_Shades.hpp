// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef FMU_SOURCE_OCCUPANT_ACTION_SHADES_HPP_
//#define FMU_SOURCE_OCCUPANT_ACTION_SHADES_HPP_
#ifndef OCCUPANT_ACTION_SHADES_HPP_
#define OCCUPANT_ACTION_SHADES_HPP_

#include <vector>

#include <Models/Model_ExternalShading.hpp>
#include <Occupants/Occupant_Action.hpp>

//**********************************************************************

/**
 * @brief Occupant action on shades
 * @details Occupant action on shades
 */

//**********************************************************************

class Occupant_Action_Shades : public Occupant_Action
    {
    public:
        Occupant_Action_Shades();
        void setup(int windowID);
        void setIndoorIlluminance(const float lumint);
        void step(const Building_Zone& zone, const bool inZone,
                  const bool previouslyInZone);

    protected:
        float Lumint = 0;

    private:
        Model_ExternalShading m_blindUsage;

    };

//**********************************************************************

//#endif  // FMU_SOURCE_OCCUPANT_ACTION_SHADES_HPP_
#endif  // OCCUPANT_ACTION_SHADES_HPP_
