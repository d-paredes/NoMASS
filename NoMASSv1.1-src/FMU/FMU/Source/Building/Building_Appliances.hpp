// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef BUILDING_APPLIANCES_HPP_
#define BUILDING_APPLIANCES_HPP_

#include <vector>
#include <string>

#include <Appliances/Appliance_Battery.hpp>
#include <Appliances/Appliance_Battery_GridCost_Reward.hpp>
#include <Appliances/Appliance_FMI.hpp>
#include <Appliances/Appliance_Group.hpp>
#include <Appliances/Appliance_Generic_CSV.hpp>
#include <Appliances/Appliance_Group_Battery.hpp>
#include <Appliances/Appliance_Large.hpp>
#include <Appliances/Appliance_Large_CSV.hpp>
#include <Appliances/Appliance_Large_Learning.hpp>
#include <Appliances/Appliance_Large_Learning_CSV.hpp>
#include <Appliances/Appliance_Small.hpp>
#include <Configuration/Configuration.hpp>
#include <Contract/Contract_Negotiation.hpp>

//**********************************************************************

/**
 * @brief Manages the different building appliances agents
 * @details Each building has a set of applaince this class manages them
 */
class Building_Appliances
    {
    public:
        Building_Appliances();
        void setup(const ConfigStructBuilding & b);
        void stepLocal();
        void stepAppliancesUseBatteries(
            Contract_Negotiation * building_negotiation);
        void stepLocalNegotiation();
        void stepGlobalNegotiation(
            const Contract_Negotiation & building_negotiation);

        void stepNeighbourhoodNegotiation(
            const Contract_Negotiation & building_negotiation);

        void postprocess();
        void preprocess();
        void postTimeStep();
        void addCurrentStates(const int stateid);
        void addContactsTo(Contract_Negotiation * building_negotiation,
                           const bool battery);
        double getTotalPower() const;

    private:
        double totalPower;
        int buildingID;

        std::vector<int> currentStates;
        std::string buildingString;
        Contract_Negotiation app_negotiation;

        Appliance_Group<Appliance_Large> large;
        Appliance_Group<Appliance_Large_CSV> largeCSV;
        Appliance_Group<Appliance_Large_Learning> largeLearning;
        Appliance_Group<Appliance_Large_Learning_CSV> largeLearningCSV;
        Appliance_Group<Appliance_Small> small;
        Appliance_Group<Appliance_FMI> fmi;
        Appliance_Group<Appliance_Generic_CSV> csv;
        Appliance_Group_Battery<Appliance_Battery> batteries;
        Appliance_Group_Battery<Appliance_Battery_GridCost_Reward> batteriesGrid;

        int datastoreIDNonShiftSupplied;
        int datastoreIDNonShiftSuppliedCost;
        int datastoreIDNonShiftReceived;
        int datastoreIDNonShiftRequested;
        int datastoreIDNonShiftCost;
    };

//**********************************************************************

#endif  // BUILDING_APPLIANCES_HPP_
