// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef STATE_HPP_
#define STATE_HPP_

#include <memory>
#include <string>
#include <vector>

#include <Building/Building_Zone.hpp>

//**********************************************************************

/**
* @brief The state of an occupant
* @details The state of an occupant based on the activity model
*/

//**********************************************************************

class State
    {
    public:
        State();
        State(int id, double metabolicRate, double clo, const std::string & activity);
        virtual ~State();
        virtual bool hasState(const int stateID) const;
        virtual State getState(const int stateID) const;

        void addState(State s);
        void setZonePtr(std::shared_ptr<Building_Zone> zoneptr);
        int getId() const;
        void setId(int id);
        void setActivity(const std::string & activity);
        void setMetabolicRate(double metabolicRate);
        void setClo(double clo);
        unsigned int numberOfSubStates() const;
        double getMetabolicRate() const;
        double getClo() const;
        bool isInActivity(const std::string & activity) const;
        std::shared_ptr<Building_Zone> getZonePtr() const;

    protected:
        int id;
        double metabolicRate;
        double clo;
        std::string activity;
        std::vector<State> states;
        std::shared_ptr<Building_Zone> zone;
    };

//**********************************************************************

#endif  // STATE_HPP_
