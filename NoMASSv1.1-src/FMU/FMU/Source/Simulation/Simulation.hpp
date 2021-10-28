// Undefined description of file -- Jacob Chapman -- 20156//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef SIMULATION_HPP_
#define SIMULATION_HPP_

#include <string>
#include <vector>

#include <Building/Building.hpp>
#include <Log/Log.hpp>
#include <LVN/LVN.hpp>

//**********************************************************************

/**
 * @brief Main NoMASS simulation manager
 * @details Called through the FMU interface, manages the simulation of the NoMass platform
 */

//**********************************************************************

class Simulation
    {
    public:
        Simulation();

        void preprocess();
        void parseConfiguration(const std::string & file);
        void setupSimulationModel();
        void postprocess();
        void preTimeStep();
        void timeStep();
        void postTimeStep();

        void setConfigurationurationFile(const std::string & filename);
        static double getGridCost();

    private:

        static void calculateGridCost();
        std::vector<int> monthCount;
        std::string simulationConfigurationFile;
        static double gridCost;
        /**
        * The Buildings
        */
        std::vector<Building> buildings;
        /**
        * Manages the low voltage network
        */
        LVN lvn;
        /**
        * Manages the building power negotiation
        */
        Contract_Negotiation building_negotiation;

        int GridPowerDataId;
        int GridCostDataId;
        int GridReceivedDataId;
    };

//**********************************************************************

#endif  // SIMULATION_HPP_
