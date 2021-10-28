// Undefined description of file -- Jacob Chapman -- 201X
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef STATEMACHINE_H
//#define STATEMACHINE_H
#ifndef STATEMACHINE_HPP_
#define STATEMACHINE_HPP_

#include <unordered_map>

#include <Simulation/State.hpp>

//**********************************************************************

/**
* @brief Moves an agent into a different state
* @details Moves an agent into a different state
*/

//**********************************************************************

class StateMachine
    {
    public:
        StateMachine();
        void addState(const State & s);
        bool hasState(const int stateID) const;
        unsigned int numberOfStates() const;
        State transistionTo(const int stateID) const;

    private:
        std::unordered_map<int, State> states;
    };

//**********************************************************************

//#endif // STATEMACHINE_H
#endif // STATEMACHINE_HPP_
