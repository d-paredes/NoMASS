// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef OCCUPANT_ACTION_HEAT_GAINS_HPP_
#define OCCUPANT_ACTION_HEAT_GAINS_HPP_

#include <string>

#include <Occupants/Occupant_Action.hpp>

//**********************************************************************

/**
 * @brief Occupant action of heat gains
 * @details Occupant action of heat gains
 */

//**********************************************************************

class Occupant_Action_Heat_Gains : public Occupant_Action
    {
    public:
        Occupant_Action_Heat_Gains();
        void prestep(double clo, double metabolicRate);
        void step(const Building_Zone& zone, const bool inZone);
        void setup(int buildingID, int agentid);
        double getPMV() const;
        double getPPD() const;

    private:
        int id;
        int buildingID;
        double clo;
        double metabolicRate;
        double ppd;
        double pmv;

        int datastoreIdMetabolicRate;
        int datastoreIdClo;
        int datastoreIdPpd;
        int datastoreIdPmv;
        int datastoreIdPmvAirTemp;
        int datastoreIdPmvAirHumid;
        int datastoreIdPmvMeanRadient;
        int datastoreIdPmvSetpoint;
    };

//**********************************************************************

#endif  // OCCUPANT_ACTION_HEAT_GAINS_HPP_
