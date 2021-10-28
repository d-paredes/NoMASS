// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef OCCUPANT_ACTION_WINDOW_HPP_
#define OCCUPANT_ACTION_WINDOW_HPP_

#include <Building/Building_Zone.hpp>
#include <Models/Model_Windows.hpp>
#include <Occupants/Occupant_Action.hpp>

//**********************************************************************

/**
 * @brief Occupant action on windows
 * @details Occupant action on windows
 */

//**********************************************************************

class Occupant_Action_Window : public Occupant_Action
    {
    public:
        Occupant_Action_Window();
        void setup(int windowID, int id);
        void setDailyMeanTemperature(double dailyMeanTemperature);
        void saveResult();
        int durationOpen() const;

    protected:
        Model_Windows m_window;
        int variableNameWindowDesire;
        double dailyMeanTemperature;
    };

//**********************************************************************

#endif  // OCCUPANT_ACTION_WINDOW_HPP_
