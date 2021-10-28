// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <Configuration/Configuration.hpp>
#include <Simulation/Simulation.hpp>
#include <Utility/Utility.hpp>

//**********************************************************************

Simulation sim;

int main(int argc, char *argv[])
    {
    if (argc > 1)
        {
        sim.setConfigurationurationFile(argv[1]);
        }

    sim.preprocess();

    int days = Utility::calculateNumberOfDays(Configuration::info.startDay,
               Configuration::info.startMonth,
               Configuration::info.endDay,
               Configuration::info.endMonth);

    int totoaltimesteps = days * 24 * Configuration::info.timeStepsPerHour;
    for (int i = 0; i < totoaltimesteps; i++)
        {
        sim.preTimeStep();
        sim.timeStep();
        sim.postTimeStep();
        }
    sim.postprocess();
    }

//**********************************************************************
