// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef AGENT_HPP_
#define AGENT_HPP_

#include <string>

//**********************************************************************

/**
 * @brief The Agent
 * @details Contains all information about the Agents
 */
class Agent
    {
    public:
        Agent();
        void setup();
        void step();
        void postprocess();
        void preprocess();
        void postTimeStep();
        void setBuildingID(const int id);
        void setIDString(const std::string & idString);
        void setID(const int id);
        int getID() const;
        int getBuildingID() const;

    protected:
        int buildingID;
        int id;
        std::string idString;
    };

//**********************************************************************

#endif  // AGENT_HPP_
