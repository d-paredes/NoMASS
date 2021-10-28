// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef OCCUPANT_ACTION_HPP_
#define OCCUPANT_ACTION_HPP_

#include <vector>

#include <Building/Building_Zone.hpp>

//**********************************************************************

/**
 * @brief Occupant action super class
 * @details Occupant action super class
 */

//**********************************************************************

class Occupant_Action
    {
    public:
        Occupant_Action();

        void setAvailableActivities(const std::vector<int> &availableActivities);
        void setZoneId(const double zoneId);
        void setReward(const double reward);
        double getResult() const;
        double getFutureDurationOfAbsenceState(
            const std::vector<double> &activities) const;
        double getPreviousDurationOfAbsenceState(
            const std::vector<double> &activities) const;
        double getCurrentDurationOfPresenceState(
            const std::vector<double> &activities) const;

    protected:
        bool activityAvailable(const int act) const;
        double result;
        double reward;
        std::vector<int> availableActivities;
        int zoneId;
    };

//**********************************************************************

#endif  // OCCUPANT_ACTION_HPP_
