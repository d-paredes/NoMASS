// Undefined description of file -- Jacob Chapman -- 201X
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef Occupant_ACTION_WINDOW_STOCHASTIC_H
//#define Occupant_ACTION_WINDOW_STOCHASTIC_H
#ifndef OCCUPANT_ACTION_WINDOW_STOCHASTIC_HPP_
#define OCCUPANT_ACTION_WINDOW_STOCHASTIC_HPP_

#include <Building/Building_Zone.hpp>
#include <Models/Model_Windows.hpp>
#include <Occupants/Occupant_Action_Window.hpp>

//**********************************************************************

/**
 * @brief Occupant action on windows using stochastic model
 * @details Occupant action on windows using stochastic model
 */

//**********************************************************************

class Occupant_Action_Window_Stochastic : public Occupant_Action_Window
    {
    public:
        Occupant_Action_Window_Stochastic();
        void setup(int windowID, int id);
        void step(const Building_Zone& zone, const bool inZone,
                  const bool previouslyInZone,
                  const std::vector<double> &activities);
    };

//**********************************************************************

//#endif // Occupant_ACTION_WINDOW_STOCHASTIC_H
#endif // OCCUPANT_ACTION_WINDOW_STOCHASTIC_HPP_
