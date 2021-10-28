// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef APPLIANCE_GENERIC_CSV_HPP_
#define APPLIANCE_GENERIC_CSV_HPP_

#include <string>
#include <vector>

#include <Appliances/Appliance.hpp>
#include <Models/Model_Appliance_Power_CSV.hpp>

//**********************************************************************

/**
 * @brief appliance read in from csv class
 * @details The CSV agent, handles the csv model
 */
class Appliance_Generic_CSV : public Appliance
    {
    public:
        Appliance_Generic_CSV();
        void setup(ConfigStructAppliance a);
        void step();
        void setFileSupply(const std::string & filename);
        void setFileDemand(const std::string & filename);

    private:
        Model_Appliance_Power_CSV modelSupply;
        Model_Appliance_Power_CSV modelDemand;
        std::string fileSupply;
        std::string fileDemand;
        bool enableSupply;
        bool enableDemand;
        std::vector<double> powers;
    };

//**********************************************************************

#endif  // APPLIANCE_GENERIC_CSV_HPP_
