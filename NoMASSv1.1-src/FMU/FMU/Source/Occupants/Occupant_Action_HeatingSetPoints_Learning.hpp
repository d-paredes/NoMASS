// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef OCCUPANT_ACTION_HEATINGSETPOINTS_LEARNING_H
//#define OCCUPANT_ACTION_HEATINGSETPOINTS_LEARNING_H
#ifndef OCCUPANT_ACTION_HEATINGSETPOINTS_LEARNING_HPP_
#define OCCUPANT_ACTION_HEATINGSETPOINTS_LEARNING_HPP_

#include <memory>

#include <Occupants/Occupant_Action.hpp>
#include <QLearning/QLearning.hpp>

//**********************************************************************

/**
 * @brief
 * @details
 */

//**********************************************************************

class Occupant_Action_HeatingSetPoints_Learning : public Occupant_Action
    {
    public:
        Occupant_Action_HeatingSetPoints_Learning();
        void step(const Building_Zone& zone, const bool inZone);
        void setup(const int id, const int learn);
        void print();
        void reset();
        void setFile(std::string file);
    private:

        void parseConfiguration(const std::string &filename);
        int getState() const;

        QLearning qlWeekDay;
        QLearning qlWeekEnd;

        int learnId;
        int agentId;
        int previousHour;
        double setPoint;
        double steps;

        double pmv;
        bool hasBeenInZone;
        int pmv_name;
        int step_name;

        std::string file;
        std::vector<std::vector<int>> stateMappings;
    };

//**********************************************************************

//#endif // OCCUPANT_ACTION_HEATINGSETPOINTS_LEARNING_H
#endif // OCCUPANT_ACTION_HEATINGSETPOINTS_LEARNING_HPP_
