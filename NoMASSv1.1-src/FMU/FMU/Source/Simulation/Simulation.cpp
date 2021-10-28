// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <algorithm>
#include <iostream>
#include <limits>
#include <string>

#include <Building/Building.hpp>
#include <Configuration/Configuration.hpp>
#include <DataStore/DataStore.hpp>
#include <Environment/Environment.hpp>
#include <LVN/LVN_Node.hpp>
#include <Simulation/SimulationTime.hpp>

#include "Simulation.hpp"

//**********************************************************************

double Simulation::gridCost;

double Simulation::getGridCost()
    {
    return Simulation::gridCost;
    }

Simulation::Simulation()
    {
    simulationConfigurationFile = "SimulationConfig.xml";
    }

void Simulation::setConfigurationurationFile(const std::string & filename)
    {
    this->simulationConfigurationFile = filename;
    }
/**
 * @brief Calls the simulation preprocess
 * @details Reads in the configuration file and sends to parser.
 * Sets up the EnergyPlus processor, the AgentModel and the ZoneManager.
 */
void Simulation::preprocess()
    {
	//LOG << "Simulation::preprocess()..." << "\n";
    parseConfiguration(Configuration::RunLocation
                       + simulationConfigurationFile);
	//LOG << "SimulationTime::preprocess()..." << "\n";
	SimulationTime::preprocess();
	//LOG << "SimulationTime::preprocess() done!" << "\n";
	if (!LOG.getError())
        {
        setupSimulationModel();
        }
    }

void Simulation::parseConfiguration(const std::string & file)
    {
	//LOG << "Simulation::parseConfiguration(" << file << ")..." << "\n";
	Configuration::parseConfiguration(file);
	//LOG << "Simulation::parseConfiguration() done!" << "\n";
	GridPowerDataId = DataStore::addVariable("grid_power");
    GridCostDataId = DataStore::addVariable("grid_cost");
    GridReceivedDataId = DataStore::addVariable("grid_received");
    }

void Simulation::setupSimulationModel()
    {
	//LOG << "Simulation.cpp Simulation::setupSimulationModel()..." << "\n";
    for (ConfigStructBuilding b : Configuration::buildings)
        {
		//LOG << "  new building..." << "\n";
        buildings.push_back(Building());
        buildings.back().setup(b);
        buildings.back().preprocess();
        }
	//LOG << "                                                ...done!!!" << "\n";
	//LOG << "  lvn.setup()..." << "\n"; 
    lvn.setup();
	//LOG << "             ...done!!!" << "\n";
    }

/**
 * @brief Calls the simulation prostprocess
 *
 */
void Simulation::postprocess()
    {
    for (Building &b : buildings)
        {
        b.postprocess();
        }
    DataStore::print();
    DataStore::clearValues();
    SimulationTime::reset();
    }

/**
 * @brief processes before timestep
 */
void Simulation::preTimeStep()
    {
    SimulationTime::trackTime();
    Environment::calculateDailyMeanTemperature();
    }

/**
 * @brief Increments the timestep for the simulation
 * @details Increments the timestep for the EnergyPlus processor, the AgentModel and the ZoneManager.
 * Also we send any effects the agent have to the zones they are located in.
 */
void Simulation::timeStep()
    {
    std::shuffle(buildings.begin(), buildings.end(), Utility::engine);
    calculateGridCost();
    //local negotiation
    for (Building &b : buildings)
        {
        b.step();
        b.stepAppliancesUse();
        // add to contracts
        b.addContactsTo(&building_negotiation, true);
        }

    // battery negotiation
    for (Building &b : buildings)
        {
        b.stepAppliancesUseBatteries(&building_negotiation);
        }
    if (buildings.size() > 1)
        {
        // only process contracts if there is a neighbourhood
        building_negotiation.process();
        }
    for (Building &b : buildings)
        {
        b.stepAppliancesNegotiationNeighbourhood(building_negotiation);
        }
    building_negotiation.clear();

    for (Building &b : buildings)
        {
        b.addContactsTo(&building_negotiation, false);
        }


    double diff = building_negotiation.getDifference();
    Contract m;
    m.id = -1;
    m.buildingID = -1;
    m.supplied = std::abs(diff);
    m.suppliedCost = gridCost;
    m.requested = 0;
    if (diff > 0.0)
        {
        m.supplied = 0;
        m.suppliedCost = 0;
        m.requested = std::numeric_limits<double>::max();
        }
    m.suppliedLeft = m.supplied;
    building_negotiation.submit(m);
    building_negotiation.process();
    for (Building &b : buildings)
        {
        b.stepAppliancesNegotiation(building_negotiation);
        }
    m = building_negotiation.getContract(m.buildingID, m.id);
    DataStore::addValue(GridReceivedDataId, m.received);
    DataStore::addValue(GridPowerDataId, m.supplied);
    DataStore::addValue(GridCostDataId, m.suppliedCost);
    building_negotiation.clear();
    }

/**
 * @brief processes After timestep
 */
void Simulation::postTimeStep()
    {
    for (Building &b : buildings)
        {
        b.postTimeStep();
        lvn.setPowerForID(b.getPower(), b.getID());
        }
    lvn.postTimeStep();
    }

void Simulation::calculateGridCost()
    {
    gridCost = 0;
    if (!Configuration::info.GridCost.empty())
        {
        gridCost = Configuration::info.GridCost[0];
        if (Configuration::info.GridCost.size() == 24)
            {
            int stepCount = Configuration::getStepCount();
            int hour = (stepCount * Configuration::lengthOfTimestep()) / 3600;
            int hourOfDay = hour % 24;
            gridCost = Configuration::info.GridCost[hourOfDay];
            }
        else if (Configuration::info.GridCost.size() == 48)
            {
            int stepCount = Configuration::getStepCount();
            int hour = (stepCount * Configuration::lengthOfTimestep()) / 1800;
            int halfHourOfDay = hour % 48;
            gridCost = Configuration::info.GridCost[halfHourOfDay];
            }
        }
    }

//**********************************************************************
