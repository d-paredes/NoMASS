// Undefined description of file -- Jacob Chapman -- 201X
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef OCCUPANT_ACTION_WINDOW_LEARNING_H
//#define OCCUPANT_ACTION_WINDOW_LEARNING_H
#ifndef OCCUPANT_ACTION_WINDOW_LEARNING_HPP_
#define OCCUPANT_ACTION_WINDOW_LEARNING_HPP_

#include <memory>

#include <Building/Building_Zone.hpp>
#include <Models/Model_Windows.hpp>
#include <Occupants/Occupant_Action_Window.hpp>
#include <QLearning/QLearning.hpp>

//**********************************************************************

/**
 * @brief Occupant action on windows using Q-Learing model
 * @details Occupant action on windows using Q-Learing model
 */

//**********************************************************************

class Occupant_Action_Window_Learning : public Occupant_Action_Window
    {
    public:
        Occupant_Action_Window_Learning();
        void setup(const int id);
        void step(const Building_Zone& zone, const bool inZone,
                  const bool previouslyInZone);
        void print();
        void reset();

    private:
        QLearning learn;
        int window_name;
    };

//**********************************************************************

//#endif // OCCUPANT_ACTION_WINDOW_LEARNING_H
#endif // OCCUPANT_ACTION_WINDOW_LEARNING_HPP_
