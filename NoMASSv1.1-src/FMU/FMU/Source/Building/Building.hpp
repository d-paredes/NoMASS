// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef BUILDING_HPP_
#define BUILDING_HPP_

#include <string>
#include <vector>

#include <Building/Building_Appliances.hpp>
#include <Building/Building_Zone.hpp>
#include <Configuration/Configuration.hpp>
#include <Occupants/Occupant.hpp>

//**********************************************************************

/**
 * @brief A Building
 * @details A Building
 */
class Building
    {
    public:
        Building();
        void setup(const ConfigStructBuilding &buildingInput);
        void step();
        void postprocess();
        void preprocess();
        void postTimeStep();
        void stepAppliancesUse();
        void stepAppliancesUseBatteries(Contract_Negotiation * building_negotiation);
        void stepAppliancesNegotiationNeighbourhood(
            const Contract_Negotiation & building_negotiation);
        void stepAppliancesNegotiation(
            const Contract_Negotiation & building_negotiation);
        void addContactsTo(Contract_Negotiation * building_negotiation,
                           const bool battery);
        bool decisionBoolean(const double val1, const double val2) const;
        bool hasZone(const std::string& zoneName) const;
        int getID() const;
        double getPower() const;
        double decisionDoubleVec(const std::vector<double> & val,
                                 const std::vector<double> & power,
                                 const double currentState) const;

    private:
        void setOccupantGainsForZone(std::shared_ptr<Building_Zone> zone);
        void setOccupantWindowDecisionForZone(std::shared_ptr<Building_Zone> zone);
        void setOccupantLightDecisionForZone(std::shared_ptr<Building_Zone> zone);
        void setOccupantBlindDecisionForZone(std::shared_ptr<Building_Zone> zone);
        void setOccupantHeatDecisionsForZone(std::shared_ptr<Building_Zone> zone);
        void setOccupantCountForZone(std::shared_ptr<Building_Zone> zone);
        void setAppGainsForZone(std::shared_ptr<Building_Zone> zone);
        void buildingInteractions();

        int id; //<! id of the building
        std::string name; //<! name of the building
        std::vector<Occupant> population; //<! occupants in the building
        std::vector<std::shared_ptr<Building_Zone>> zones; //<! zones in the building
        Building_Appliances appliances; //<! building appliances
    };

//**********************************************************************

#endif  // BUILDING_HPP_
