// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <iostream>

#include "StateMachine.hpp"

//**********************************************************************

StateMachine::StateMachine() {}

unsigned int StateMachine::numberOfStates() const
    {
    return states.size();
    }

void StateMachine::addState(const State & s)
    {
    states.insert({s.getId(), s});
    }

bool StateMachine::hasState(const int stateID) const
    {
    bool found = states.end() != states.find(stateID) ;
    if (!found)
        {
        for (const auto & s : states)
            {
            found = s.second.hasState(stateID);
            if (found)
                {
                break;
                }
            }
        }
    return found;
    }

State StateMachine::transistionTo(const int stateID) const
    {
    std::unordered_map<int, State>::const_iterator si = states.find(stateID) ;
    State x;
    if (states.end() == si && hasState(stateID))
        {
        for (const auto & s : states)
            {
            if (s.second.hasState(stateID))
                {
                x = s.second.getState(stateID);
                break;
                }
            }
        }
    else
        {
        x = states.at(stateID);
        }
    return x;
    }

//**********************************************************************
